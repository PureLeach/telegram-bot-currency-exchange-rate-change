import copyreg
import ssl

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from settings.core import env


def save_sslcontext(obj):
    return obj.__class__, (obj.protocol,)


copyreg.pickle(ssl.SSLContext, save_sslcontext)

scheduler = AsyncIOScheduler(
    timezone=utc,
    jobstores={
        'default': RedisJobStore(
            host='127.0.0.1', port=6379, db=0, jobs_key='scheduler_jobs', run_times_key='scheduler_running'
        )
    },
)
JOB_INTERVAL = env.int('JOB_INTERVAL', default=30)
