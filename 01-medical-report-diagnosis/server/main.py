from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.route import router as auth_router
from .reports.route import router as reports_router
from .diagnosis.route import router as diagnosis_router


app = FastAPI(
    title="Medical Report Diagnosis",
    description="A RESTful API for a medical report diagnosis service",
)

app.include_router(auth_router)
app.include_router(reports_router)
app.include_router(diagnosis_router)
