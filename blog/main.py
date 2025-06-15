from typing import Optional
from fastapi import FastAPI
import uvicorn

from blog.schemas import Blog

app = FastAPI()

@app.get('/blog')
def index():
    return {'data': f'list of blogs'}

@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id = id
    return {"data": id}

@app.get('/blog/{id}/comments')
def comments(id):
    # fetch comments of a blog
    return {'data': {'1', '2'}} 

@app.post('/blog')
def create_blog(blog: Blog):
    return {'data': f'Blog {blog.title} is created'}

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.12", port=1000)