import os
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from actions import start, buttons


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=os.environ['TOKEN_BOT'], use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(buttons))

updater.start_polling()
updater.idle()
