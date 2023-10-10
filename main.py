from pydantic import BaseModel
from typing import List
from abc import ABC, abstractmethod
from collections import defaultdict


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


# Декоратор для логування при додаванні нової книги до бібліотеки
def log_addition(func):
    def wrapper(*args, **kwargs):
        _book = args[1]
        print(f"Додаємо {_book.title}, (Автор: {_book.author})")
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


# Клас бібліотеки
class Library:
    def __init__(self):
        self.books = set()
        self.books_by_author = defaultdict(list)
        print("Бібліотека створена")

    @log_addition
    def add_book(self, book):
        if book not in self.books:
            self.books.add(book)
            self.books_by_author[book.author].append(book)

    @check_book_existence
    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)

    def __iter__(self):
        return iter(self.books)

    def books_by_author(self, author_name):
        return self.books_by_author[author_name]

    def print_books_by_author(self, author_name):
        books = self.books_by_author.get(author_name, [])
        if books:
            for book in books:
                print(book.book_info())
        else:
            print(f"No books found for author {author_name}.")

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            for book in self.books:
                file.write(f"{book.title}, {book.author}, {book.year}\n")

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                book_info = line.strip().split(", ")
                book_model = BookModel(title=book_info[0], author=book_info[1], year=int(book_info[2]))
                new_book = Book(book_model)
                self.add_book(new_book)


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
    print("\nСписок книг у бібліотеці:")
    for book in library:
        print(book.book_info())

    # Виведення книг за певним автором
    print("\nСписок книг у бібліотеці - автор Хэл Элрод:")
    library.print_books_by_author("Хэл Элрод")

    # Сохранение списка книг в файл
    library.save_to_file("books.txt")

    # Видалення книги з бібліотеки
    library.remove_book(book1)

    # Виведення списку книг після видалення
    print("\nСписок у бібліотеці після видалення:")
    for book in library:
        print(book.book_info())

    # Додавання книг з файлу в бібліотеку
    print('\nДодаемо з файлу')
    library.load_from_file("books.txt")

    # Виведення списку книг бібліотеки після додавання
    print("\nСписок книг у бібліотеці після додавання з файлу:")
    for book in library:
        print(book.book_info())
