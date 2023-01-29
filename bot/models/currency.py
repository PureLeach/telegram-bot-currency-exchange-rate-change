from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from settings.db import Base


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    char_code = Column(String, unique=True)
    users = relationship('User', secondary='currency_users', back_populates='currencies', lazy='joined')
