import datetime
import logging
import uuid
import json

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, SuccessfulPayment, CallbackQuery, ContentType, MediaGroup, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, PreCheckoutQuery
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, BadRequest
import asyncio

import config
from keyboards import inline_keyboards
from loader import dp
from states.states import States
from services import db_commands
from django.utils import timezone



def provider_data_toJSON(sumq):
	provider_data = {
		"InvoiceId": str(uuid.uuid4()),
		"Receipt": {
			"sno": "usn_income_outcome",
			"items": [
				{
					"name": "Создание и размещение текстового контента",
					"quantity": 1,
					"sum": sumq,
					"payment_method": "full_payment",
					"payment_object": "service",
					"tax": "none"
				}
			]
		}
	}

	return json.dumps(
		provider_data,
		indent=4
	)


# ----------------------------- З А П Л А Н И Р О В А Н Н Ы Е ----------------------------


@dp.callback_query_handler(text='planned')
async def planned_ads(call: CallbackQuery, state: FSMContext):
	await call.message.delete()
	ads = await db_commands.select_ads_by_user_id(call.from_user.id)
	
	msg_ids = []

	for ad in ads:
		now = timezone.now()
		datetime_ad = ad.datetime_publication
		if now < datetime_ad and ad.accepted == True:
			msg = await call.message.answer(
				f'👇 Это объявление запланировано на <b>{(ad.datetime_publication+datetime.timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")}</b>',
				parse_mode='html'
			)
			await asyncio.sleep(0.5)
			msg2 = await call.message.answer_photo(
				photo=ad.photo,
				caption=ad.text,
				parse_mode='html'
			)
			await asyncio.sleep(0.5)
			msg_ids.append(msg.message_id)
			msg_ids.append(msg2.message_id)

	if msg_ids == []:
		msg_return = await call.message.answer(
			'Запланированных объявлений пока что нет',
			reply_markup=inline_keyboards.return_to_my_ads_keyboard
			)
	else:
		msg_return = await call.message.answer(
			'Вернуться назад',
			reply_markup=inline_keyboards.return_to_my_ads_keyboard
			)

	await state.update_data(msg_ids=msg_ids)







