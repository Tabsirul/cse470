from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import health_controller

app = FastAPI(title="StudyBuddy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_controller.router)