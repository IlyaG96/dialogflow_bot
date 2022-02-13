from telegram.ext import Updater, MessageHandler, Filters
from config import TG_TOKEN, PROJECT_ID, LANGUAGE_CODE, DEBUG_CHAT_ID
from dialogflow import detect_intent_texts
import time
import logging
import telegram


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def dialog_flow(update, context):
    user_message = update.message.text
    user_id = update.effective_chat.id
    language_code = context.bot_data['language_code']
    project_id = context.bot_data['project_id']
    dialogflow_response = detect_intent_texts(
        project_id, user_id, user_message, language_code
    )
    answer = dialogflow_response.query_result.fulfillment_text
    update.message.reply_text(answer)


def run_tg_bot(logger, updater):
    while True:
        try:
            dispatcher = updater.dispatcher
            dispatcher.bot_data['language_code'] = LANGUAGE_CODE
            dispatcher.bot_data['project_id'] = PROJECT_ID

            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, dialog_flow))
            updater.start_polling()
            updater.idle()
        except Exception as exception:
            logger.error(exception, exc_info=True)
            time.sleep(60)


def main():
    chat_id = DEBUG_CHAT_ID
    updater = Updater(TG_TOKEN)
    bot = telegram.Bot(token=TG_TOKEN)
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    run_tg_bot(logger, updater)


if __name__ == '__main__':
    main()
