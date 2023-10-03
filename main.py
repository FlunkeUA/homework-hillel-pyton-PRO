from pydantic import BaseModel


class Book:
    book_title = str
    book_author = str
    book_year = int

class BookModel(BaseModel):
