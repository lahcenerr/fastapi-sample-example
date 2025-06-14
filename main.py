from fastapi import FastAPI

api = FastAPI()

@api.get('/')
def index():
    return {"message": "Hello World"}

@api.get('/about')
def about():
    return {"data": "about page"}