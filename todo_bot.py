from telegram.ext import (
    Updater, CommandHandler, PicklePersistence, CallbackQueryHandler
)
from settings import TELEGRAM_BOT_TOKEN
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def create_todo(update, context):
    # a function to let users create todos
    message_id = update.effective_message.message_id
    message_text = update.effective_message.text
    todo_title = message_text.replace("/new ", "")
    context.user_data[message_id] = {"title": todo_title, "completed": False}
    update.message.reply_text("A new todo has been created !")


def generate_todo_message(context):
    text = "Here are the list of todos:\n"
    keyboard = []
    for key, value in context.user_data.items():
        status_emo = "✅" if value['completed'] else "❌"
        title = value['title'] + " " + status_emo
        keyboard.append(
            [InlineKeyboardButton(text=title, callback_data=key)]
        )
        text += "\n- " + title
    reply_markup = InlineKeyboardMarkup(keyboard)
    return text, reply_markup


# a function to view list of todos
def show_todo_list(update, context):
    text, reply_markup = generate_todo_message(context)
    update.message.reply_text(text, reply_markup=reply_markup)


def help(update, context):
    update.message.reply_text(
        text="Available Commands:\n"
             "/new Make a new tutorial\n"
             "/list - to show a list of todos"
    )


def button_click(update, context):
    query = update.callback_query
    todo_id = int(query.data)
    current_status = context.user_data[todo_id]['completed']
    context.user_data[todo_id]['completed'] = not current_status
    text, reply_markup = generate_todo_message(context)
    query.answer(text='Todo status updated !')
    query.edit_message_text(text=text, reply_markup=reply_markup)


my_persistence = PicklePersistence(filename='data.bck')

updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True, persistence=my_persistence)

updater.dispatcher.add_handler(CommandHandler('new', create_todo))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('list', show_todo_list))

updater.dispatcher.add_handler(CallbackQueryHandler(button_click))

updater.start_polling()
updater.idle()
