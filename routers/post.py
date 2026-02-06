import oauth2
import models, schemas, utils
from typing import List
from sqlalchemy.orm import Session
from database import engine, SessionLocal, get_db
from fastapi import Response, status, HTTPException, Depends, APIRouter

posts_router = APIRouter(prefix="/posts", tags=["Posts"])

@posts_router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()

    return posts

@posts_router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@posts_router.get("/{id}", response_model=schemas.Post)
def get_post(id : str, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} was not found."
        )
    return post

@posts_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : str, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} does not exist"
        )
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@posts_router.put("/{id}", response_model=schemas.Post)
def update_post(id : str, post:schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    updatePost = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updatePost.first()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} does not exist"
        )
    
    updatePost.update(post.dict(), synchronize_session=False)
    db.commit()

    return updatePost.first()
