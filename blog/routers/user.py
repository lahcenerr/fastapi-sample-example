from typing import List
from fastapi import APIRouter

from blog.hashing import Hash
from .. import schemas, database, models
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        body = f"The user with id {id} does not exist"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=body)
    return user


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy_user(id, db: Session = Depends(get_db)):

    res = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': f"user with id {id} does not exist"})
    db.commit()
    return {'message': f'user with id {id} has been deleted'}