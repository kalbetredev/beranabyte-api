
from abc import ABC, abstractmethod
from typing import List, Union
from api.schemas.types.blog import Blog, NewBlog
from api.schemas.types.user import User


class Database(ABC):
    @abstractmethod
    def get_all_blogs(self) -> List[Blog]:
        pass

    @abstractmethod
    def get_blogs(self, is_published: bool) -> List[Blog]:
        pass

    @abstractmethod
    def get_blog_by_id(self, blog_id: str) -> Union[Blog, None]:
        pass

    @abstractmethod
    def get_blog_author(self, blog_id: str) -> Union[User, None]:
        pass

    @abstractmethod
    def get_user_blogs(self, user_id: str) -> List[Blog]:
        pass

    @abstractmethod
    def get_all_topics(self) -> List[str]:
        pass
