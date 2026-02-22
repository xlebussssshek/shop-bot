from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.states import CheckoutState
from src.config import Settings
from src.db.repo import Repo
from src.services.notify_service import notify_admins
from src.services.order_service import admin_order_text, order_confirmation_text
from src.utils.validators import is_valid_phone

router = Router()


@router.callback_query(F.data.in_({'menu:checkout', 'order:start'}))
async def start_checkout(call: CallbackQuery, state: FSMContext, repo: Repo):
    items = await repo.get_cart(call.from_user.id)
    if not items:
        await call.answer('Корзина пуста', show_alert=True)
        return
    await state.set_state(CheckoutState.name)
    await call.message.answer('Введите ваше имя:')
    await call.answer()


@router.message(CheckoutState.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(CheckoutState.phone)
    await message.answer('Введите телефон (например, +79991234567):')


@router.message(CheckoutState.phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not is_valid_phone(phone):
        await message.answer('Некорректный телефон, попробуйте еще раз.')
        return
    await state.update_data(phone=phone)
    await state.set_state(CheckoutState.address)
    await message.answer('Введите адрес доставки:')


@router.message(CheckoutState.address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    await state.set_state(CheckoutState.comment)
    await message.answer('Комментарий к заказу (или "-" если нет):')


@router.message(CheckoutState.comment)
async def get_comment(message: Message, state: FSMContext, repo: Repo, settings: Settings):
    data = await state.get_data()
    comment = message.text.strip()
    await state.clear()

    items = await repo.get_cart(message.from_user.id)
    if not items:
        await message.answer('Корзина пуста, заказ не создан.')
        return

    order_id = await repo.create_order(
        user_id=message.from_user.id,
        customer_name=data['name'],
        phone=data['phone'],
        address=data['address'],
        comment=comment,
        items=items,
    )
    order = await repo.get_order(order_id)

    await message.answer(order_confirmation_text(order_id))

    admin_text = admin_order_text(order, items)
    await notify_admins(message.bot, settings.admin_ids, admin_text, message.from_user.id, order_id)
