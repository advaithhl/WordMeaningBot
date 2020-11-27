import json
import os

import requests
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


def start(update, context):
    """ Greet user when start command is sent. """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi! I'm a dictionary bot!\n"
        "Send me a word, and I'll send you back its Oxford meaning.")


def make_output(word):
    """ Make calls to util functions and return final str result. """
    response = _request_oxford(word)
    if response.ok:
        definitions = _filter_definitions(response)
        output = '\n'.join((f'{idx}. {definition}'
                            for (idx, definition) in
                            enumerate(definitions, start=1)))
        return output


def _filter_definitions(response):
    """ Get the definitions from the API response. """
    json_response = json.loads(response.text)
    senses = json_response['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
    return (s['definitions'][0] for s in senses)


def _request_oxford(word):
    """ Request word via Oxford API. """
    url = "https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/" + word
    auth = {
        'app_id': os.getenv('OXFORD_APPID'),
        'app_key': os.getenv('OXFORD_APPKEY'),
    }
    response = requests.get(url, headers=auth)
    return response


def define(update, context):
    """ Send definition(s), if available to user. """
    word = update.message.text
    output = make_output(word)
    if output:
        response_message = output
    else:
        response_message = 'Sorry, I was unable to complete that request.'
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message)


if __name__ == "__main__":
    # get token
    TOKEN = os.getenv('DEFINEBOT_TOKEN')
    NAME = "DefineBot"

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    define_handler = MessageHandler(Filters.text & (~Filters.command), define)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(define_handler)

    updater.start_polling()
    updater.idle()
