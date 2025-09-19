import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import PINECONE_API_KEY

# Set environment variables for Pinecone
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


INDEX_NAME = "basicagentrag-bot-index"


# 1. Retriever Function
def get_retriever(query: str):
    """Initializes and returns pinecone vector store retriever"""

    # Ensure the index exists, create if not
    if INDEX_NAME not in pc.list_indexes():
        print("Creating new index...")

        pc.create_index(
            name=INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

        print("Index created successfully")

    vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    return vectorstore.as_retriever()


# 2. Upload documents to vector store
def add_documents(text_content: str):
    """
    Adds a single text document to the pinecone vector store
    splits the text into chunks, embeds the chunks, before embedding and upserting into pinecone
    """

    if not text_content:
        raise ValueError("Text content is required")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )

    # create langchain document objects from the raw text
    documents = text_splitter.create_documents(text_content)

    print("Splitting document into chunks for indexing...")

    # get vector store instance to add documents
    vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)

    print("Adding documents to vector store...")

    # add documents to vector store
    vectorstore.add_documents(documents)

    print("Documents added to vector store successfully")
