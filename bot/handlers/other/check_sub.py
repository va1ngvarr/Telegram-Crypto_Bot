from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Text
from aiogram.utils.markdown import text
from aiogram.fsm.context import FSMContext

from bot.keyboards import main_menu

from database.methods.create import add_new_user
from database.methods.get import get_user_with_id
from database.methods.update import update_user_data

import config


router = Router()


check_text = {
    "ru": text(
        "Необходимо, чтобы вы были подписаны на наш основной канал, где мы выкладываем новости о нашем проекте❤️\n",
        "Это необходимо для поддержки, развития бота, а так же нам важна ваша активность и заинтересованность.\n",
        "После подписки это сообщение не появится и не будет вам мешать☕️🍪",
        sep="\n",
    ),
    "en": text(
        "You need to be subscribed to our main channel, where we post news about our project❤️\n",
        "This is necessary for support, development of the bot, as well as your activity and interest.\n",
        "After subscribing, this message will not appear and will not affect you☕️🍪",
        sep="\n",
    ),
}


@router.message(F.text)
async def check_sub(message: types.Message, bot: Bot):
    sub = await bot.get_chat_member(config.CHECKED_CHAT_ID, message.from_user.id)

    if sub.status != "member":
        await message.answer(
            text=check_text,
            reply_markup=main_menu.inline_check_kb,
        )
