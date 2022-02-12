from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyMarkup
from config import tg_token, project_id
from dialogflow import detect_intent_texts


def start(update, context):
    update.message.reply_text(
        f'Здравствуйте!',
        reply_markup=ReplyMarkup(),
    )


def help_command(update, context):
    update.message.reply_text('Help!')


def dialog_flow(update, context):
    user_message = update.message.text
    user_id = update.effective_chat.id
    language_code = context.bot_data['language_code']
    project_id = context.bot_data['project_id']

    incoming_message = detect_intent_texts(
        project_id, user_id, user_message, language_code
    )

    update.message.reply_text(incoming_message)


def main() -> None:

    language_code = "ru-ru"
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data["language_code"] = language_code
    dispatcher.bot_data["project_id"] = project_id

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, dialog_flow))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
