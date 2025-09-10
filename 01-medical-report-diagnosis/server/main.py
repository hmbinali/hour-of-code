from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.route import router as auth_router


app = FastAPI(
    title="Medical Report Diagnosis",
    description="A RESTful API for a medical report diagnosis service",
)

app.include_router(auth_router)
