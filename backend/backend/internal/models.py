from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator

from bson import ObjectId
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class ArticleModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    title: str = Field(...)
    source: str = Field(...)
    link: str = Field(...)
    authors: list[str] = Field(...)
    keywords: str = Field(...)
    summary: str = Field(...)
    full_text: str = Field(...)


class ArticleCollection(BaseModel):
    articles: list[ArticleModel]