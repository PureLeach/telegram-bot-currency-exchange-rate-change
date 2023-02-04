from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from settings.core import DATABASE_URL, env

data_store = SQLAlchemyJobStore(url=DATABASE_URL)
scheduler = AsyncIOScheduler(timezone=utc, data_store=data_store)
JOB_INTERVAL = env.int('JOB_INTERVAL', default=1 * 1)
