import os
from functools import cache

from dotenv import load_dotenv

load_dotenv()


__all__ = ("settings")


@cache
class Settings:
    def __init__(self):
        self.update_interval = os.getenv("RECORDING_INTERVAL", 1000)
        self.db_uri = os.getenv("DB_URI", "sqlite:///system_data.db")
        self.test_db_uri = os.getenv("TEST_DB_URI", "sqlite:///:memory:")


settings = Settings()