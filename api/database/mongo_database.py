from fastapi import UploadFile
from api.database.database import Database
from typing import AsyncGenerator, List, Set, Tuple, Union
from api.database.databaseerror import DatabaseError
from api.database.models.blog_model import BlogModel
from api.database.models.image_meta_data import ImageMetaData
from api.database.models.page_model import PageModel
from api.database.models.sort_model import SortModel
from api.database.models.user_model import UserModel, UserRole
from api.utils.logging.defaultlogger import DefaultLogger
from logging import Logger
import motor.motor_asyncio
from api.config.settings import settings
from pymongo import TEXT
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

USERS_COLLECTION = "users"
BLOGS_COLLECTION = "blogs"
FILES_COLLECTION = "fs.files"


class MongoDatabase(Database):
    def __init__(self, logger=DefaultLogger()) -> None:
        self.logger: Logger = logger
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.mongodb_url,
        )
        self.main_db = self.client[settings.main_db_name]
        self.users_collection = self.main_db[USERS_COLLECTION]
        self.blogs_collection = self.main_db[BLOGS_COLLECTION]
        self.files_collection = self.main_db[FILES_COLLECTION]
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

    async def get_blog_by_id(self, blog_id: str) -> Union[BlogModel, None]:
        try:
            document = await self.blogs_collection.find_one({"_id": ObjectId(blog_id)})
            if document is not None:
                return BlogModel(**document)
            return None
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to get the specified blog")

    async def get_blog_by_title(self, title: str) -> Union[BlogModel, None]:
        try:
            document = await self.blogs_collection.find_one({"title": title})
            if document is not None:
                return BlogModel(**document)
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

    async def add_new_blog(self, new_blog: BlogModel) -> Union[BlogModel, None]:
        try:
            result = await self.blogs_collection.insert_one(new_blog.dict())
            return (
                await self.get_blog_by_id(str(result.inserted_id))
                if result.inserted_id is not None
                else None
            )
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to add blog to Database")

    async def update_blog(self, updated_blog: BlogModel) -> Union[BlogModel, None]:
        try:
            result = await self.blogs_collection.replace_one(
                {"_id": ObjectId(updated_blog.id)}, updated_blog.dict()
            )
            return (
                await self.get_blog_by_id(updated_blog.id)
                if result.modified_count > 0
                else None
            )
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to update the blog.")

    async def delete_blog(self, blog_id: str) -> bool:
        try:
            result = await self.blogs_collection.delete_one({"_id": ObjectId(blog_id)})
            return result.deleted_count > 0
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to delete the blog.")

    async def add_user(self, user: UserModel) -> str:
        try:
            result = await self.users_collection.insert_one(user.__dict__)
            return result.inserted_id
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to Save User Meta data to Database")

    async def get_user(self, user_id: str) -> UserModel | None:
        try:
            document = await self.users_collection.find_one({"user_id": user_id})
            if document is not None:
                return UserModel(**document)
            else:
                return None
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to get the specified user's data.")

    async def save_image(
        self,
        blog_id: str,
        image: UploadFile,
    ) -> str:
        g_fs = AsyncIOMotorGridFSBucket(self.main_db)
        meta_data = ImageMetaData(
            content_type=image.content_type,
            reference_id=blog_id,
        )
        image_id = await g_fs.upload_from_stream(
            image.filename,
            image.file,
            metadata=meta_data.dict(),
        )
        return image_id

    async def read_image(
        self, image_id: str, user_id: str
    ) -> Tuple[AsyncGenerator | None, str | None]:
        try:
            g_fs = AsyncIOMotorGridFSBucket(self.main_db)

            image = await self.files_collection.find_one({"_id": ObjectId(image_id)})
            meta_data = ImageMetaData(**image["metadata"])

            blog = await self.get_blog_by_id(meta_data.reference_id)
            if not blog.is_published:
                user_data = await self.get_user(user_id) if user_id else None
                if not user_data or user_data.role != UserRole.ADMIN:
                    return (None, None)

            g_out = await g_fs.open_download_stream(ObjectId(image_id))
            return (self.read_image_in_chunks(g_out), meta_data.content_type)
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to delete the specified image")

    async def delete_image(self, image_id: str) -> bool:
        try:
            g_fs = AsyncIOMotorGridFSBucket(self.main_db)
            await g_fs.delete(ObjectId(image_id))
            return True
        except Exception as error:
            self.logger.error(__name__, error)
            return False

    async def read_image_in_chunks(self, grid_out):
        while True:
            chunk = await grid_out.readchunk()
            if not chunk:
                break
            yield chunk