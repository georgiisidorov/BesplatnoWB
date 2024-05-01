import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import asyncio


loop = asyncio.get_event_loop()
bot = Bot(
	token=os.getenv('BOT_TOKEN'), 
	parse_mode=types.ParseMode.HTML
)
storage = RedisStorage2(
	os.getenv('REDIS_HOST'),
	int(os.getenv('REDIS_PORT'))
)
dp = Dispatcher(bot, storage=storage)
