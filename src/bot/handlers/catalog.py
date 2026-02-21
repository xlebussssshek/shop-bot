from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.bot.keyboards import categories_keyboard, product_card_keyboard, products_keyboard
from src.db.repo import Repo
from src.services.catalog_service import product_card_text

router = Router()


@router.callback_query(F.data == 'menu:catalog')
async def catalog_menu(call: CallbackQuery, repo: Repo):
    categories = await repo.list_categories()
    if not categories:
        await call.message.edit_text('Каталог пуст. Обратитесь к администратору.')
    else:
        await call.message.edit_text('Категории:', reply_markup=categories_keyboard(categories))
    await call.answer()


@router.callback_query(F.data.startswith('cat:'))
async def category_products(call: CallbackQuery, repo: Repo):
    category_id = int(call.data.split(':')[1])
    products = await repo.list_products_by_category(category_id)
    if not products:
        await call.message.edit_text('В этой категории пока нет товаров.')
    else:
        await call.message.edit_text('Товары:', reply_markup=products_keyboard(products))
    await call.answer()


@router.callback_query(F.data.startswith('prod:'))
async def product_card(call: CallbackQuery, repo: Repo):
    product_id = int(call.data.split(':')[1])
    product = await repo.get_product(product_id)
    if not product:
        await call.answer('Товар не найден', show_alert=True)
        return

    await call.message.edit_text(product_card_text(product), reply_markup=product_card_keyboard(product_id))
    await call.answer()
