from fastapi import FastAPI

from .database import Base, engine
from .routers import (users, protected, events, photos, galleries, customer)
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Photo Sharing Platform",
    description="TrizenAI Full Stack Internship Challenge",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:5173"
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(protected.router)
app.include_router(galleries.router)
app.include_router(events.router)
app.include_router(photos.router)
app.include_router(customer.router)

@app.get("/")
def root():
    return {
        "message": "Photo Sharing Platform API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }