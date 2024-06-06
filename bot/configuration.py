import os
import sys

from dotenv import load_dotenv
from pathlib import Path


class ConfigureBot:
    def __init__(self, bot_config: str = 'config.yaml'):
        load_dotenv()
        try:
            self.bot_token = os.getenv("BOT_TOKEN")
            admin_ids_ = os.getenv("ADMIN_IDS").split()
            self.admin_ids = [int(admin_id) for admin_id in admin_ids_]
            self.logging_level = os.getenv("LOGGING_LEVEL").upper()
            self.opendata_api_key = os.getenv("OPENDATA_API_KEY")
            self.db_host = os.getenv("DB_HOST")
            self.db_port = os.getenv("DB_PORT")
            self.db_user = os.getenv("DB_USER")
            self.db_pass = os.getenv("DB_PASS")
            self.db_name = os.getenv("DB_NAME")
            self.db_uri_asyncpg = (f"postgresql+asyncpg://"
                                   f"{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}")
            self.reports_temp_folder = os.getenv("REPORTS_TEMP_FOLDER")
            self.reports_template = os.getenv("REPORTS_TEMPLATE")
            self.reports_template_dir = os.getenv("REPORTS_TEMPLATE_DIR")
            self.reports_template_file = os.getenv("REPORTS_TEMPLATE_FILE")
            self.reports_remote_url = os.getenv("REPORTS_REMOTE_URL")
            self.reports_remote_folder = os.getenv("REPORTS_REMOTE_FOLDER")
            self.reports_host = os.getenv("REPORTS_HOST")
            self.reports_user = os.getenv("REPORTS_USER")
            self.reports_user_pass = os.getenv("REPORTS_PASS")
            self.project_root = Path(sys.modules['__main__'].__file__).resolve().parents[0]
        except Exception as _ex:
            raise Exception(f"Can't init Bot! Check .env file! {repr(_ex)}")


bot_configuration = ConfigureBot()
