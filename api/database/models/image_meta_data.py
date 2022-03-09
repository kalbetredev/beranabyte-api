from pydantic import BaseModel


class ImageMetaData(BaseModel):
    content_type: str
    reference_id: str
