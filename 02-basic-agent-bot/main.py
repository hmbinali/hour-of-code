from fastapi import FastAPI

app = FastAPI(name="LangGraph AI Agent")


@app.get("/health")
def health_check():
    return {"message": "Health check passed"}


def main():
    print("Hello from 02-basic-agent-bot!")


if __name__ == "__main__":
    main()
