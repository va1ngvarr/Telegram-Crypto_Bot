from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from utils.load_json_config import load_json_config


data = load_json_config()
order = data["order"]


inline_kb_1 = {
    "ru": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{order['order_1']['price']} USDT / {order['order_1']['term_en']}",
                    callback_data="order_1",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"{order['order_2']['price']} USDT / {order['order_2']['term_ru']}",
                    callback_data="order_2",
                ),
                InlineKeyboardButton(
                    text=f"{order['order_3']['price']} USDT / {order['order_3']['term_ru']}",
                    callback_data="order_3",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"{order['order_4']['price']} USDT / {order['order_4']['term_ru']}",
                    callback_data="order_4",
                ),
                InlineKeyboardButton(
                    text=f"{order['order_5']['price']} USDT / {order['order_5']['term_ru']}",
                    callback_data="order_5",
                ),
            ],
            [
                InlineKeyboardButton(text="Помощь", callback_data="help_purchase"),
            ],
        ]
    ),
    "en": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{order['order_1']['price']} USDT / {order['order_1']['term_en']}",
                    callback_data="order_1",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"{order['order_2']['price']} USDT / {order['order_2']['term_en']}",
                    callback_data="order_2",
                ),
                InlineKeyboardButton(
                    text=f"{order['order_3']['price']} USDT / {order['order_3']['term_en']}",
                    callback_data="order_3",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"{order['order_4']['price']} USDT / {order['order_4']['term_en']}",
                    callback_data="order_4",
                ),
                InlineKeyboardButton(
                    text=f"{order['order_5']['price']} USDT / {order['order_5']['term_en']}",
                    callback_data="order_5",
                ),
            ],
            [
                InlineKeyboardButton(text="Help", callback_data="help_purchase"),
            ],
        ]
    ),
}

inline_kb_2 = {
    "ru": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Назад", callback_data="back_purchase"),
            ],
        ]
    ),
    "en": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Back", callback_data="back_purchase"),
            ],
        ]
    ),
}

inline_kb_3 = {
    "ru": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data="okey_nickname"),
                InlineKeyboardButton(text="Назад", callback_data="back_purchase"),
            ],
        ]
    ),
    "en": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Yes", callback_data="okey_nickname"),
                InlineKeyboardButton(text="Back", callback_data="back_purchase"),
            ],
        ]
    ),
}

inline_kb_4 = {
    "ru": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Инструкция",
                    url="https://t.me/+39ry0lAMWBsyZTUy",
                )
            ],
        ]
    ),
    "en": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="How to use",
                    url="https://t.me/+39ry0lAMWBsyZTUy",
                )
            ],
        ]
    ),
}
