import datetime
import logging
import uuid
import json

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ContentType, MediaGroup, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, PreCheckoutQuery
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, BadRequest
import asyncio

import config
from keyboards import inline_keyboards
from loader import dp
from services import db_commands


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


@dp.callback_query_handler(text='tariffs')
async def tariffs(call: CallbackQuery, state: FSMContext):
	await call.answer()
	user = await db_commands.select_user_by_user_id(call.from_user.id)
	tariffs_keyboard = await inline_keyboards.tariffs()
	await call.message.edit_text(
		f'<b>📌 Количество доступных публикаций: {user.ads_amount}</b>',
		reply_markup=tariffs_keyboard,
		parse_mode='html'
	)


@dp.callback_query_handler(text_contains=';rub')
async def payment(call: CallbackQuery, state: FSMContext):
	price = int(call.data.split(';')[0])
	ads_amount = int(call.data.split(';')[1])
	await call.message.delete()

	user = await db_commands.select_user_by_user_id(call.from_user.id)
	email = 'abrakadabra@gmail.com'

	await db_commands.update_user_ads_amount(call.from_user.id, (user.ads_amount+ads_amount))
	await db_commands.update_user_email(call.from_user.id, email)
	await db_commands.add_transaction(call.from_user.id, email, price, ads_amount, datetime.datetime.now()+datetime.timedelta(hours=3))
		
	await call.message.answer(
		f'Количество доступных Вам новых публикаций увеличилось на <b>{ads_amount}</b>', 
		parse_mode='html', 
		reply_markup=inline_keyboards.backtomenu_keyboard
	)
