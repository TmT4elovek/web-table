import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy_serializer import SerializerMixin

from flask_login import UserMixin

from flask_bcrypt import check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'user'

    id         = Column(Integer, autoincrement=True, primary_key=True)
    username   = Column(String(15), nullable=False, unique=True)
    password   = Column(String(25), nullable=False)
    email      = Column(String, nullable=False)
    icon       = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    all_notes  = relationship('Note', backref='creator', cascade='all, delete')

    def check_password(enter_pass):
        return check_password_hash(User.password, enter_pass)
        