from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase

class Tag(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)