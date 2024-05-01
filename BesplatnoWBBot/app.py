import logging
import os

from aiogram import executor, types

from loader import bot, storage, scheduler, loop
import middlewares as middlewares
from handlers import dp


async def on_startup(dp):

	logging.basicConfig(format=u'[%(asctime)s] [%(filename)s - LINE:%(lineno)d] %(message)s',
						level=logging.DEBUG,
						handlers=([
							logging.StreamHandler(),
							logging.FileHandler("logging_debug.log", encoding='utf-8'),

						]))
	
	await dp.bot.set_my_commands(
		[
			types.BotCommand('start', 'Запустить бота')
		]
	)
	await dp.storage.reset_all()

	post_ads_10_minutes()
	middlewares.setup(dp)


async def on_shutdown(dp):
	await bot.close()
	await storage.close()


if __name__ == '__main__':
	executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)