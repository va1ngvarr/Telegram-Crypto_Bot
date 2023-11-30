from aiogram import types, Router, F
from aiogram.filters import CommandStart, Text
from aiogram.utils.markdown import text
from aiogram.fsm.context import FSMContext

from bot.keyboards import main_menu

from database.methods.create import add_new_user
from database.methods.get import get_user_with_id
from database.methods.update import update_user_data


router = Router()


def extract_unique_code(text):
    # Extract the unique code from the sent /start command.

    if text == "Домой" or text == "Go home":
        return None

    try:
        unique_code = text.split()[1]
    except IndexError:
        return None

    return int(unique_code)


@router.message(CommandStart())
@router.message(F.text == "Домой")
@router.message(F.text == "Go home")
async def start(message: types.Message, state: FSMContext):
    await state.clear()

    referrer_id = extract_unique_code(message.text)
    user_id = message.from_user.id

    user = get_user_with_id(user_id)

    lang = "en"

    if user != None:
        # if user exists

        lang = user.language

        welcome_text = {
            "ru": text(
                f"Как поживаешь, <i>{message.from_user.first_name}</i>? Давно не виделись!"
            ),
            "en": text(
                f"What's up, <i>{message.from_user.first_name}</i>? We were bored without you!"
            ),
        }
        if referrer_id:
            # if there is referer's id
            if referrer_id == user_id:
                # if referer's id is user's id
                link_text = {
                    "ru": text("Вы перешли по собственной реферальной ссылке"),
                    "en": text("You have followed your own referral link"),
                }
                await message.answer(text=link_text[lang])
        await message.answer(
            text=welcome_text[lang], reply_markup=main_menu.inline_kb[lang]
        )
    else:
        welcome_text = {
            "en": text(
                f"Welcome, <i>{message.from_user.first_name}</i>! This is <b>chat-bot</b>, where you may purchase access to our services",
                "choosing subscription type you need and proceeding with the cryptocurrency.\n",
                "Also we have referral program that earns you a percentage of sales.",
                sep="\n",
            )
        }
        add_new_user(user_id=user_id, referrer_id=referrer_id)

        if referrer_id:
            # if there is referer's id
            if referrer_id != user_id:
                link_text = {
                    "ru": text(
                        f"Вы перешли по реферальной ссылке пользователя с ID {referrer_id}"
                    ),
                    "en": text(
                        f"You have followed the referral link of user with ID {referrer_id}"
                    ),
                }
                await message.answer(text=link_text[lang])

        await message.answer(
            text=welcome_text[lang], reply_markup=main_menu.inline_kb[lang]
        )

    menu_text = {
        "ru": text("Используйте меню ниже для навигации"),
        "en": text("Use following the menu to navigate"),
    }
    await message.answer(
        text=menu_text[lang],
        reply_markup=main_menu.reply_kb[lang],
    )


@router.callback_query(Text("ru"))
async def set_russian(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    update_user_data(user_id, language="ru")

    change_text = text(f"Вы сменили язык интерфейса на <b>русский</b>!")

    await callback.message.answer(
        text=change_text, reply_markup=main_menu.reply_kb["ru"]
    )


@router.callback_query(Text("en"))
async def set_english(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    update_user_data(user_id, language="en")

    change_text = text(f"You have changed interface language to <b>english</b>!")

    await callback.message.answer(
        text=change_text, reply_markup=main_menu.reply_kb["en"]
    )
