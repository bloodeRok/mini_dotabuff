import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("BOT_API_KEY", "")
PICTURES_PATH = os.path.join("constants", "pictures")
DOTABUFF_MAIN_PHOTO_PATH = os.path.join(PICTURES_PATH, "dotabuff_main.jpg")
DOTABUFF_URL_PHOTO_PATH = os.path.join(PICTURES_PATH, "dotabuff_URL.jpg")
DOTA_CLIENT_MAIN_PHOTO_PATH = os.path.join(
    PICTURES_PATH,
    "dota_client_main.jpg"
)
DOTA_CLIENT_WINDOW_PHOTO_PATH = os.path.join(
    PICTURES_PATH,
    "dota_client_window.jpg"
)
ADMIN_ACCOUNT = 190947906
