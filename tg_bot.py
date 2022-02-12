from telegram import ReplyMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from environs import Env
import environs
from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, text, language_code):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    answer = response.query_result.fulfillment_text
    return answer


if __name__ == "__main__":
    env = environs.Env()
    env.read_env()


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
    env = Env()
    env.read_env()
    TG_TOKEN = env.str("TG_TOKEN")
    GOOGLE_APPLICATION_CREDENTIALS = env.str('GOOGLE_APPLICATION_CREDENTIALS')
    project_id = env.str('PROJECT_ID')
    language_code = "ru-ru"
    updater = Updater(TG_TOKEN)
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
