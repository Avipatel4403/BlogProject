from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    public: bool
    published: bool


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/createposts")
def create_post(post: Post):
    print(post)
    return {"data": "New post"}
