from fastapi import HTTPException, BackgroundTasks, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import shutil
import os
import time

from ..auth import create_token
from ..dependencies import get_user_or_404
from .. import models, schemas
from ..database import get_db
from ..hashing import hash_password, verify_password

router = APIRouter(tags=["Users & Authentication"])

def send_welcome_email(email: str):
    print(f"Sending welcome email to {email}...")

@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register_user(
    user: schemas.UserCreate,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db)
):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email is already registered")

    existing_username = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username is already taken")

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
    ) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    background_task.add_task(send_welcome_email, new_user.email)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form.username).first()

    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    token = create_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/users/{id}/upload")
async def upload_profile_pic(
    id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user_or_404)
):
    upload_dir = "/tmp/uploads" if os.environ.get("VERCEL") else "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    filename = f"{id}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    user.profile_pic = f"/uploads/{filename}"
    db.commit()
    return {"profile_pic_url": f"/uploads/{filename}"}
