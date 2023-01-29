from sqlalchemy import Column, ForeignKey, Integer

from settings.db import Base


class CurrencyUser(Base):
    __tablename__ = 'currency_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    currency_id = Column(Integer, ForeignKey('currencies.id'))
