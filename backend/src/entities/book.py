# coding=utf-8

from sqlalchemy import Column, String, Integer, Date
from marshmallow import Schema, fields
from .entity import Entity, Base


class Book(Entity, Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    pages = Column(Integer)
    published = Column(Date)

    def __init__(self, title, author, created_by):
        Entity.__init__(self, created_by)
        self.title = title
        self.author = author

class BookSchema(Schema):
    id = fields.Number()
    title = fields.Str()
    author = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()