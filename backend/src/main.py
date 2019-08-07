# coding=utf-8

from .entities.entity import Session, engine, Base
from .entities.book import Book

# generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check for existing data
books = session.query(Book).all()

if len(books) == 0:
    # create and persist dummy book
    python_book = Book("SQLAlchemy Book", "SQLAlchemy devs", "script")
    session.add(python_book)
    session.commit()
    session.close()

    # reload books
    books = session.query(Book).all()

# show existing books
print('### books:')
for book in books:
    print(f'({book.id}) {book.title} - {book.author}')