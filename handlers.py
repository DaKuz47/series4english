from sqlalchemy import select

from telegram import ReplyKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from db import Session
from db.models import LevelTest
from messages import (
    GREETINGS,
    LEVEL_TEST_CMD,
    LEVEL_TEST_TEMPLATE,
    LEVEL_TESTS_LIST_TEMPLATE,
    SEARCH_SERIES_CMD
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        update.effective_chat.id, GREETINGS, reply_markup=ReplyKeyboardMarkup(
            [[SEARCH_SERIES_CMD],
            [LEVEL_TEST_CMD]],
            one_time_keyboard=False,
            resize_keyboard=True
        )
    )


async def get_level_testers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with Session() as session:
        level_test_msgs = [
            LEVEL_TEST_TEMPLATE.format(
                name=row.resource_name,
                link=row.resource_link,
                desc=row.description
            )
            for row in session.scalars(select(LevelTest)).all()
        ]

    final_message = LEVEL_TESTS_LIST_TEMPLATE.format('\n\n'.join(
        f'{idx + 1}\. {msg}' for idx, msg in enumerate(level_test_msgs)
    ))
    await context.bot.send_message(
        update.effective_chat.id, final_message,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True
    )
