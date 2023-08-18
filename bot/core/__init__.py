import logging
from .app import dp
from .handlers import send_welcome, get_user


logging.basicConfig(level=logging.INFO)
