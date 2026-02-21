import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.middlewares import ErrorLoggingMiddleware
from src.bot.router import setup_routers
from src.config import get_settings
from src.db.migrate import run_migrations
from src.db.repo import Repo
from src.logger import setup_logging


async def main() -> None:
    setup_logging()

    settings = get_settings()
    await run_migrations(settings.db_path)

    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    repo = Repo(settings.db_path)
    dp.update.middleware(ErrorLoggingMiddleware())
    dp['repo'] = repo
    dp['settings'] = settings

    setup_routers(dp)

    logging.info('Bot started')
    await dp.start_polling(bot, repo=repo, settings=settings)


if __name__ == '__main__':
    asyncio.run(main())
