from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(slots=True)
class Settings:
    bot_token: str
    admin_ids: list[int]
    db_path: str

    @property
    def parsed_admin_ids(self) -> list[int]:
        return [int(x) for x in self.admin_ids]


def _parse_admin_ids(raw: str) -> list[int]:
    return [int(x.strip()) for x in raw.split(',') if x.strip().isdigit()]


def get_settings() -> Settings:
    token = os.getenv('BOT_TOKEN', '').strip()
    if not token:
        raise ValueError('BOT_TOKEN is not set')

    db_path = os.getenv('DB_PATH', 'data/shop_bot.db').strip()
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    admin_ids = _parse_admin_ids(os.getenv('ADMIN_IDS', ''))
    return Settings(bot_token=token, admin_ids=admin_ids, db_path=db_path)
