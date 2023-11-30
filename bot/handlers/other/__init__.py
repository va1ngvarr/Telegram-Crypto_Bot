from aiogram import Dispatcher

from . import check_sub


def register_other_handlers(dp: Dispatcher):
    dp.include_router(check_sub.router)
