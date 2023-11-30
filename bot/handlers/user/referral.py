from aiogram import types, Router, Bot, F
from aiogram.filters import Command, Text

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.utils.markdown import text

from bot.keyboards import referral_menu

from database.methods.update import update_user_data
from database.methods.get import get_user_with_id, get_users_with_referrer

from config import ADMIN


router = Router()


class WithdrawState(StatesGroup):
    enter_wallet = State()


async def answer(message: types.Message, bot: Bot, user_id: int) -> str:
    bot_me = await bot.get_me()
    bot_name = bot_me.username
    ref_code = str(user_id)

    ref_link = f"https://t.me/{bot_name}?start={ref_code}"

    user = get_user_with_id(user_id)

    balance = user.balance

    users_with_this_referrer = get_users_with_referrer(user_id)
    potential_ref = len(users_with_this_referrer)

    users_who_subscribed = []

    for user in users_with_this_referrer:
        if user.subscription:
            users_who_subscribed.append(user)

    validated_ref = len(users_who_subscribed)

    referral_text = {
        "ru": text(
            "Это меню для управления реферальной программой!\n",
            f"Ваша реферальная ссылка: {ref_link}\n",
            f"Ваш баланс: {balance} USDT\n",
            f"Перешло по ссылке: {potential_ref}",
            f"Количество рефералов: {validated_ref}",
            sep="\n",
        ),
        "en": text(
            "This is menu to manage the referral program!\n",
            f"Your referral link: {ref_link}\n",
            f"Your balance: {balance} USDT\n",
            f"Followed the link: {potential_ref}",
            f"Referral amount: {validated_ref}",
            sep="\n",
        ),
    }

    return referral_text


@router.message(F.text == "Реферальная программа")
@router.message(F.text == "Referral program")
async def referral(message: types.Message, state: FSMContext, bot: Bot):
    await state.clear()

    user_id = message.from_user.id
    referral_text = await answer(message, bot, user_id)

    lang = get_user_with_id(user_id).language

    await message.answer(
        text=referral_text[lang], reply_markup=referral_menu.inline_kb_1[lang]
    )


@router.callback_query(Text("withdraw"))
async def ask_wallet(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_with_id(callback.from_user.id).language

    withdraw_text = {
        "ru": text(
            "Хорошо, теперь введите свой крипто-кошелек и если надо укажите блокчейн-сеть, такую как TRC-20. Если вы что-то неправильно укажите деньги могут не придти!",
        ),
        "en": text(
            "Great, then enter your crypto-wallet and if there is blockchain-network, specify it, like TRC-20. If you enter something wrong, money may be unable to arrive!",
        ),
    }

    await callback.message.edit_text(
        text=withdraw_text[lang],
        reply_markup=referral_menu.inline_kb_2[lang],
    )

    await state.set_state(WithdrawState.enter_wallet)


@router.message(WithdrawState.enter_wallet)
async def ask_if_correct(message: types.Message, state: FSMContext):
    await state.update_data(wallet=message.text)
    await message.delete()

    lang = get_user_with_id(message.from_user.id).language

    wallet_text = {
        "ru": text(
            f"Ваш крипто-кошелек {message.text}? Если не так, то введите еще раз"
        ),
        "en": text(
            f"Is your crypto-wallet {message.text}? Whether it isn't, enter again"
        ),
    }

    await message.answer(
        text=wallet_text[lang],
        reply_markup=referral_menu.inline_kb_3[lang],
    )


@router.callback_query(WithdrawState.enter_wallet, Text("okey_wallet"))
async def send_petition(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()

    user = get_user_with_id(callback.from_user.id)

    lang = user.language
    balance = user.balance

    if balance > 0.0:
        update_user_data(user.user_id, balance=0.0)

        await bot.send_message(
            chat_id=ADMIN,
            text=f"Пользователь @{callback.from_user.username} хочет вывести {balance} USDT на крипто-кошелек {data['wallet']}",
        )
        ok_withdraw_text = {
            "ru": text(
                "Отлично, мы отправили заявку на вывод! Ждите поступления средств"
            ),
            "en": text(
                "That's excellent, we sent request! Wait for the funds to arrive"
            ),
        }
        await callback.message.edit_text(text=ok_withdraw_text[lang])
    else:
        null_balance_text = {
            "ru": text("Нельзя вывести нулевой баланс..."),
            "en": text("You can't withdraw empty balance..."),
        }
        await callback.message.edit_text(text=null_balance_text[lang])

    await state.clear()


help_referral_text = {
    "ru": text(
        "Чтобы участвовать в реферальной программе и зарабатывать на этом деньги,",
        "необходимо скопировать вашу реферальную ссылку и распространять там, где вы хотите.\n",
        "Когда человек перешел по вашей ссылке, то он еще не совсем реферал. Чтобы он стал",
        "вашим рефералом, он должен оплатить любую подписку.\n",
        "Вы получаете 20% на ваш счет от каждого платежа вашего реферала",
        "Затем вы можете отправить запрос на вывод средств, с указанием вашего крипто-кошелька.",
        sep="\n",
    ),
    "en": text(
        "To take part our referral program and make some money out of this you need to copy",
        "your referral link and propagate it there you would like to.\n",
        "When a person followed your link, it doesn't means that is your referral now.",
        "To become your referral, they should pay for any subscription.\n",
        "You retrieve 20% to your bill for everytime your referral paid.",
        "After you may send request to withdraw money, specifying your crypto-wallet.",
        sep="\n",
    ),
}


@router.callback_query(Text("help_referral"))
async def referral_help(callback: types.CallbackQuery):
    lang = get_user_with_id(callback.from_user.id).language

    await callback.message.edit_text(
        text=help_referral_text[lang], reply_markup=referral_menu.inline_kb_2[lang]
    )


@router.callback_query(Text("back_referral"))
async def referral_back(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()

    user_id = callback.from_user.id

    lang = get_user_with_id(user_id).language
    referral_text = await answer(callback.message, bot, user_id)

    await callback.message.edit_text(
        text=referral_text[lang], reply_markup=referral_menu.inline_kb_1[lang]
    )
