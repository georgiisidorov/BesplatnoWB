from services import db_commands
import datetime
from django.utils import timezone
import config
from handlers import dp


async def post_ads():
	now = datetime.datetime.now()+datetime.timedelta(hours=3)
	time = datetime.datetime(now.date().year, now.date().month, now.date().day, now.time().hour, now.time().minute)

	ad = await db_commands.select_ad_by_date_and_time(time)
	if ad != None:			
		if ad.accepted:
			await dp.bot.send_photo(
				chat_id=config.chats_subscribed[0],
				photo=ad.photo,
				caption=ad.text,
				parse_mode='html'
			)
			await db_commands.update_ad_publicated(ad.id)
	else:
		pass

