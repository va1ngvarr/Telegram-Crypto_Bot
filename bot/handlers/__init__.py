from aiogram import Dispatcher

from .user import register_user_handlers
from .other import register_other_handlers


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_user_handlers,
        register_other_handlers,
    )

    for handler in handlers:
        handler(dp)
