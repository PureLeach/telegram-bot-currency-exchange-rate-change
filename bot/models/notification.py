from sqlalchemy import BigInteger, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from settings.db import Base


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, unique=False)
    user = relationship('User', backref='notifications', lazy='joined')
    currency_char_code = Column(String, nullable=False)
    value = Column(Numeric(precision=9, scale=4), nullable=False)
    comparison = Column(String, nullable=False)
