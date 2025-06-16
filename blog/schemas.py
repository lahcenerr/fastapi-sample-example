from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str

class Blog(BaseModel):
    title: str
    body: str

class ShowUser(BaseModel):
    name: str
    email: str
    
    blogs: List[Blog]


class showBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
