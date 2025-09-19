from typing import TypedDict, List, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field
from langchain_core.tools import tool
import os
from config import GROQ_API_KEY, TAVILY_API_KEY, PINECONE_API_KEY
from langchain_groq import ChatGroq
from vectorstore import get_retriever


# Tools
@tool
def rag_search_tool(query: str) -> str:
    """
    Top-k chunks from KB (empty string if none)
    """
    try:
        retriever_instance = get_retriever(query)
        docs = retriever_instance.invoke(query, k=3)
        return "\n\n".join(d.page_content for d in docs) if docs else ""
    except Exception as e:
        return f"RAG_ERROR: {e}"


# Pydantic Schemas for structured output
class RouteDecision(BaseModel):
    route: Literal["rag", "web", "answer", "end"]
    reply: str | None = Field(None, description="Filled only when the route == 'end'")


class RagJudge(BaseModel):
    sufficient: bool = Field(
        ...,
        description="True if retrieved information is sufficient to answer the question else False",
    )


# LLM instances with structured schemas
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

router_llm = ChatGroq(
    temperature=0, model="llama-3.3-70b-versatile"
).with_structured_output(RouteDecision)

judge_llm = ChatGroq(
    temperature=0, model="llama-3.3-70b-versatile"
).with_structured_output(RagJudge)

answer_llm = ChatGroq(temperature=0.7, model="llama-3.3-70b-versatile")


# State: shared data structure
class AgentState(TypedDict, total=False):
    messages: List[BaseMessage]
    route: Literal["rag", "web", "answer", "end"]
    rag: str
    web: str
    web_search_enabled: bool


# Node: For individual functions


# Node 1: Router (Decision node)
def router_node(state: AgentState) -> AgentState:
    print("Router node called")

    # extract query
    query = next(
        (m.content for m in reversed(state["messages"]) if isinstance(HumanMessage)), ""
    )
    # if isinstance(HumanMessage):
    #     for m in reversed(state["messages"]):
    #         next(m.content)
    # else:
    #     ""

    web_search_enabled = state.get("web_search_enabled", True)
    print(f"Router received web search info: {web_search_enabled}")

    system_prompt = (
        "You are an intelligent routing agent designed to direct user queries to the most appropriate tool."
        "Your primary goal is to provide accurate and relevant information by selecting the best source."
        "Prioritize using the **internal knowledge base (RAG)** for factual information that is likely "
        "to be contained within pre-uploaded documents or for common, well-established facts."
    )

    if web_search_enabled:
        system_prompt += (
            "You **CAN** use web search for queries that require very current, real-time, or broad general knowledge "
            "that is unlikely to be in a specific, static knowledge base (e.g., today's news, live data, very recent events)."
            "\n\nChoose one of the following routes:"
            "\n- 'rag': For queries about specific entities, historical facts, product details, procedures, or any information that would typically be found in a curated document collection (e.g., 'What is X?', 'How does Y work?', 'Explain Z policy')."
            "\n- 'web': For queries about current events, live data, very recent news, or broad general knowledge that requires up-to-date internet access (e.g., 'Who won the election yesterday?', 'What is the weather in London?', 'Latest news on technology')."
        )

    else:
        system_prompt += (
            "**Web search is currently DISABLED.** You **MUST NOT** choose the 'web' route."
            "If a query would normally require web search, you should attempt to answer it using RAG (if applicable) or directly from your general knowledge."
            "\n\nChoose one of the following routes:"
            "\n- 'rag': For queries about specific entities, historical facts, product details, procedures, or any information that would typically be found in a curated document collection, AND for queries that would normally go to web search but web search is disabled."
            "\n- 'answer': For very simple, direct questions you can answer without any external lookup (e.g., 'What is your name?')."
        )

    system_prompt += (
        "\n- 'answer': For very simple, direct questions you can answer without any external lookup (e.g., 'What is your name?')."
        "\n- 'end': For pure greetings or small-talk where no factual answer is expected (e.g., 'Hi', 'How are you?'). If choosing 'end', you MUST provide a 'reply'."
        "\n\nExample routing decisions:"
        "\n- User: 'What are the treatment of diabetes?' -> Route: 'rag' (Factual knowledge, likely in KB)."
        "\n- User: 'What is the capital of France?' -> Route: 'rag' (Common knowledge, can be in KB or answered directly if LLM knows)."
        "\n- User: 'Who won the NBA finals last night?' -> Route: 'web' (Current event, requires live data)."
        "\n- User: 'How do I submit an expense report?' -> Route: 'rag' (Internal procedure)."
        "\n- User: 'Tell me about quantum computing.' -> Route: 'rag' (Foundational knowledge can be in KB. If KB is sparse, judge will route to web if enabled)."
        "\n- User: 'Hello there!' -> Route: 'end', reply='Hello! How can I assist you today?'"
    )

    messages = [
        ("system", system_prompt),
        ("user", query),
    ]

    result: RouteDecision = router_llm.invoke(messages)

    initial_router_decision = result.route

    router_override_reason = None

    # Override decision to go for web search
    if not web_search_enabled and initial_router_decision == "web":
        result.route = "rag"
        router_override_reason = "Web search disabled by user, redirected to rag"
        print("Router decision overridden to rag, change from web to rag")

    print(f"Router decision: {result.route}, Reply (if 'end'): {result.reply}")

    out = {
        "messages": state["messages"],
        "router": result.route,
        "web_search_enabled": web_search_enabled,
    }

    if router_override_reason:
        out["initial_router_decision"] = initial_router_decision
        out["router_override_reason"] = router_override_reason

    if result.route == "end":
        out["messages"] = state["messages"] + [
            AIMessage(content=result.reply or "hello")
        ]

    print("Existing router_node")

    return out


# Node 2: RAG Lookup
def rag_node(state: AgentState) -> AgentState:
    print("RAG node called")

    # extract query
    query = next(
        (m.content for m in reversed(state["messages"]) if isinstance(HumanMessage)), ""
    )

    web_search_enabled = state.get("web_search_enabled", True)
    print(f"RAG node received web search info: {web_search_enabled}")

    print(f"RAG Query: {query}")

    chunks = rag_search_tool.invoke(query)

    # Logic to handle chunk
    if chunks.startswith("RAG_ERROR:"):
        print(f"RAG_ERROR: {chunks}, checking with search enabled status")

        # If rag fails and web search is enabled, try web search
        next_route = "web" if web_search_enabled else "answer"
        return {**state, "rag": "", "route": next_route}

        if chunks:
            print(f"Retrieved chunks from RAG : {chunks[:5]}...")
        else:
            print("No RAG chunks found")

        judge_messages = [
            (
                "system",
                (
                    "You are a judge evaluating if the **retrieved information** is **sufficient and relevant** "
                    "to fully and accurately answer the user's question. "
                    "Consider if the retrieved text directly addresses the question's core and provides enough detail."
                    "If the information is incomplete, vague, outdated, or doesn't directly answer the question, it's NOT sufficient."
                    "If it provides a clear, direct, and comprehensive answer, it IS sufficient."
                    "If no relevant information was retrieved at all (e.g., 'No results found'), it is definitely NOT sufficient."
                    '\n\nRespond ONLY with a JSON object: {"sufficient": true/false}'
                    "\n\nExample 1: Question: 'What is the capital of France?' Retrieved: 'Paris is the capital of France.' -> {\"sufficient\": true}"
                    "\nExample 2: Question: 'What are the symptoms of diabetes?' Retrieved: 'Diabetes is a chronic condition.' -> {\"sufficient\": false} (Doesn't answer symptoms)"
                    "\nExample 3: Question: 'How to fix error X in software Y?' Retrieved: 'No relevant information found.' -> {\"sufficient\": false}"
                ),
            ),
            (
                "user",
                f"Question: {query}\n\nRetrieved info: {chunks}\n\nIs this sufficient to answer the question?",
            ),
        ]

        verdict: RagJudge = judge_llm.invoke(judge_messages)

        print(f"RAG Judge verdict: {verdict.sufficient}")
        print(f"Existing RAG node")

        # Dedice next route based on sufficient and web search info

        if verdict.sufficient:
            next_route = "answer"
        else:
            next_route = "web" if web_search_enabled else "answer"
            print(
                f"RAG not sufficient, Web search enabled: {web_search_enabled}, redirecting to {next_route}"
            )

        return {
            **state,
            "rag": chunks,
            "route": next_route,
            "web_search_enabled": web_search_enabled,
        }

    print(f"Retrieved chunks from RAG : {chunks[:5]}...")

    return {**state, "rag": chunks, "route": "rag"}
