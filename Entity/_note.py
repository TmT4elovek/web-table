from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Note(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'note'

    id      = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    creator = relationship("User", back_populates='all_notes', foreign_keys=[user_id])
    text    = Column(String(60), nullable=False)
    tag_id  = Column(Integer, ForeignKey('tag.id'))
    tag     = relationship('Tag', back_populates='notes', foreign_keys=[tag_id])