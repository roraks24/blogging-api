from fastapi import FastAPI, HTTPException, Depends
from . import models
from sqlalchemy.orm import Session
from .database import get_db

def get_post_or_404(id: int,
                    db: Session= Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post

def get_user_or_404(id: int,
                    db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
     raise HTTPException(status_code=404, detail="User not found")
    
    return user