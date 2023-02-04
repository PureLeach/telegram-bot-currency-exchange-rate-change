from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator
from pytz import utc

from settings.core import REDIS_DB_SCHEDULER, REDIS_HOST, REDIS_PORT, env

scheduler = ContextSchedulerDecorator(
    AsyncIOScheduler(
        timezone=utc,
        jobstores={
            'default': RedisJobStore(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB_SCHEDULER,
                jobs_key='scheduler_jobs',
                run_times_key='scheduler_running',
            )
        },
    )
)

JOB_INTERVAL = env.int('JOB_INTERVAL', default=30)
