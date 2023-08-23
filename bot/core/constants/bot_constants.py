import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("BOT_API_KEY", "")
PICTURES_PATH = os.environ.get("PICTURES_PATH", "")
