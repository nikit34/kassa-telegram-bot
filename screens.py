import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import requests

from errors import ErrorsHandler


def StartMenu(update, context):
    keyboard = [
        [InlineKeyboardButton('Last results tests', callback_data='last_results_tests'),
        InlineKeyboardButton('Status pipeline', callback_data='status_pipeline_tests')],
        [InlineKeyboardButton('Run pipeline of tests', callback_data='run_tests')],
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

        self.id_server = '5750'

    def RunTests(self):
        response = ''
        try:
            response = requests.post(f'https://gitlab.rambler.ru/api/v4/projects/{self.id_server}/trigger/pipeline', \
                                     data={
                                         'token': os.environ['CI_JOB_TOKEN'],
                                         'ref': 'ios-ui-tests'
                                     })
        except requests.exceptions.RequestException as error:
            self.errors_handler_network(response, error)
        if response.status_code == 200:
            self.context.bot.send_message(
                chat_id=self.update.effective_chat.id,
                text='tests are running'
            )

    def CancelPipeline(self):
        id_latest = self._get_id_latest_pipeline()
        response = ''
        try:
            response = requests.post(f'https://gitlab.rambler.ru/api/v4/projects/{self.id_server}/pipelines/{id_latest}/cancel', headers={'PRIVATE-TOKEN': os.environ['PRIVATE_TOKEN']})
        except requests.exceptions.RequestException as error:
            self.errors_handler_network(response, error)
            return

    def LastTests(self):
        self.context.bot.send_message(
            chat_id=self.update.effective_chat.id,
            text='Last run of tests\nhttps://kassa-mobile-dev.pages.rambler-co.ru/kassa-ui-tests/'
        )

    def StatusPipeline(self):
        id_latest = self._get_id_latest_pipeline()
        response = ''
        try:
            response = requests.get(f'https://gitlab.rambler.ru/api/v4/projects/{self.id_server}/pipelines/{id_latest}/jobs?include_retried=true', headers={'PRIVATE-TOKEN': os.environ['PRIVATE_TOKEN']})
        except requests.exceptions.RequestException as error:
            self.errors_handler_network(response, error)
            return

    def _get_id_latest_pipeline(self):
        response = ''
        try:
            response = requests.get(f'https://gitlab.rambler.ru/api/v4/projects/{self.id_server}/pipelines/latest', headers={'PRIVATE-TOKEN': os.environ['PRIVATE_TOKEN']})
            try:
                return response.json()['id']
            except (AttributeError, KeyError) as error:
                self.errors_handler(error)
        except requests.exceptions.RequestException as error:
            self.errors_handler_network(response, error)



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