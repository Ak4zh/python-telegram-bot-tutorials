from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TELEGRAM_BOT_TOKEN, CUSTOM_REPLIES


def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name)
    )


def custom_reply(update, context):
    # a function to listen to new messages from user and send a reply
    message_text = update.effective_message.text
    reply_text = CUSTOM_REPLIES.get(message_text)
    if reply_text:
        update.message.reply_text(text=reply_text)


updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
# a handler to filter messages received in private
updater.dispatcher.add_handler(
    MessageHandler(Filters.private, custom_reply)
)

updater.start_polling()
updater.idle()
