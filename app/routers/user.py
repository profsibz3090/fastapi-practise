from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from .. import schemas, utils, models
from ..database import get_db
from ..oauth2 import get_current_user, oauth2_scheme

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(
        **user.dict()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {id} does not exist'
        )
    return user

@router.get('/', response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    users = db.query(models.User).all()
    return users