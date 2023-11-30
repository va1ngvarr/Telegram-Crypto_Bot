from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


inline_kb_1 = {
    "ru": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вывести средства", callback_data="withdraw"),
                InlineKeyboardButton(text="Помощь", callback_data="help_referral"),
            ],
        ]
    ),
    "en": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Withdraw", callback_data="withdraw"),
                InlineKeyboardButton(text="Help", callback_data="help_referral"),
            ],
        ]
    ),
}

inline_kb_2 = {
    "ru": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Назад", callback_data="back_referral"),
            ],
        ]
    ),
    "en": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Back", callback_data="back_referral"),
            ],
        ]
    ),
}

inline_kb_3 = {
    "ru": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data="okey_wallet"),
                InlineKeyboardButton(text="Назад", callback_data="back_referral"),
            ],
        ]
    ),
    "en": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Yes", callback_data="okey_wallet"),
                InlineKeyboardButton(text="Back", callback_data="back_referral"),
            ],
        ]
    ),
}
