from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from settings.core import env

scheduler = AsyncIOScheduler(timezone=utc)
JOB_INTERVAL = env.int('JOB_INTERVAL', default=30)
