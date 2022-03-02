from api.database.database import Database
from typing import List, Union
from api.database.databaseerror import DatabaseError
from api.schemas.types.blog import Blog, NewBlog, UpdatedBlog
from api.schemas.types.user import UserMeta
from api.utils.logging.defaultlogger import DefaultLogger
from logging import Logger
import motor.motor_asyncio
from api.config.settings import settings

USERS_META_COLLECTION = "users_meta"
BLOGS_COLLECTION = "blogs"


class MongoDatabase(Database):
    def __init__(self, logger=DefaultLogger()) -> None:
        self.logger: Logger = logger
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.mongodb_url,
        )
        self.main_db = self.client[settings.main_db_name]
        self.users_meta_collection = self.main_db[USERS_META_COLLECTION]
        self.blogs_collection = self.main_db[BLOGS_COLLECTION]

    async def get_blogs(
        self, user_id: str | None = None, is_published: bool | None = None
    ) -> List[Blog]:
        pass

    async def get_blog(self, blog_id: str) -> Union[Blog, None]:
        pass

    async def get_all_topics(self) -> List[str]:
        pass

    async def create_new_blog(self, new_blog: NewBlog) -> Blog:
        pass

    async def update_blog(self, updated_blog: UpdatedBlog) -> Blog:
        pass

    async def delete_blog(self, blog_id: str):
        pass

    async def publish_blog(self, blog_id: str):
        pass

    async def increment_blog_view_count(self, blog_id: str):
        pass

    async def add_user_meta(self, user_meta: UserMeta) -> str:
        try:
            result = await self.users_meta_collection.insert_one(user_meta.__dict__)
            return result.inserted_id
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to Save User Meta data to Database")

    async def get_user_meta(self, user_id: str) -> UserMeta:
        try:
            document = await self.users_meta_collection.find_one({"user_id": user_id})
            if document is not None:
                del document["_id"]
                return UserMeta(**document)
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to get the specified user's meta data.")
