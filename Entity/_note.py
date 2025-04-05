from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Note(SqlAlchemyBase):
    __tablename__ = 'note'

    id      = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    text    = Column(String(60), nullable=False)
    tag_id  = Column(Integer, ForeignKey('tag.id'))
    user    = relationship("User", backref='notes')