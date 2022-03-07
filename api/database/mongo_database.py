from api.database.database import Database
from typing import List, Set, Union
from api.database.databaseerror import DatabaseError
from api.database.models.blog_model import BlogModel
from api.database.models.page_model import PageModel
from api.database.models.sort_model import SortModel
from api.database.models.user_model import UserModel
from api.schemas.types.blog import NewBlog, UpdatedBlog
from api.utils.logging.defaultlogger import DefaultLogger
from logging import Logger
import motor.motor_asyncio
from api.config.settings import settings
from pymongo import TEXT
from bson.objectid import ObjectId

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
        self.blogs_collection.create_index([("$**", TEXT)])

    async def get_blogs(
        self,
        query: dict,
        sort: SortModel | None,
        page: PageModel,
    ) -> List[BlogModel]:
        try:
            blogs: List[BlogModel] = []
            sort = sort if sort is not None else SortModel(key="_id", dir=1)
            skip = (page.number - 1) * page.size

            cursor = (
                self.blogs_collection.find(query)
                .sort(sort.key, sort.dir)
                .skip(skip)
                .limit(page.size)
            )

            for document in await cursor.to_list(length=page.size):
                blogs.append(BlogModel(**document))
            return blogs
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to get the specified blogs")

    async def get_blogs_count(self) -> int:
        return await self.blogs_collection.count_documents({})

    async def search_blogs(
        self,
        text: str,
        page: PageModel,
        max_limit: int,
    ) -> List[BlogModel]:
        try:
            blogs: List[BlogModel] = []
            skip = (page.number - 1) * page.size

            cursor = (
                self.blogs_collection.find(
                    {"$text": {"$search": text}, "is_published": True},
                    {"score": {"$meta": "textScore"}},
                )
                .skip(skip)
                .limit(max_limit)
                .sort("score", {"$meta": "textScore"})
            )
            for document in await cursor.to_list(length=page.size):
                blogs.append(BlogModel(**document))
            return blogs
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to search for your blogs")

    async def get_blog(self, blog_id: str) -> Union[BlogModel, None]:
        try:
            document = await self.blogs_collection.find_one({"_id": ObjectId(blog_id)})
            if document is not None:
                return BlogModel(id=blog_id, **document)
            return None
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to get the specified blog")

    async def get_all_topics(self) -> Set[str]:
        try:
            count = await self.get_blogs_count()
            cursor = self.blogs_collection.find({})

            return {
                BlogModel(**document).topic
                for document in await cursor.to_list(length=count)
            }
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to get the blog topics")

    async def create_new_blog(self, new_blog: NewBlog) -> BlogModel:
        pass

    async def update_blog(self, updated_blog: UpdatedBlog) -> BlogModel:
        pass

    async def delete_blog(self, blog_id: str):
        pass

    async def publish_blog(self, blog_id: str):
        pass

    async def increment_blog_view_count(self, blog_id: str):
        pass

    async def add_user(self, user: UserModel) -> str:
        try:
            result = await self.users_meta_collection.insert_one(user.__dict__)
            return result.inserted_id
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to Save User Meta data to Database")

    async def get_user(self, user_id: str) -> UserModel | None:
        try:
            document = await self.users_meta_collection.find_one({"user_id": user_id})
            if document is not None:
                return UserModel(**document)
            else:
                return None
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to get the specified user's data.")
