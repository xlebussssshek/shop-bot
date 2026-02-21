from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards import admin_panel_keyboard
from src.config import Settings
from src.db.repo import Repo
from src.utils.security import is_admin

router = Router()


def _deny() -> str:
    return 'Доступ запрещен.'


@router.message(Command('admin'))
async def admin_cmd(message: Message, settings: Settings):
    if not is_admin(message.from_user.id, settings.admin_ids):
        await message.answer(_deny())
        return
    await message.answer('Админ-панель', reply_markup=admin_panel_keyboard())


@router.callback_query(F.data == 'admin:panel')
async def admin_panel(call: CallbackQuery, settings: Settings):
    if not is_admin(call.from_user.id, settings.admin_ids):
        await call.answer(_deny(), show_alert=True)
        return
    await call.message.edit_text('Админ-панель', reply_markup=admin_panel_keyboard())
    await call.answer()


@router.callback_query(F.data == 'admin:categories')
async def categories_info(call: CallbackQuery, settings: Settings, repo: Repo):
    if not is_admin(call.from_user.id, settings.admin_ids):
        await call.answer(_deny(), show_alert=True)
        return

    categories = await repo.list_categories()
    lines = ['Категории:'] + [f"{c['id']}: {c['name']}" for c in categories]
    lines += [
        '',
        'Команды:',
        '/cat_add Название',
        '/cat_rename ID|НовоеНазвание',
        '/cat_del ID',
    ]
    await call.message.answer('\n'.join(lines))
    await call.answer()


@router.callback_query(F.data == 'admin:products')
async def products_info(call: CallbackQuery, settings: Settings, repo: Repo):
    if not is_admin(call.from_user.id, settings.admin_ids):
        await call.answer(_deny(), show_alert=True)
        return

    products = await repo.list_all_products()
    lines = ['Товары:']
    for p in products[:20]:
        lines.append(f"{p['id']}: [{p['category_name']}] {p['name']} - {p['price']} ₽ | in_stock={p['in_stock']}")
    lines += [
        '',
        'Команды:',
        '/prod_add cat_id|Название|Описание|Цена',
        '/prod_edit id|Название|Описание|Цена|0/1',
        '/prod_del id',
        '/prod_stock id|0/1',
    ]
    await call.message.answer('\n'.join(lines))
    await call.answer()


@router.callback_query(F.data == 'admin:orders')
async def orders_info(call: CallbackQuery, settings: Settings, repo: Repo):
    if not is_admin(call.from_user.id, settings.admin_ids):
        await call.answer(_deny(), show_alert=True)
        return
    orders = await repo.list_recent_orders(10)
    if not orders:
        await call.message.answer('Заказов пока нет.')
    else:
        lines = ['Последние 10 заказов:']
        for o in orders:
            lines.append(f"#{o['id']} | {o['customer_name']} | {o['phone']} | {o['total_amount']} ₽ | {o['status']}")
        await call.message.answer('\n'.join(lines))
    await call.answer()


@router.callback_query(F.data.startswith('admin:done:'))
async def mark_done(call: CallbackQuery, settings: Settings, repo: Repo):
    if not is_admin(call.from_user.id, settings.admin_ids):
        await call.answer(_deny(), show_alert=True)
        return
    order_id = int(call.data.split(':')[2])
    await repo.set_order_status(order_id, 'processed')
    await call.answer('Заказ помечен обработанным')


@router.message(Command('cat_add'))
async def cat_add(message: Message, settings: Settings, repo: Repo):
    if not is_admin(message.from_user.id, settings.admin_ids):
        await message.answer(_deny())
        return
    name = message.text.replace('/cat_add', '', 1).strip()
    if not name:
        await message.answer('Использование: /cat_add Название')
        return
    await repo.add_category(name)
    await message.answer('Категория добавлена.')


@router.message(Command('cat_rename'))
async def cat_rename(message: Message, settings: Settings, repo: Repo):
    if not is_admin(message.from_user.id, settings.admin_ids):
        await message.answer(_deny())
        return
    raw = message.text.replace('/cat_rename', '', 1).strip()
    if '|' not in raw:
        await message.answer('Использование: /cat_rename ID|НовоеНазвание')
        return
    cid, name = raw.split('|', 1)
    await repo.rename_category(int(cid.strip()), name.strip())
    await message.answer('Категория переименована.')


@router.message(Command('cat_del'))
async def cat_del(message: Message, settings: Settings, repo: Repo):
    if not is_admin(message.from_user.id, settings.admin_ids):
        await message.answer(_deny())
        return
    cid = message.text.replace('/cat_del', '', 1).strip()
    await repo.delete_category(int(cid))
    await message.answer('Категория удалена.')


@router.message(Command('prod_add'))
async def prod_add(message: Message, settings: Settings, repo: Repo):
    if not is_admin(message.from_user.id, settings.admin_ids):
        await message.answer(_deny())
        return
    raw = message.text.replace('/prod_add', '', 1).strip()
    parts = [p.strip() for p in raw.split('|')]
    if len(parts) != 4:
        await message.answer('Использование: /prod_add cat_id|Название|Описание|Цена')
        return
    cid, name, desc, price = parts
    await repo.add_product(int(cid), name, desc, float(price), True)
    await message.answer('Товар добавлен.')


@router.message(Command('prod_edit'))
async def prod_edit(message: Message, settings: Settings, repo: Repo):
    if not is_admin(message.from_user.id, settings.admin_ids):
        await message.answer(_deny())
        return
    raw = message.text.replace('/prod_edit', '', 1).strip()
    parts = [p.strip() for p in raw.split('|')]
    if len(parts) != 5:
        await message.answer('Использование: /prod_edit id|Название|Описание|Цена|0/1')
        return
    pid, name, desc, price, stock = parts
    await repo.update_product(int(pid), name, desc, float(price), bool(int(stock)))
    await message.answer('Товар обновлен.')


@router.message(Command('prod_del'))
async def prod_del(message: Message, settings: Settings, repo: Repo):
    if not is_admin(message.from_user.id, settings.admin_ids):
        await message.answer(_deny())
        return
    pid = message.text.replace('/prod_del', '', 1).strip()
    await repo.delete_product(int(pid))
    await message.answer('Товар удален.')


@router.message(Command('prod_stock'))
async def prod_stock(message: Message, settings: Settings, repo: Repo):
    if not is_admin(message.from_user.id, settings.admin_ids):
        await message.answer(_deny())
        return
    raw = message.text.replace('/prod_stock', '', 1).strip()
    if '|' not in raw:
        await message.answer('Использование: /prod_stock id|0/1')
        return
    pid, stock = raw.split('|', 1)
    await repo.set_product_stock(int(pid.strip()), bool(int(stock.strip())))
    await message.answer('Статус наличия обновлен.')
