import json

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import os

from PBG_Bot import BotAI

botAI = BotAI(db_file="data/db_esempio.csv")

TOKEN = os.environ['PBG_BOT']

# with open('config.json') as config_file:
#     config = json.load(config_file)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""

    if botAI.check_model():
        try:
            risposta = botAI.bot_reply(update.message.text)
            update.message.reply_text(risposta)
        except Exception as err:
            update.message.reply_text(err)
    else:
        update.message.reply_text("Il Bot non si è avviato")


def bot():
    """Start the bot."""

    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    bot()
