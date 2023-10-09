from pydantic import BaseModel
from typing import List
from abc import ABC, abstractmethod


# Абстрактний клас
class PublicModel(ABC):
    @abstractmethod
    def book_info(self):
        pass


# Клас моделі книги
class BookModel(BaseModel):
    title: str
    author: str
    year: int


# Клас книги, що наслідується від моделі книги та абстрактного класу
class Book(PublicModel):
    def __init__(self, book_model: BookModel):
        self.title = book_model.title
        self.author = book_model.author
        self.year = book_model.year

    def book_info(self):
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}"


# Клас журналу, що наслідується від моделі книги та абстрактного класу
class Magazine(PublicModel):
    def __init__(self, book_model: BookModel):
        self.title = book_model.title
        self.author = book_model.author
        self.year = book_model.year

    def book_info(self):
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}"


# Клас бібліотеки
class Library:
    def __init__(self):
        self.books = set()
        print("Бібліотека створена")

    # Додавання книги в бібліотеку
    def add_book(self, book):
        if book not in self.books:
            self.books.add(book)
            print(f"Додана книга: {book.title}")
        else:
            print(f"Книга {book.title} вже існує у бібліотеці.")

    # Видалення книги з бібліотеки
    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
            print(f"Видалена книга: {book.title}")
        else:
            print(f"Книга {book.title} не знайдена у бібліотеці.")

    # Ітератор для проходження по всіх книгах
    def __iter__(self):
        return iter(self.books)

    # Генератор, який повертає книги за ім'ям автора
    def books_by_author(self, author_name):
        for __book in self.books:
            if book.author == author_name:
                yield book


# Декоратор для логування при додаванні нової книги до бібліотеки
def log_addition(func):
    def wrapper(*args, **kwargs):
        _book = args[1]
        print(f"Додаємо книгу: {book.title} (Автор: {book.author})")
        return func(*args, **kwargs)
    return wrapper


# Декоратор, який перевіряє наявність книги в бібліотеці перед її видаленням
def check_book_existence(func):
    def wrapper(*args, **kwargs):
        library, book = args[0], args[1]
        if book in library.books:
            return func(*args, **kwargs)
        else:
            print(f"Книга {book.title} вже в бібліотеці.")
    return wrapper


# Контекстний менеджер для роботи з файлами
class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        return open(self.file_path, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


if __name__ == "__main__":
    # Створення бібліотеки
    library = Library()

    # Створення книги та журналу
    book_model1 = BookModel(title="Книга: Магия утра", author="Хэл Элрод", year=2014)
    book_model2 = BookModel(title="Книга: Эссенциализм", author="Грег МакКеон", year=2014)
    book_model3 = BookModel(title="Книга: Магическая формула", author="Хэл Элрод", year=2019)
    journal_model1 = BookModel(title="Журнал: The Ukrainian Week", author="Ukraine", year=2019)

    book1 = Book(book_model1)
    book2 = Book(book_model2)
    book3 = Book(book_model3)
    journal1 = Magazine(journal_model1)

    # Додавання книг та журналу у бібліотеку
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    library.add_book(journal1)

    # Виведення списку книг у бібліотеці
    print("Список книг у бібліотеці:")
    for book in library:
        print(book.book_info())

    # Виведення списку книг бібліотеки по імені автора
    print("\nСписок книг у бібліотеці за автором Хэл Элрод:")
    for book in library.books_by_author("Хэл Элрод"):
        print(book.book_info())

    # Збереження списку книг у файл
    with FileManager("books.txt") as file:
        for book in library:
            file.write(f"{book.title}, {book.author}, {book.year}\n")

    # Видалення книги з бібліотеки
    library.remove_book(book1)

    # Виведення списку книг після видалення
    print("\nСписок у бібліотеці після видалення:")
    for book in library:
        print(book.book_info())

    # Додавання книг з файлу в бібліотеку
    with open("books.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            book_info = line.strip().split(", ")
            book_model = BookModel(title=book_info[0], author=book_info[1], year=int(book_info[2]))
            new_book = Book(book_model)
            library.add_book(new_book)

    # Виведення списку книг бібліотеки після додавання
    print("\nСписок книг у бібліотеці після додавання з файлу:")
    for book in library:
        print(book.book_info())
