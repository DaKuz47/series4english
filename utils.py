import itertools
from typing import Iterable

from telegram import ReplyKeyboardMarkup


def make_keyboard(buttons: Iterable[str], row_size: int) -> ReplyKeyboardMarkup:
    buttons_iter = iter(buttons)
    buttons_per_row = list(itertools.islice(buttons_iter, row_size))

    layout = []
    while buttons_per_row:
        layout.append(buttons_per_row)
        buttons_per_row = list(itertools.islice(buttons_iter, row_size))

    return ReplyKeyboardMarkup(
        layout, resize_keyboard=True, one_time_keyboard=True
    )
