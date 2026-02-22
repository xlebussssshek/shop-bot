from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards import main_menu_keyboard
from src.bot.texts import MAIN_MENU
from src.config import Settings

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, settings: Settings):
    await message.answer(MAIN_MENU, reply_markup=main_menu_keyboard(message.from_user.id in settings.admin_ids))


@router.message(Command("id"))
async def cmd_id(message: Message):
    await message.answer(f"Ваш ID: {message.from_user.id}")


@router.callback_query(F.data == 'menu:main')
async def menu_main(call: CallbackQuery, settings: Settings):
    await call.message.edit_text(
        MAIN_MENU,
        reply_markup=main_menu_keyboard(call.from_user.id in settings.admin_ids),
    )
    await call.answer()
