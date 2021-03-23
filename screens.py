from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Timer  # TODO


def StartMenu(update, context):
    keyboard = [
        [InlineKeyboardButton('last results tests', callback_data='last_results'),
        InlineKeyboardButton('history tests', callback_data='history')],
            [InlineKeyboardButton('Run tests', callback_data='run'),
        InlineKeyboardButton('Setting of notifications', callback_data='notifications')]
    ]
    if context.chat_data['reply']:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Start Menu',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        update.message.reply_text('Start Menu', reply_markup=InlineKeyboardMarkup(keyboard))


def LastTests(update, context):
    pass


def HistoryTests(update, context):
    pass


def RunTests(update, context):
    pass


def SettingsNotion(update, context):
    pass


def AdminMenu(update, context):
    pass