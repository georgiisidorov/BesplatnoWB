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


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(query: PreCheckoutQuery):
	await dp.bot.answer_pre_checkout_query(
		pre_checkout_query_id=query.id, 
		ok=True
	)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, state: FSMContext):
	data = await state.get_data()
	amount = int(message.successful_payment.total_amount / 100)
	invoice_msgid = data.get('invoice_msgid')

	try:
		await dp.bot.delete_message(message.from_user.id, invoice_msgid)
	except Exception:
		pass
		
	pay_data = message.successful_payment.invoice_payload
	ads_amount = int(pay_data.split(';')[0].split(':')[1])
	email = message.successful_payment.order_info.email
	user = await db_commands.select_user_by_user_id(message.from_user.id)
	await db_commands.update_user_ads_amount(message.from_user.id, (user.ads_amount+ads_amount))
	await db_commands.update_user_email(message.from_user.id, email)
	await db_commands.add_transaction(message.from_user.id, email, amount, ads_amount)
		
	await message.answer(
		f'Количество доступных Вам новых публикаций увеличилось на <b>{ads_amount}</b>', 
		parse_mode='html', 
		reply_markup=inline_keyboards.backtomenu_keyboard
	)
