from dataclasses import dataclass
from typing import List, Union
from datetime import datetime
from pydantic.main import BaseModel
from pydantic.types import constr
from api.database.database import Database
from api.schemas.types.blog import Blog, NewBlog, UpdatedBlog
from api.schemas.types.user import User
from api.utils.errors.apierror import APIError
from api.utils.errors.blogerrors import BlogNotFound, BlogTitleTaken
from api.utils.helpers import update_attributes
from api.utils.constants import messages
from random import randint
from pydantic import EmailStr


@dataclass
class Author:
    user_id: str
    blog_id: str


class UserLoginModel(BaseModel):
    email: EmailStr
    password: constr(min_length=5)


class UserModel(BaseModel):
    id: str
    email: EmailStr
    hash: str


blogs: List[Blog] = []
authors: List[Author] = []
users: List[UserModel] = []

for i in range(20):
    blogs.append(
        Blog(
            id=i,
            title=f"My blog {i}",
            topic=f"Topic {i%2}",
            is_featured=True if i % 2 == 0 else False,
            is_published=True if i % 2 == 0 else False,
            published_on=datetime.now(),
            modified_on=datetime.now(),
            summary="Summary Text",
            image_url="",
            view_count=10,
            content=f"My awesome blog {i}",
        )
    )
    authors.append(Author(f"UU-{randint(1,4)}", i))

for i in range(1, 5):
    users.append(UserModel(id=f"UU-{i}", email=f"kal{i}@gmail.com", hash="XXXXXXX"))


class TestDatabase(Database):
    def get_all_blogs(self) -> List[Blog]:
        return blogs

    def get_blogs(self, is_published: bool) -> List[Blog]:
        return [blog for blog in blogs if blog.is_published == is_published]

    def get_blog_by_id(self, blog_id: str) -> Union[Blog, None]:
        return next((blog for blog in blogs if (str(blog.id) == blog_id)), None)

    def get_blog_author(self, blog_id: str) -> Union[User, None]:
        user_id = next(
            (author.user_id for author in authors if author.blog_id == blog_id)
        )
        if user_id == None:
            raise APIError(messages.BLOG_NOT_FOUND)

        user = next((user for user in users if user.id == user_id))
        if user == None:
            return None

        return User(id=user.id, email=user.email)

    def get_user_blogs(self, user_id: str) -> List[Blog]:
        return [blog for blog in blogs if str(blog.id) == user_id]

    def get_all_topics(self) -> List[str]:
        return {blog.topic for blog in blogs}

    def create_new_blog(self, new_blog: NewBlog) -> Blog:
        blog = Blog.fromNewBlog(id=len(blogs), new_blog=new_blog)
        existingBlog = next((b for b in blogs if (blog.title == b.title)), None)

        if existingBlog != None:
            raise BlogTitleTaken()

        try:
            blogs.append(blog)
            return blog
        except:
            raise APIError(messages.ERROR_CREATING_BLOG)

    def update_blog(self, updated_blog: UpdatedBlog) -> Blog:
        blog = next(
            (blog for blog in blogs if (str(blog.id) == updated_blog.id)),
            None,
        )
        if blog == None:
            raise BlogNotFound()
        try:
            update_attributes(blog, **updated_blog.__dict__)
        except:
            raise APIError(messages.ERROR_UPDATING_BLOG)
        return blog

    def delete_blog(self, blog_id: str):
        blog = next(
            (blog for blog in blogs if (str(blog.id) == blog_id)),
            None,
        )
        if blog == None:
            raise BlogNotFound()
        try:
            blogs.remove(blog)
        except:
            raise APIError(messages.ERROR_DELETING_BLOG)

    def publish_blog(self, blog_id: str) -> Blog:
        blog = next(
            (blog for blog in blogs if (str(blog.id) == blog_id)),
            None,
        )
        if blog == None:
            raise BlogNotFound()
        blog.is_published = True
        return blog

    def increment_blog_view_count(self, blog_id: str) -> Blog:
        blog = next(
            (blog for blog in blogs if (str(blog.id) == blog_id)),
            None,
        )
        if blog == None:
            raise BlogNotFound()
        blog.view_count += 1
        return blog

    def get_user_by_id(self, user_id: str) -> Union[User, None]:
        user = next(
            (user for user in users if (str(user.id) == user_id)),
            None,
        )
        if user == None:
            return None

        return User(id=user.id, email=user.email)
