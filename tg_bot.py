from telegram.ext import Updater, MessageHandler, Filters
from dialogflow import detect_intent_texts
from logger import TelegramLogsHandler
from environs import Env
import telegram
import logging
import time

logger = logging.getLogger('Logger')
logger.setLevel(logging.WARNING)


def fetch_message(update, context):
    user_message = update.message.text
    user_id = update.effective_chat.id
    language_code = context.bot_data['language_code']
    project_id = context.bot_data['project_id']
    dialogflow_response = detect_intent_texts(
        project_id, user_id, user_message, language_code
    )
    answer = dialogflow_response.query_result.fulfillment_text
    update.message.reply_text(answer)


def main():
    env = Env()
    env.read_env()
    tg_token = env.str('TG_TOKEN')
    project_id = env.str('PROJECT_ID')
    language_code = 'ru-ru'
    debug_chat_id = env.int('DEBUG_CHAT_ID')
    updater = Updater(tg_token)
    bot = telegram.Bot(token=tg_token)
    logger.addHandler(TelegramLogsHandler(bot, debug_chat_id))

    while True:
        try:
            dispatcher = updater.dispatcher
            dispatcher.bot_data['language_code'] = language_code
            dispatcher.bot_data['project_id'] = project_id
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, fetch_message))
            updater.start_polling()
            updater.idle()
        except Exception as exception:
            logger.exception(exception, exc_info=True)
            time.sleep(60)


if __name__ == '__main__':
    main()
