from telegram.ext import Updater, CommandHandler
from settings import TELEGRAM_BOT_TOKEN


def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name)
    )


updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
