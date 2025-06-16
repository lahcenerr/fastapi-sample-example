from typing import List
from fastapi import APIRouter
from .. import schemas, database, models
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.showBlog], tags=['Blogs'])
def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()

    return blogs

@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.showBlog, tags=['Blogs'])
def show(id, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        body = f"The blog with id {id} does not exist"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=body)
    return blog


@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['Blogs'])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh (new_blog)
    return new_blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blogs'])
def destroy(id, db: Session = Depends(get_db)):

    res = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': f"blog with id {id} doesn't exist"})
    db.commit()
    return {'message': f'blog with id {id} has been deleted'}


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': f"blog with id {id} doesn't exist"})
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return "Updated"
