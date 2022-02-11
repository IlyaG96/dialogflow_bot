from telegram import ForceReply, ReplyMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from environs import Env


def start(update, context):
    user = update.effective_user
    update.message.reply_text(
        f'Здравствуйте!',
        reply_markup=ReplyMarkup(),
    )


def help_command(update, context):
    update.message.reply_text('Help!')


def echo(update, context):
    update.message.reply_text(update.message.text)


def main() -> None:
    env = Env()
    env.read_env()
    TG_TOKEN = env.str("TG_TOKEN")
    updater = Updater(TG_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()