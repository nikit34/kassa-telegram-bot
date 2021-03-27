import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import requests

from errors import ErrorsHandler


def StartMenu(update, context):
    keyboard = [
        [InlineKeyboardButton('Last results tests', callback_data='last_results_tests'),
        InlineKeyboardButton('Status pipeline', callback_data='status_pipeline_tests')],
        [InlineKeyboardButton('Run pipeline of tests', callback_data='run_tests')],
        [InlineKeyboardButton('Cancel pipeline', callback_data='delete_pipeline_tests'),
        InlineKeyboardButton('Enable all runners', callback_data='enable_all_runners')]
    ]
    if context.chat_data['reply']:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Start Menu',
            reply_markup=InlineKeyboardMarkup(keyboard))
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
                                     data={'token': os.environ['CI_JOB_TOKEN'], 'ref': 'ios-ui-tests'})
        except requests.exceptions.RequestException as error:
            self.errors_handler_network(response, error)
        if response.status_code == 201:
            self.context.bot.send_message(
                chat_id=self.update.effective_chat.id,
                text='tests are running')

    def CancelPipeline(self):
        id_latest = self._get_id_latest_pipeline()
        response = ''
        try:
            response = requests.post(f'https://gitlab.rambler.ru/api/v4/projects/{self.id_server}/pipelines/{id_latest}/cancel', \
                                     headers={'PRIVATE-TOKEN': os.environ['PRIVATE_TOKEN']})
        except requests.exceptions.RequestException as error:
            self.errors_handler_network(response, error)
        if response.status_code == 200:
            self.context.bot.send_message(
                chat_id=self.update.effective_chat.id,
                text='pipeline has cancel')

    def LastTests(self):
        self.context.bot.send_message(
            chat_id=self.update.effective_chat.id,
            text='Last run of tests\nhttps://kassa-mobile-dev.pages.rambler-co.ru/kassa-ui-tests/')

    def StatusPipeline(self):
        id_latest = self._get_id_latest_pipeline()
        response = ''
        try:
            response = requests.get(f'https://gitlab.rambler.ru/api/v4/projects/{self.id_server}/pipelines/{id_latest}/jobs?include_retried=true', \
                                    headers={'PRIVATE-TOKEN': os.environ['PRIVATE_TOKEN']})
        except requests.exceptions.RequestException as error:
            self.errors_handler_network(response, error)
        if response.status_code == 200:
            body_jobs = response.json()
            text = ''
            for body_job in body_jobs:
                text += f'{body_job["status"].upper()} - {body_job["name"]}\n' + \
                        f'duration: {body_job["duration"]}s\n' + \
                        f'author:   {body_job["commit"]["author_name"]}\n' + \
                        f'comment:  "{body_job["commit"]["title"]}"\n' + \
                        f'launched: {body_job["user"]["username"]}\n' + \
                         '---------------------------------------\n'
            self.context.bot.send_message(
                chat_id=self.update.effective_chat.id,
                text=text)

    def EnabledRunners(self):
        response = ''
        for runner_id in self._get_id_all_runners():
            try:
                response = requests.post(f'https://gitlab.rambler.ru/api/v4/projects/{self.id_server}/runners', \
                                        headers={'PRIVATE-TOKEN': os.environ['PRIVATE_TOKEN']}, data={'runner_id': runner_id})
                self.context.bot.send_message(
                    chat_id=self.update.effective_chat.id,
                    text=f'1/ {response}')
            except requests.exceptions.RequestException as error:
                self.errors_handler_network(response, error)

                self.context.bot.send_message(
                    chat_id=self.update.effective_chat.id,
                    text=f'2/ {error}, {response}')
            if response.status_code == 200:
                self.context.bot.send_message(
                    chat_id=self.update.effective_chat.id,
                    text=f'runner id: {runner_id} are ready')

    def _get_id_latest_pipeline(self):
        response = ''
        try:
            response = requests.get(f'https://gitlab.rambler.ru/api/v4/projects/{self.id_server}/pipelines/latest', \
                                    headers={'PRIVATE-TOKEN': os.environ['PRIVATE_TOKEN']})
            try:
                return response.json()['id']
            except (AttributeError, KeyError) as error:
                self.errors_handler(error)
        except requests.exceptions.RequestException as error:
            self.errors_handler_network(response, error)

    def _get_id_all_runners(self):
        response = ''
        try:
            response = requests.get(f'https://gitlab.rambler.ru/api/v4/runners', \
                                    headers={'PRIVATE-TOKEN': os.environ['PRIVATE_TOKEN']})
            try:
                body_runners = response.json()
                for runner in body_runners:
                    yield runner['id']
            except (AttributeError, KeyError) as error:
                self.errors_handler(error)
        except requests.exceptions.RequestException as error:
            self.errors_handler_network(response, error)

