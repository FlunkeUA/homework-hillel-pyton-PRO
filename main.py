from pydantic import BaseModel
from abc import ABC, abstractmethod


class PublicationModel(BaseModel):
    title: str
    author: str
    year: int


class BookModel(BaseModel):
    pass


class JournalModel(BookModel):
    month: int


class AbstractPublication(ABC):
    @abstractmethod
    def display_info(self):
        raise NotImplementedError


class Book:
    def __init__(self, model: BookModel):
        self._model = model

    def __str__(self):
        return f'{self._model.titel} + {self._model.author} + {self._model.year}'

    def display_info(self):
        return str(self)
