from __future__ import annotations

from collections.abc import Iterable

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(
    title="Social Network API",
    version="1.0.0",
    description="Simple REST API for users and posts (CRUD).",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=30, examples=["mark_kr"])
    email: str = Field(examples=["mark@example.com"])
    full_name: str = Field(examples=["Mark Kriukov"])


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=30)
    email: str | None = None
    full_name: str | None = None


class User(UserBase):
    id: int


class PostBase(BaseModel):
    title: str = Field(min_length=3, max_length=120, examples=["My first post"])
    content: str = Field(examples=["Hello, social network!"])
    user_id: int = Field(examples=[1])


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=120)
    content: str | None = None
    user_id: int | None = None


class Post(PostBase):
    id: int


users: dict[int, User] = {}
posts: dict[int, Post] = {}
user_counter = 1
post_counter = 1


def _list_values(data: Iterable[BaseModel]) -> list[BaseModel]:
    return list(data)


@app.get("/users", response_model=list[User], tags=["Users"])
def list_users() -> list[User]:
    return _list_values(users.values())


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(payload: UserCreate) -> User:
    global user_counter

    new_user = User(id=user_counter, **payload.model_dump())
    users[user_counter] = new_user
    user_counter += 1
    return new_user


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
def get_user(user_id: int) -> User:
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=User, tags=["Users"])
def update_user(user_id: int, payload: UserUpdate) -> User:
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated = user.model_copy(update=payload.model_dump(exclude_none=True))
    users[user_id] = updated
    return updated


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(user_id: int) -> None:
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    users.pop(user_id)
    # Remove posts that belonged to the deleted user.
    for post_id, post in list(posts.items()):
        if post.user_id == user_id:
            posts.pop(post_id)


@app.get("/posts", response_model=list[Post], tags=["Posts"])
def list_posts(user_id: int | None = Query(default=None)) -> list[Post]:
    if user_id is None:
        return _list_values(posts.values())
    return [p for p in posts.values() if p.user_id == user_id]


@app.post("/posts", response_model=Post, status_code=status.HTTP_201_CREATED, tags=["Posts"])
def create_post(payload: PostCreate) -> Post:
    global post_counter

    if payload.user_id not in users:
        raise HTTPException(status_code=404, detail="Author user not found")

    new_post = Post(id=post_counter, **payload.model_dump())
    posts[post_counter] = new_post
    post_counter += 1
    return new_post


@app.get("/posts/{post_id}", response_model=Post, tags=["Posts"])
def get_post(post_id: int) -> Post:
    post = posts.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put("/posts/{post_id}", response_model=Post, tags=["Posts"])
def update_post(post_id: int, payload: PostUpdate) -> Post:
    post = posts.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    patch = payload.model_dump(exclude_none=True)
    if "user_id" in patch and patch["user_id"] not in users:
        raise HTTPException(status_code=404, detail="Author user not found")

    updated = post.model_copy(update=patch)
    posts[post_id] = updated
    return updated


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Posts"])
def delete_post(post_id: int) -> None:
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    posts.pop(post_id)
