from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyMarkup
from config import tg_token, project_id, language_code
from dialogflow import detect_intent_texts


def start(update, context):
    update.message.reply_text(
        'Здравствуйте!',
        reply_markup=ReplyMarkup(),
    )


def help_command(update, context):
    update.message.reply_text('Help!')


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


def run_tg_bot() -> None:

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['language_code'] = language_code
    dispatcher.bot_data['project_id'] = project_id

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, dialog_flow))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run_tg_bot()
