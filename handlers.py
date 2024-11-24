from enum import Enum, auto
import logging

from sqlalchemy import select

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, helpers
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from db import Session
from db.models import Genre, LevelTest, UserLevel, Series
from messages import (
    CHOOSE_LEVEL,
    CHOOSE_GENRE,
    GREETINGS,
    LEVEL_TEST_CMD,
    LEVEL_TEST_TEMPLATE,
    LEVEL_TESTS_LIST_TEMPLATE,
    SEARCH_SERIES_CMD,
    SERIES_TEMPLATE,
    SERIES_LIST_TEMPLATE,
    EMPTY_SERIES_LIST
)
from utils import make_keyboard


log = logging.getLogger(__name__)


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


class SearchState(Enum):
    USER_LEVEL = auto()
    GENRE = auto()


async def search_series(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=CHOOSE_LEVEL,
        reply_markup=make_keyboard(iter(UserLevel), row_size=3)
    )

    return SearchState.USER_LEVEL


async def choose_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    level = update.message.text
    log.info('User %s choose level %s', update.effective_user.name, level)

    context.user_data['level'] = level

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=CHOOSE_GENRE,
        reply_markup=make_keyboard(
            (genre.with_smile() for genre in Genre),
            row_size=3
        )
    )

    return SearchState.GENRE


async def choose_genre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    genre = Genre.rm_smile(update.message.text)
    log.info('User %s choose genre %s', update.effective_user.name, genre)

    with Session() as session:
        series = [
            row
            for row in session.scalars(
                select(Series).
                where(Series.genre.like(f'%{genre}%')).
                where(Series.difficulty == context.user_data['level'])
            )
        ]

    for serie in series:
        message = SERIES_TEMPLATE.format(
            name=helpers.escape_markdown(
                serie.name, version=2, entity_type=ParseMode.MARKDOWN_V2,
            ),
            genres=serie.genre,
            years=helpers.escape_markdown(
                serie.published_years, version=2, entity_type=ParseMode.MARKDOWN_V2,
            ),
            n_series=serie.n_series
        )

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=serie.cover_url,
            caption=message,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=ReplyKeyboardMarkup(
                [[SEARCH_SERIES_CMD],
                [LEVEL_TEST_CMD]],
                one_time_keyboard=False,
                resize_keyboard=True
            )
        )

    return ConversationHandler.END
