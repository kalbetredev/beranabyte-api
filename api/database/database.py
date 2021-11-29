
from abc import ABC, abstractmethod
from typing import List
from api.schemas.types.blog import Blog
from api.schemas.types.user import User


class Database(ABC):
    @abstractmethod
    def get_all_blogs(self) -> List[Blog]:
        pass

    @abstractmethod
    def get_blog_author(self, blog_id: str) -> User:
        pass

    @abstractmethod
    def get_user_blogs(self, user_id: str) -> List[Blog]:
        pass
