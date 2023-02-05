from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings.core import DATABASE_URL

metadata = MetaData()
Base = declarative_base(metadata=metadata)
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
