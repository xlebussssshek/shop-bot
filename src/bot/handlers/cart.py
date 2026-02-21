from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.bot.keyboards import cart_keyboard
from src.db.repo import Repo

router = Router()


def _cart_text(items) -> str:
    if not items:
        return 'Корзина пуста.'
    total = sum(i['price'] * i['quantity'] for i in items)
    lines = ['🛒 Ваша корзина:']
    for item in items:
        lines.append(f"- {item['name']} x{item['quantity']} = {item['price'] * item['quantity']} ₽")
    lines.append(f'\nИтого: {total} ₽')
    return '\n'.join(lines)


async def _render_cart(call: CallbackQuery, repo: Repo):
    items = await repo.get_cart(call.from_user.id)
    await call.message.edit_text(_cart_text(items), reply_markup=cart_keyboard(items))


@router.callback_query(F.data == 'menu:cart')
async def show_cart(call: CallbackQuery, repo: Repo):
    await _render_cart(call, repo)
    await call.answer()


@router.callback_query(F.data.startswith('cart:add:'))
async def add_to_cart(call: CallbackQuery, repo: Repo):
    product_id = int(call.data.split(':')[2])
    await repo.add_to_cart(call.from_user.id, product_id, 1)
    await call.answer('Добавлено в корзину')


@router.callback_query(F.data.startswith('cart:plus:'))
async def plus_item(call: CallbackQuery, repo: Repo):
    product_id = int(call.data.split(':')[2])
    await repo.change_cart_quantity(call.from_user.id, product_id, 1)
    await _render_cart(call, repo)
    await call.answer()


@router.callback_query(F.data.startswith('cart:minus:'))
async def minus_item(call: CallbackQuery, repo: Repo):
    product_id = int(call.data.split(':')[2])
    await repo.change_cart_quantity(call.from_user.id, product_id, -1)
    await _render_cart(call, repo)
    await call.answer()


@router.callback_query(F.data.startswith('cart:remove:'))
async def remove_item(call: CallbackQuery, repo: Repo):
    product_id = int(call.data.split(':')[2])
    await repo.remove_cart_item(call.from_user.id, product_id)
    await _render_cart(call, repo)
    await call.answer()


@router.callback_query(F.data == 'cart:clear')
async def clear_cart(call: CallbackQuery, repo: Repo):
    await repo.clear_cart(call.from_user.id)
    await _render_cart(call, repo)
    await call.answer('Корзина очищена')
