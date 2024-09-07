from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter

from app.oauth2 import get_current_user
from .. import schemas, utils, models
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostOut])
def index(db: Session = Depends(get_db), current_user: schemas.PostBase = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    
    posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Posts, func.count(models.Posts.id).label('votes')).join(models.Vote, models.Posts.id == models.Vote.post_id, isouter=True).group_by(models.Posts.id)
    ok = db.query(models.Posts, func.count(models.Vote.post_id)).join(
        models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).all()
    res = [{'Posts': row[0], 'votes': row[1] }for row in ok]
    return res

@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: schemas.PostBase = Depends(get_current_user)):
    # post = db.query(models.Posts).filter(models.Posts.id == id).first()
    post = db.query(models.Posts, func.count(models.Vote.post_id)).join(
        models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).filter(models.Posts.id == id).group_by(models.Posts.id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id {id} not found'
        )
    
    return {'Posts': post[0], 'votes': post[1] }

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(data: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.PostBase = Depends(get_current_user)):
    post = data.dict()
    new_post = models.Posts(
        user_id = current_user.id,
        **post
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.patch('/{id}', response_model=schemas.Post)
def update_posts(updated_post: schemas.PostCreate, id: int, db: Session = Depends(get_db), current_user: schemas.PostBase = Depends(get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id {id} not found'
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Operation is forbidden'
            )
    post_query.update(updated_post.dict())
    db.commit()
    return post_query.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db),current_user: schemas.PostBase = Depends(get_current_user)):
    delete_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = delete_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id {id} not found'
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Operation is forbidden'
            )
    delete_query.delete()
    db.commit()
    return 'ok'
