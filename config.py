from environs import Env

env = Env()
env.read_env()
VK_TOKEN = env.str('VK_TOKEN')
TG_TOKEN = env.str('TG_TOKEN')
PROJECT_ID = env.str('PROJECT_ID')
LANGUAGE_CODE = 'ru-ru'
DEBUG_CHAT_ID = env.int('DEBUG_CHAT_ID')
