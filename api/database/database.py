from abc import ABC, abstractmethod
from typing import List, Set, Union
from api.schemas.types.blog import NewBlog, UpdatedBlog
from api.database.models.blog_model import BlogModel
from api.database.models.page_model import PageModel
from api.database.models.sort_model import SortModel
from api.database.models.user_model import UserModel


class Database(ABC):
    @abstractmethod
    async def get_blogs(
        self,
        query: dict,
        sort: SortModel | None,
        page: PageModel,
    ) -> List[BlogModel]:
        pass

    @abstractmethod
    async def get_blogs_count(self) -> int:
        pass

    @abstractmethod
    async def search_blogs(
        self,
        text: str,
        page: PageModel,
        max_limit: int,
    ) -> List[BlogModel]:
        pass

    @abstractmethod
    async def get_blog(self, blog_id: str) -> Union[BlogModel, None]:
        pass

    @abstractmethod
    async def get_all_topics(self) -> Set[str]:
        pass

    @abstractmethod
    async def create_new_blog(self, new_blog: NewBlog) -> BlogModel:
        pass

    @abstractmethod
    async def update_blog(self, updated_blog: UpdatedBlog) -> BlogModel:
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
    async def add_user(self, user: UserModel) -> bool:
        pass

    @abstractmethod
    async def get_user(self, user_id: str) -> UserModel:
        pass
