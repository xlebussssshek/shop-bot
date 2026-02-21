from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.bot.texts import CONTACT_TEXT, FAQ_TEXT

router = Router()


@router.callback_query(F.data == 'menu:faq')
async def faq(call: CallbackQuery):
    await call.message.edit_text(FAQ_TEXT)
    await call.answer()


@router.callback_query(F.data == 'menu:contact')
async def contact(call: CallbackQuery):
    await call.message.edit_text(CONTACT_TEXT)
    await call.answer()
