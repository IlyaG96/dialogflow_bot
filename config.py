from environs import Env

env = Env()
env.read_env()
vk_token = env.str('VK_TOKEN')
tg_token = env.str('TG_TOKEN')
project_id = env.str('PROJECT_ID')
language_code = 'ru-ru'
