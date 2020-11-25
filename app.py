import os

from telegram.ext import CommandHandler, Updater


def start(update, context):
    """ Greet user when start command is sent. """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi! I'm a dictionary bot!\n"
        "Send me a word, and I'll send you back its Oxford meaning.")


if __name__ == "__main__":
    # get token
    TOKEN = os.getenv('DEFINEBOT_TOKEN')
    NAME = "DefineBot"

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()
