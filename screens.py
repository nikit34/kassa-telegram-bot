import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import requests


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
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='tests are running'
    )
    requests.post('https://gitlab.rambler.ru/api/v4/projects/5750/trigger/pipeline', \
                  files={
                      'token': os.environ['CI_JOB_TOKEN'],
                      'ref': 'ios-ui-tests'
                  })


def SettingsNotion(update, context):
    pass


def AdminMenu(update, context):
    pass