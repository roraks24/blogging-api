from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import time
import os
from .routers import posts, users
from . import models
from .database import engine

app = FastAPI(
    title="Blogging REST API",
    description="A high-performance, production-ready REST API built with FastAPI, SQLAlchemy, JWT Authentication, and automated tests. Optimized for Vercel Serverless.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

models.Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request duration & path logging middleware
@app.middleware("http")
async def log_request(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url.path} {response.status_code} ({duration:.2f}s)")
    return response

# Static uploads directory configuration
UPLOAD_DIR = "/tmp/uploads" if os.environ.get("VERCEL") else "uploads"
try:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
except Exception as e:
    print(f"Static directory mounting skipped: {e}")

@app.get("/", tags=["Health & Info"])
def root():
    return {
        "status": "online",
        "message": "Blogging REST API is running successfully.",
        "documentation": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0",
    }

app.include_router(posts.router)             
app.include_router(users.router)
