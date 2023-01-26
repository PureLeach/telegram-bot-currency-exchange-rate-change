from sqlalchemy import BigInteger, Column, String

from db.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=False, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
