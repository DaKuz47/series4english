import logging

import argclass
from telegram.ext import (
    ApplicationBuilder,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
)
from telegram.ext.filters import Regex

from db.models import Genre, UserLevel
from handlers import (
    get_level_testers, search_series, start,
    choose_level, choose_genre,
    SearchState
)
from messages import LEVEL_TEST_CMD, SEARCH_SERIES_CMD


class Parser(argclass.Parser):
    bot_token: str = argclass.Secret(env_var='BOT_TOKEN')


def main():
    args = Parser().parse_args()

    app = ApplicationBuilder().token(args.bot_token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(Regex(LEVEL_TEST_CMD), get_level_testers))
    app.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Regex(SEARCH_SERIES_CMD), search_series)],
        states={
            SearchState.USER_LEVEL: [MessageHandler(Regex(UserLevel.regex()), choose_level)],
            SearchState.GENRE: [MessageHandler(Regex(Genre.regex()), choose_genre)],
        },
        fallbacks=[MessageHandler(Regex('cancel'), lambda x: ...)]
    ))
    app.run_polling()


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
        level=logging.INFO
    )

    main()
