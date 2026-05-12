from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..dependencies import get_post_or_404
from ..auth import get_current_user

router = APIRouter(prefix="/posts" ,tags=["Posts"])


@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@router.get("/{id}")
def get_post(
    id: int,
    post: Session =  Depends(get_post_or_404)
):
    return post

@router.post("/")
def create_post(
    post: schemas.Post, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
    ):
    
    new_post = models.Post(**post. model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}")
def update_post(id: int, post: schemas.Post, 
                db : Session = Depends(get_db),
                current_user = Depends(get_current_user),
                existing_post : models.Post = Depends(get_post_or_404)
                ):
    
    existing_post.author = post.author
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.date_posted = post.date_posted

    db.commit()
    db.refresh(existing_post)
    return existing_post

@router.delete("/{id}")
def delete_post(id: int, 
                db: Session = Depends(get_db),
                current_user = Depends(get_current_user),
                post : models.Post = Depends(get_post_or_404)
                ):
    
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}