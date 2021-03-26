import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import requests


def StartMenu(update, context):
    keyboard = [
        [InlineKeyboardButton('Last results tests', callback_data='last_results_tests'),
        InlineKeyboardButton('Status tests', callback_data='status_pipeline_tests')],
        [InlineKeyboardButton('Run tests', callback_data='run_tests')],
        [InlineKeyboardButton('Delete pipeline', callback_data='delete_pipeline_tests'),
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
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Last run of tests \n\
https://kassa-mobile-dev.pages.rambler-co.ru/kassa-ui-tests/'
    )


def StatusPipeline(update, context):
    pass


def RunTests(update, context):
    response = requests.post('https://gitlab.rambler.ru/api/v4/projects/5750/trigger/pipeline', \
                  data={
                      'token': os.environ['CI_JOB_TOKEN'],
                      'ref': 'ios-ui-tests'
                  })
    if response.status_code == 200:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='tests are running'
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Error occurred on GitLab side \n\
status code: {response.status_code}'
        )


def DeletePipeline(update, context):
    response = requests.delete('https://gitlab.rambler.ru/api/v4/projects/5750/pipelines', headers={'PRIVATE-TOKEN': os.environ['PRIVATE_TOKEN']})
    # response_dict = response.json()
    # id_latest = response_dict['id']
    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{response}'
        )
    #
    # 'curl --header "PRIVATE-TOKEN: <your_access_token>" "https://gitlab.example.com/api/v4/projects/1/pipelines/46"'
    # response = requests.delete('https://gitlab.rambler.ru/api/v4/projects/5750/trigger/pipeline', \
    #               data={
    #                   'token': os.environ['CI_JOB_TOKEN'],
    #                   'ref': 'ios-ui-tests'
    #               })
    # if response.status_code == 200:
    #     context.bot.send_message(
    #         chat_id=update.effective_chat.id,
    #         text='pipeline has deleted'
    #     )
    # else:
    #     context.bot.send_message(
    #         chat_id=update.effective_chat.id,
    #         text=f'Error occurred on GitLab side \n\
    #     status code: {response.status_code}'
    #     )


def SettingsNotion(update, context):
    pass


def AdminMenu(update, context):
    pass