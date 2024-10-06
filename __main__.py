import logging

import argclass
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from telegram.ext.filters import Regex

from handlers import get_level_testers, start
from messages import LEVEL_TEST_CMD


class Parser(argclass.Parser):
    bot_token: str = argclass.Secret(env_var='BOT_TOKEN')


def main():
    args = Parser().parse_args()

    app = ApplicationBuilder().token(args.bot_token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(Regex(LEVEL_TEST_CMD), get_level_testers))
    app.run_polling()


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
        level=logging.INFO
    )

    main()
