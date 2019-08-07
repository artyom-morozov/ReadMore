# coding=utf-8
from flask import Flask, jsonify, request

from .entities.entity import Session, engine, Base
from .entities.book import Book, BookSchema

# creating the Flask application
app = Flask(__name__)

# if needed, generate database schema
Base.metadata.create_all(engine)


@app.route('/books')
def get_books():
    # fetching from the database
    session = Session()
    book_objects = session.query(Book).all()

    # transforming into JSON-serializable objects
    schema = BookSchema(many=True)
    books = schema.dump(book_objects)

    # serializing as JSON
    session.close()
    return jsonify(books.data)


@app.route('/books', methods=['POST'])
def add_book():
    # mount book object
    posted_book = BookSchema(only=('title', 'author'))\
        .load(request.get_json())

    book = Book(**posted_book.data, created_by="HTTP post request")

    # persist book
    session = Session()
    session.add(book)
    session.commit()

    # return created book
    new_book = BookSchema().dump(book).data
    session.close()
    return jsonify(new_book), 201