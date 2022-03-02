from abc import ABC, abstractmethod
from typing import List, Union
from api.schemas.types.blog import Blog, NewBlog, UpdatedBlog
from api.schemas.types.user import User, UserMeta


class Database(ABC):
    @abstractmethod
    async def get_blogs(
        self, user_id: str | None = None, is_published: bool | None = None
    ) -> List[Blog]:
        pass

    @abstractmethod
    async def get_blog(self, blog_id: str) -> Union[Blog, None]:
        pass

    @abstractmethod
    async def get_all_topics(self) -> List[str]:
        pass

    @abstractmethod
    async def create_new_blog(self, new_blog: NewBlog) -> Blog:
        pass

    @abstractmethod
    async def update_blog(self, updated_blog: UpdatedBlog) -> Blog:
        pass

    @abstractmethod
    async def delete_blog(self, blog_id: str):
        pass

    @abstractmethod
    async def publish_blog(self, blog_id: str):
        pass

    @abstractmethod
    async def increment_blog_view_count(self, blog_id: str):
        pass

    @abstractmethod
    async def add_user_meta(self, user_meta: UserMeta) -> bool:
        pass

    @abstractmethod
    async def get_user_meta(self, user_id: str) -> UserMeta:
        pass
