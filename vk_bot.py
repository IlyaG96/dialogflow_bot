from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow import detect_intent_texts
from logger import TelegramLogsHandler
from telegram import Bot
from environs import Env
import vk_api as vk
import logging
import random
import time


logger = logging.getLogger('Logger')
logger.setLevel(logging.WARNING)


def fetch_message(event, vk_api, project_id, language_code):

    user_message = event.text
    user_id = event.user_id
    dialogflow_response = detect_intent_texts(project_id,
                                              user_id,
                                              user_message,
                                              language_code)
    if not dialogflow_response.query_result.intent.is_fallback:
        answer = dialogflow_response.query_result.fulfillment_text
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )


def main():
    env = Env()
    env.read_env()
    vk_token = env.str('VK_TOKEN')
    tg_token = env.str('TG_TOKEN')
    project_id = env.str('PROJECT_ID')
    language_code = 'ru-ru'
    debug_chat_id = env.int('DEBUG_CHAT_ID')
    bot = Bot(token=tg_token)
    logger.addHandler(TelegramLogsHandler(bot, debug_chat_id))

    while True:
        try:
            vk_session = vk.VkApi(token=vk_token)
            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    fetch_message(event, vk_api, project_id, language_code)
        except Exception as exception:
            logger.exception(exception, exc_info=True)
            time.sleep(60)


if __name__ == '__main__':
    main()
