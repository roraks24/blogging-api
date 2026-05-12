from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import time, os
from .routers import posts, users
from . import models
from .database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Logging
@app.middleware("http")
async def log_request(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url} {response.status_code} ({duration: .2f}s)")
    return response

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(posts.router)             
app.include_router(users.router)







    