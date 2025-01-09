from typing import Optional, Union

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
            "title": "favorite cars", "content": "I like ford trucks", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        

def find_index_post(id):
    for i, p  in enumerate(my_posts):
        if p['id'] == id:
            return i



@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return{"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) -1]
    return{"detail": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id; {id} was not found")
    return {"post_detail": post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail= f"Post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail= f"Post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)