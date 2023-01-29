from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from settings.core import DATABASE_URL

data_store = SQLAlchemyJobStore(url=DATABASE_URL)
scheduler = AsyncIOScheduler(timezone=utc, data_store=data_store)
