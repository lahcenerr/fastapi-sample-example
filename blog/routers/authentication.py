from fastapi import APIRouter, Depends, HTTPException, status
from blog import database, schemas, models
from sqlalchemy.orm import Session

from blog.hashing import Hash

router = APIRouter(
    tags=['login']
)

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
    return "logged in"
