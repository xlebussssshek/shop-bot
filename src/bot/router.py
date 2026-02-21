from aiogram import Dispatcher

from src.bot.handlers import admin, cart, catalog, faq, order, start


def setup_routers(dp: Dispatcher) -> None:
    dp.include_router(start.router)
    dp.include_router(catalog.router)
    dp.include_router(cart.router)
    dp.include_router(order.router)
    dp.include_router(faq.router)
    dp.include_router(admin.router)
