from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health_check():
    return {"message": "Health check passed"}


def main():
    print("Hello from 01-medical-report-diagnosis!")


if __name__ == "__main__":
    main()
