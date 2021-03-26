
class ErrorsHandler:
    def __init__(self, update, context):
        self.update = update
        self.context = context

    def errors_handler(self, msg, error):
        print(f'[ERROR] {self.__class__.__name__} -> {msg}', error)
        self.context.bot.send_message(
            chat_id=self.update.effective_chat.id,
            text=f'Error on GitLab side\n{msg}')

    def errors_handler_network(self, response, error):
        print(f'[ERROR] {self.__class__.__name__} -> {response.request.method} failed\nstatus code: {response.status_code}', error)
        self.context.bot.send_message(
            chat_id=self.update.effective_chat.id,
            text=f'Error on GitLab side\nin {self.__class__.__name__}\nstatus code: {response.status_code}')
