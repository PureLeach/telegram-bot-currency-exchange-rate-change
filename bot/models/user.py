from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from settings.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=False, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    currencies = relationship('Currency', secondary='currency_users', back_populates='users', lazy='joined')
