from abc import ABC, abstractmethod
from typing import List, Set, Union
from fastapi import UploadFile
from api.database.models.blogmodel import BlogModel
from api.database.models.pagemodel import PageModel
from api.database.models.projectmodel import ProjectModel
from api.database.models.sortmodel import SortModel
from api.database.models.usermodel import UserModel


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
    async def get_blog_by_id(self, blog_id: str) -> Union[BlogModel, None]:
        pass

    @abstractmethod
    async def get_blog_by_title(self, title: str) -> Union[BlogModel, None]:
        pass

    @abstractmethod
    async def get_all_topics(self) -> Set[str]:
        pass

    @abstractmethod
    async def add_new_blog(self, new_blog: BlogModel) -> Union[BlogModel, None]:
        pass

    @abstractmethod
    async def update_blog(self, updated_blog: BlogModel) -> Union[BlogModel, None]:
        pass

    @abstractmethod
    async def delete_blog(self, blog_id: str) -> bool:
        pass

    @abstractmethod
    async def add_user(self, user: UserModel) -> bool:
        pass

    @abstractmethod
    async def get_user(self, user_id: str) -> UserModel:
        pass

    @abstractmethod
    async def save_image(self, blog_id: str, image: UploadFile) -> str:
        pass

    @abstractmethod
    async def read_image(self, image_id: str):
        pass

    @abstractmethod
    async def delete_image(self, image_id: str):
        pass

    @abstractmethod
    async def add_subscriber(self, email: str) -> bool:
        pass

    @abstractmethod
    async def unsubscribe_user(self, user_token: str) -> bool:
        pass

    @abstractmethod
    async def get_unsubscribe_token(self, email: str) -> bool:
        pass

    @abstractmethod
    async def save_message(self, email: str, message: str) -> bool:
        pass

    @abstractmethod
    async def get_project_by_id(self, project_id: str) -> ProjectModel | None:
        pass

    @abstractmethod
    async def get_project_by_title(self, project_title: str) -> ProjectModel | None:
        pass

    @abstractmethod
    async def add_project(self, project_model: ProjectModel) -> ProjectModel | bool:
        pass

    @abstractmethod
    async def delete_project(self, project_id: str) -> bool:
        pass

    @abstractmethod
    async def update_project(self, project_model) -> ProjectModel | bool:
        pass
