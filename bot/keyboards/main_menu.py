from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


reply_kb = {
    "ru": ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="Реферальная программа"),
                KeyboardButton(text="Приобрести подписку"),
            ],
            [
                KeyboardButton(text="Домой"),
            ],
        ],
    ),
    "en": ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="Referral program"),
                KeyboardButton(text="Pay subscription"),
            ],
            [
                KeyboardButton(text="Go home"),
            ],
        ],
    ),
}


inline_kb = {
    "ru": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Официальный канал", url="https://t.me/+39ry0lAMWBsyZTUy"
                )
            ],
            [InlineKeyboardButton(text="О нас", url="https://t.me/+39ry0lAMWBsyZTUy")],
            [InlineKeyboardButton(text="Поддержка", url="https://t.me/va1ngvarr")],
            [
                InlineKeyboardButton(text="🇷🇺Ru", callback_data="ru"),
                InlineKeyboardButton(text="🇺🇸En", callback_data="en"),
            ],
        ]
    ),
    "en": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Official channel", url="https://t.me/+39ry0lAMWBsyZTUy"
                )
            ],
            [
                InlineKeyboardButton(
                    text="About us", url="https://t.me/+39ry0lAMWBsyZTUy"
                )
            ],
            [InlineKeyboardButton(text="Support", url="https://t.me/va1ngvarr")],
            [
                InlineKeyboardButton(text="🇷🇺Ru", callback_data="ru"),
                InlineKeyboardButton(text="🇺🇸En", callback_data="en"),
            ],
        ]
    ),
}

inline_check_kb = {
    "ru": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подписаться", url="https://t.me/+39ry0lAMWBsyZTUy"
                )
            ],
        ]
    ),
    "en": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Subscribe", url="https://t.me/+39ry0lAMWBsyZTUy"
                )
            ],
        ]
    ),
}
