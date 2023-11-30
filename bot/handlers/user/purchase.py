from aiogram import types, Router, Bot, F
from aiogram.filters import Command, Text
from aiogram.utils.markdown import text

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from database.methods.get import get_user_with_id
from database.methods.update import update_user_data

from bot.keyboards import purchase_menu

from utils.payment_request import payment_request
from utils.payment_details import payment_details

from utils.load_json_config import load_json_config
from utils.retrieve_percent import retrieve_percent

from config import ADMIN


PERCENT = 20

data = load_json_config()
order = data["order"]

router = Router()


class OrderState(StatesGroup):
    enter_nickname = State()
    pay_crypto = State()


purchase_text = {
    "ru": text(
        "Итак, здесь вы можете оплатить подписку криптовалютой.\n",
        "Выберите нужный вариант ниже.",
        sep="\n",
    ),
    "en": text(
        "Welp, here you may pay for the subscription with crypto-currency.\n",
        "Choose needed option below.",
        sep="\n",
    ),
}


@router.message(F.text == "Приобрести подписку")
@router.message(F.text == "Pay subscription")
async def purchase(message: types.Message, state: FSMContext):
    await state.clear()

    lang = get_user_with_id(message.from_user.id).language

    await message.answer(
        text=purchase_text[lang], reply_markup=purchase_menu.inline_kb_1[lang]
    )


@router.callback_query(Text(startswith="order_"))
async def ask_nickname(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_with_id(callback.from_user.id).language

    nick_text = {
        "ru": text("Хорошо, теперь введите свой никнейм на нашем сервисе"),
        "en": text("Okay, enter your nickname on the service"),
    }

    await callback.message.edit_text(
        text=nick_text[lang],
        reply_markup=purchase_menu.inline_kb_2[lang],
    )

    await state.update_data(order=callback.data)
    await state.set_state(OrderState.enter_nickname)


@router.message(OrderState.enter_nickname)
async def ask_if_correct(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await message.delete()

    lang = get_user_with_id(message.from_user.id).language

    ask_nick_text = {
        "ru": text(f"Ваш никнейм {message.text}? Если нет, введите еще раз"),
        "en": text(f"Is your nickname {message.text}? If it isn't, enter again"),
    }

    await message.answer(
        text=ask_nick_text[lang],
        reply_markup=purchase_menu.inline_kb_3[lang],
    )


@router.callback_query(OrderState.enter_nickname, Text("okey_nickname"))
async def pay_order(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.pay_crypto)
    data = await state.get_data()

    lang = get_user_with_id(callback.from_user.id).language

    price = order[data["order"]]["price"]

    await state.update_data(price=price)

    payment_data = payment_request(price, lang)
    await state.update_data(track_id=payment_data["trackId"])

    inline_kb_4 = {
        "ru": InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Оплатить", url=payment_data["payLink"]),
                    InlineKeyboardButton(text="Проверить", callback_data="check"),
                ],
            ]
        ),
        "en": InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Pay", url=payment_data["payLink"]),
                    InlineKeyboardButton(text="Check", callback_data="check"),
                ],
            ]
        ),
    }

    pay_text = {
        "ru": text(
            "Отлично, теперь оплатите криптовалютой нажав на кнопку, а затем нажмите <b>Проверить</b>. Не подтверждайте оплату пока не оплатите всю сумму указанную на данной странице! Т.е. если указана сумма 142.13, необходимо оплатить 142.13 неважно сколькими попытками, но только тогда подтверждать."
        ),
        "en": text(
            "That's excellent, now pay with crypto-currency clicking on button, and then click <b>Check</b>. Don't confirm payment until you pay all the count specified on following page! Thus if there is 142.13 count, you should pay 142.13 and it doesn't matter how much times with, but only then you confirm."
        ),
    }

    await callback.message.edit_text(
        text=pay_text[lang],
        reply_markup=inline_kb_4[lang],
    )


@router.callback_query(OrderState.pay_crypto, Text("check"))
async def check_payment(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()

    lang = get_user_with_id(callback.from_user.id).language

    order = payment_details(data["track_id"], lang)

    thanks_text = {
        "ru": text("Спасибо за покупку, мы отправили ваш запрос!"),
        "en": text("Thank for purchase, we sent your request!"),
    }

    if order["status"] == "Paid":
        await callback.message.edit_text(
            text=thanks_text[lang],
            reply_markup=purchase_menu.inline_kb_4[lang],
        )

        subscription = data["order"].split("_")[1]

        user = get_user_with_id(callback.from_user.id)

        update_user_data(user.user_id, subscription=int(subscription))

        try:
            if user.referrer_id:
                update_user_data(
                    user.referrer_id,
                    balance=retrieve_percent(f"{data['price']}*{PERCENT}%"),
                )
        except:
            pass

        await bot.send_message(
            chat_id=ADMIN,
            text=f"Пользователь @{callback.from_user.username} оплатил {subscription}-й тип подписки. Никнейм {data['nickname']}",
        )
        await state.clear()
    else:
        sorry_text = {
            "ru": text("Извините, вы не оплатили покупку :("),
            "en": text("Sorry, you haven't pay :("),
        }
        await callback.answer(text=sorry_text[lang], show_alert=True)


help_purchase_text = {
    "ru": text(
        "Чтобы приобрести подписку на индикатор, необходимо выбрать нужный вам срок подписки,",
        "а также ввести ваш никнейм на нашем сервисе, затем оплатить криптовалютой.",
        sep="\n",
    ),
    "en": text(
        "To purchase the subscription, it is necessary to choose needed subscription term,",
        "and then enter your nickname on our service, and then pay with crypto-currency.",
        sep="\n",
    ),
}


@router.callback_query(Text("help_purchase"))
async def purchase_help(callback: types.CallbackQuery):
    lang = get_user_with_id(callback.from_user.id).language

    await callback.message.edit_text(
        text=help_purchase_text[lang], reply_markup=purchase_menu.inline_kb_2[lang]
    )


@router.callback_query(Text("back_purchase"))
async def purchase_back(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_with_id(callback.from_user.id).language

    await callback.message.edit_text(
        text=purchase_text[lang], reply_markup=purchase_menu.inline_kb_1[lang]
    )
