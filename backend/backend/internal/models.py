from datetime import datetime

from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator

from bson import ObjectId
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class ArticleModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    title: str
    source: str
    url: str
    authors: list[str]
    # published: datetime = Field(...)
    text: str


class ArticleCollection(BaseModel):
    articles: list[ArticleModel]