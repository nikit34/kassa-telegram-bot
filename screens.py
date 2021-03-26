import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import requests

from errors import ErrorsHandler


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


class MainScreen(ErrorsHandler):
    def __init__(self, update, context):
        super().__init__(update, context)
        self.update = update
        self.context = context

    def RunTests(self):
        response = ''
        try:
            response = requests.post('https://gitlab.rambler.ru/api/v4/projects/5750/trigger/pipeline', \
                                     data={
                                         'token': os.environ['CI_JOB_TOKEN'],
                                         'ref': 'ios-ui-tests'
                                     })
        except requests.exceptions.RequestException as error:
            print(f'[ERROR] RunTests -> POST request failed\nstatus code: {response.status_code}', error)
            self.context.bot.send_message(
                chat_id=self.update.effective_chat.id,
                text=f'Error occurred on GitLab side\nstatus code: {response.status_code}')
            return
        if response.status_code == 200:
            self.context.bot.send_message(
                chat_id=self.update.effective_chat.id,
                text='tests are running'
            )

    def CancelPipeline(self):
        response = ''
        try:
            response = requests.get('https://gitlab.rambler.ru/api/v4/projects/5750/pipelines/latest', headers={'PRIVATE-TOKEN': os.environ['PRIVATE_TOKEN']})
        except requests.exceptions.RequestException as error:
            self.errors_handler_network(response, error)
            return
        try:
            id_latest = response.json()['id']
        except KeyError as error:
            self.errors_handler('Key Error', error)
            return
        try:
            response = requests.post(f'https://gitlab.rambler.ru/api/v4/projects/5750/pipelines/{id_latest}/cancel', headers={'PRIVATE-TOKEN': os.environ['PRIVATE_TOKEN']})
        except requests.exceptions.RequestException as error:
            self.errors_handler_network(response, error)
            return

    def LastTests(self):
        self.context.bot.send_message(
            chat_id=self.update.effective_chat.id,
            text='Last run of tests\nhttps://kassa-mobile-dev.pages.rambler-co.ru/kassa-ui-tests/'
        )

    def StatusPipeline(self):
        pass


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