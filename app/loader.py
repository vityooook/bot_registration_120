# from loguru import logger
# from notifiers.logging import NotificationHandler
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config

# Set up notification handler to send errors to admin
param = {
    'token': config.BOT_TOKEN,
    'chat_id': config.ADMIN
}
# handler = NotificationHandler("telegram", defaults=param)
# logger.add(handler, level="ERROR")
#
# # Set up logging, declare the bot and dispatcher
# logger.add(
#     "logs/logs.log",
#     format="{time} {level} {message}",
#     level="INFO",
#     rotation="1 week",
#     compression="zip",
#     enqueue=True,
#     backtrace=False,
#     diagnose=False
# )
# Create a new memory storage object
storage = MemoryStorage()
# Create a new bot object with the specified token and parse mode
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
# Create a new dispatcher object with the specified storage
dp = Dispatcher(storage=storage)
