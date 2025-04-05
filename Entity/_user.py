import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'user'

    id         = Column(Integer, autoincrement=True, primary_key=True)
    username   = Column(String(15), nullable=False, unique=True)
    password   = Column(String(25), nullable=False)
    email      = Column(String, nullable=False)
    icon       = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    notes      = relationship('Note', backref='user', cascade='all, delete')