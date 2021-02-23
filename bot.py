#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram.utils.helpers import escape_markdown

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

mctranslate = {
    "A": "ᔑ",
    "B": "ʖ",
    "C": "ᓵ",
    "D": "↸",
    "E": "ᒷ",
    "F": "⎓",
    "G": "⊣",
    "H": "⍑",
    "I": "╎",
    "J": "⋮",
    "K": "ꖌ",
    "L": "ꖎ",
    "M": "ᒲ",
    "N": "リ",
    "O": "𝙹",
    "P": "!¡",
    "Q": "ᑑ",
    "R": "∷",
    "S": "ᓭ",
    "T": "ℸ",
    "U": "⚍",
    "V": "⍊",
    "W": "∴",
    "X": "̇/",
    "Y": "||",
    "Z": "⨅",
    " ": " ",
}

mctranslaterev = {
    "ᔑ": "A",
    "ʖ": "B",
    "ᓵ": "C",
    "↸": "D",
    "ᒷ": "E",
    "⎓": "F",
    "⊣": "G",
    "⍑": "H",
    "╎": "I",
    "⋮": "J",
    "ꖌ": "K",
    "ꖎ": "L",
    "ᒲ": "M",
    "リ": "N",
    "𝙹": "O",
    "!": "P",
    "ᑑ": "Q",
    "∷": "R",
    "ᓭ": "S",
    "ℸ": "T",
    "⚍": "U",
    "⍊": "V",
    "∴": "W",
    "̇/": "X",
    "|": "Y",
    "⨅": "Z",
    " ": " ",
    "¡": "",
}

def translate(mess):
    output = ""
    output.encode('utf-8')
    try:
        for i in mess:
            if i in mctranslate:
                output += mctranslate[i]
            else:
                output += i
        return output
    except:
        return "  "

def translaterev(mess):
    output = ""
    output.encode('utf-8')
    try:
        i=0
        while i<len(mess):
            if mess[i] in mctranslaterev:
                if mess[i] == "|":
                    i += 1
                    output += mctranslaterev[mess[i]]
                else:
                    output += mctranslaterev[mess[i]]
            else:
                output += mess[i]
            i+=1
        return output.lower()   
    except Exception as e:
        print(e)
        return("M8 send me minecraft enchanting table.")

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Use this bot to translate to and from minecraft enchanting table. U can use me in-line, just type @enchantlengbot before wirting a message. U can also send a me a pvt message. Made by @lolloandr')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('U really need help m8?')


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Latin => minecraft enchanting table",
            input_message_content=InputTextMessageContent(
                translate(query.upper())
            ),
        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Send me a pvt message to traslate the text from enchanint table to latin",
            input_message_content=InputTextMessageContent(
                "Send me a pvt message to traslate the text from enchanint table to latin"
            ),
        )
    ]

    update.inline_query.answer(results)

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    #update.message.reply_text(update.message.text)
    update.message.reply_text(translaterev(update.message.text.upper()))

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
