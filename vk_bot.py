from vk_api.longpoll import VkLongPoll, VkEventType
from config import VK_TOKEN, PROJECT_ID, LANGUAGE_CODE, DEBUG_CHAT_ID, TG_TOKEN
from dialogflow import detect_intent_texts
from logger import TelegramLogsHandler
from telegram import Bot
import vk_api as vk
import logging
import random
import time


logger = logging.getLogger('Logger')
logger.setLevel(logging.WARNING)


def fetch_message(event, vk_api):

    user_message = event.text
    user_id = event.user_id
    dialogflow_response = detect_intent_texts(PROJECT_ID,
                                              user_id,
                                              user_message,
                                              LANGUAGE_CODE)
    if not dialogflow_response.query_result.intent.is_fallback:
        answer = dialogflow_response.query_result.fulfillment_text
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )


def run_vk_bot(logger):
    vk_session = vk.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    fetch_message(event, vk_api)
        except Exception as exception:
            logger.error(exception, exc_info=True)
            time.sleep(60)


def main():
    chat_id = DEBUG_CHAT_ID
    bot = Bot(token=TG_TOKEN)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    run_vk_bot(logger)


if __name__ == '__main__':
    main()
