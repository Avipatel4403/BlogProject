import time
from random import randrange

import psycopg2
from fastapi import Body, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()


# TODO Store users
class user:
    name: str


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="Avip@tel1234",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection Success")
        break
    except Exception as error:
        print("Connection Failed")
        print("Error: ", error)
        time.sleep(300)


# FIXME
class Post(BaseModel):
    title: str
    content: str
    public: bool
    published: bool


my_post = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


# TODO make  more effecient way of searching for post
def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def root():
    cursor.execute("""SELECT * FROM post""")
    post = cursor.fetchall()
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 100000000)
    my_post.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

        return {"post"}
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT):
    # TODO find efficient way to find index
    # find
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_post[index] = post_dict
    return {"data": post_dict}
