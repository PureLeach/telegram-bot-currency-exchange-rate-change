from aiocache import Cache
from aiocache.serializers import PickleSerializer
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from environs import Env
from loguru import logger

env = Env()
env.read_env(override=True)

API_TOKEN = env.str('API_TOKEN')
CBR_URL = env.str('CBR_URL')

# Database
DB_NAME = env.str('DB_NAME')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_HOST = env.str('DB_HOST')
DB_PORT = env.int('DB_PORT')
DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


logger.add(
    'bot/logs/backend.log',
    format='{time:DD/MM/YYYY HH:mm:ss} | {name}:{function}:{line} | {level} | {message}',
    level='DEBUG',
    rotation='10 MB',
    serialize=True,
    compression='zip',
    backtrace=True,
    diagnose=True,
    encoding='utf-8',
)


REDIS_HOST = env.str('REDIS_HOST', default='127.0.0.1')
REDIS_PORT = env.int('REDIS_PORT', default=6379)
REDIS_DB_CACHE = env.int('REDIS_DB_CACHE', default=0)
REDIS_DB_FSM = env.int('REDIS_DB_FSM', default=1)
REDIS_DB_SCHEDULER = env.int('REDIS_DB_SCHEDULER', default=2)


CACHE_TTL = env.int('CACHE_TTL', default=60 * 60)
cache = Cache(
    Cache.REDIS,
    endpoint=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB_CACHE,
    namespace='cache',
    serializer=PickleSerializer(),
)
storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_FSM, pool_size=10, prefix='aiogram_fsm')
