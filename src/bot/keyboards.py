from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard(is_admin: bool = False):
    kb = InlineKeyboardBuilder()
    kb.button(text='Каталог', callback_data='menu:catalog')
    kb.button(text='Корзина', callback_data='menu:cart')
    kb.button(text='FAQ', callback_data='menu:faq')
    kb.button(text='Оставить заказ', callback_data='menu:checkout')
    kb.button(text='Связаться', callback_data='menu:contact')
    if is_admin:
        kb.button(text='Админка', callback_data='admin:panel')
    kb.adjust(2, 2, 1)
    return kb.as_markup()


def categories_keyboard(categories):
    kb = InlineKeyboardBuilder()
    for cat in categories:
        kb.button(text=cat['name'], callback_data=f'cat:{cat["id"]}')
    kb.button(text='⬅️ Назад', callback_data='menu:main')
    kb.adjust(1)
    return kb.as_markup()


def products_keyboard(products):
    kb = InlineKeyboardBuilder()
    for p in products:
        stock = '✅' if p['in_stock'] else '❌'
        kb.button(text=f"{stock} {p['name']} ({p['price']} ₽)", callback_data=f'prod:{p["id"]}')
    kb.button(text='⬅️ Назад', callback_data='menu:catalog')
    kb.adjust(1)
    return kb.as_markup()


def product_card_keyboard(product_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text='+ В корзину', callback_data=f'cart:add:{product_id}')
    kb.button(text='Назад', callback_data='menu:catalog')
    kb.adjust(1)
    return kb.as_markup()


def cart_keyboard(items):
    kb = InlineKeyboardBuilder()
    for item in items:
        pid = item['product_id']
        kb.row(
            InlineKeyboardButton(text=f"➖ {item['name']}", callback_data=f'cart:minus:{pid}'),
            InlineKeyboardButton(text=f"➕ {item['quantity']}", callback_data=f'cart:plus:{pid}'),
            InlineKeyboardButton(text='🗑', callback_data=f'cart:remove:{pid}'),
        )
    kb.button(text='Очистить корзину', callback_data='cart:clear')
    kb.button(text='Оформить заказ', callback_data='order:start')
    kb.button(text='⬅️ В меню', callback_data='menu:main')
    kb.adjust(1)
    return kb.as_markup()


def admin_panel_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text='Категории', callback_data='admin:categories')
    kb.button(text='Товары', callback_data='admin:products')
    kb.button(text='Последние заказы', callback_data='admin:orders')
    kb.button(text='⬅️ В меню', callback_data='menu:main')
    kb.adjust(1)
    return kb.as_markup()


def order_notify_keyboard(user_id: int, order_id: int):
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text='Связаться', url=f'tg://user?id={user_id}'),
        InlineKeyboardButton(text='Пометить обработан', callback_data=f'admin:done:{order_id}'),
    )
    return kb.as_markup()
