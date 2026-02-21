from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(slots=True)
class Settings:
    bot_token: str
    admin_ids: set[int]
    db_path: str



def _parse_admin_ids(raw: str) -> set[int]:
    result: set[int] = set()
    for item in raw.split(','):
        item = item.strip()
        if item:
            result.add(int(item))
    return result



def get_settings() -> Settings:
    token = os.getenv('BOT_TOKEN', '').strip()
    if not token:
        raise ValueError('BOT_TOKEN is not set')

    db_path = os.getenv('DB_PATH', 'data/shop_bot.db').strip()
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    admin_ids = _parse_admin_ids(os.getenv('ADMIN_IDS', ''))
    return Settings(bot_token=token, admin_ids=admin_ids, db_path=db_path)
