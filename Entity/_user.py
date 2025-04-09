import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'user'

    id         = Column(Integer, autoincrement=True, primary_key=True)
    username   = Column(String(15), nullable=False, unique=True)
    password   = Column(String(25), nullable=False)
    email      = Column(String, nullable=False)
    icon       = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    all_notes  = relationship('Note', backref='creator', cascade='all, delete')