# ~/inventory_service/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ... other configurations ...
    MYSQL_HOST = 'db'
    MYSQL_USER = 'flaskuser'
    MYSQL_PASSWORD = 'flaskpassword'
    MYSQL_DB = 'inventory'
    MYSQL_CURSORCLASS = 'DictCursor'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_for_dev'
    MYSQL_CUSTOM_OPTIONS = {"charset": "utf8mb4"}
    # ... other configurations ...
