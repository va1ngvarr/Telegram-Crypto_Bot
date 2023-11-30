from aiogram import Dispatcher

from . import start, referral, purchase


def register_user_handlers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(referral.router)
    dp.include_router(purchase.router)
