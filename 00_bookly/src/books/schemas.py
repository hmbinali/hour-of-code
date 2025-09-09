from pydantic import BaseModel
from datetime import datetime


class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str


class BookUpdateSchema(BaseModel):
    title: str
    author: str
    language: str
    publisher: str
    published_date: datetime
    description: str
    page_count: int


class BookCreateSchema(BaseModel):
    """
    This class is used to validate the request when creating or updating a book
    """

    title: str
    author: str
    isbn: str
    description: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str
