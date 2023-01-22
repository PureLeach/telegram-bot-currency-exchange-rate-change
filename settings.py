from environs import Env

env = Env()
env.read_env(override=True)

API_TOKEN = env.str('API_TOKEN')
CBR_URL = env.str('CBR_URL')
