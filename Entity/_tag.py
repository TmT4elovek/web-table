from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase

class Tag(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tag'

    id   = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False, unique=True)
    notes  = relationship('Note', back_populates='tag', uselist=True)