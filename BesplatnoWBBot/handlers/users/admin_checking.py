import datetime
import logging
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
from states.states import States
from services import db_commands
from django.utils import timezone




@dp.callback_query_handler(text_contains='accept_ad;')
async def accepting_ad(call: CallbackQuery, state: FSMContext):
	
	ad_id = call.data.split(';')[-1]
	msg_id = call.data.split(';')[-2]
	ad = await db_commands.select_ad_by_ad_id(int(ad_id))


	if ad.datetime_publication < datetime.datetime.now():
		await dp.bot.edit_message_text(
			chat_id=int(ad.user_id), 
			message_id=int(msg_id),
			text='Добавление объявления отменено',
			reply_markup=inline_keyboards.backtomenu_keyboard
		)
		await db_commands.delete_ad_by_ad_id(int(ad_id))
		await state.finish()

		await call.message.delete()
		await call.message.answer(
			'Добавление объявления отменено, не вовремя уже'
		)
	else:
		await call.message.delete()
		await call.message.answer(
			'Объявление одобрено!'
		)

		user = await db_commands.select_user_by_user_id(ad.user_id)

		await db_commands.update_ad_accepted(int(ad_id))
		await db_commands.update_user_ads_amount(ad.user_id, user.ads_amount-1)

		await asyncio.sleep(2)

		await dp.bot.edit_message_text(
			chat_id=int(ad.user_id), 
			message_id=int(msg_id),
			text='Объявление одобрено!',
			reply_markup=inline_keyboards.backtomenu_keyboard
		)


@dp.callback_query_handler(text_contains='edit_ad;')
async def editing_ad(call: CallbackQuery, state: FSMContext):
	
	ad_id = call.data.split(';')[-1]
	msg_id = call.data.split(';')[-2]

	await call.message.edit_reply_markup()

	msg = await call.message.answer(
		'Напишите комментарий к данному объявлению'
	)
	await state.update_data(msg_id=msg_id, msg_ids=[msg.message_id], ad_id=ad_id)
	await States.Comment.set()


@dp.message_handler(state=States.Comment)
async def commenting_ad(message: Message, state: FSMContext):
	data = await state.get_data()
	for msg_id in data.get('msg_ids'):
		await dp.bot.delete_message(message.from_user.id, msg_id)

	ad_id = int(data.get('ad_id'))
	msg_id_user = int(data.get('msg_id'))
	text = message.text

	ad = await db_commands.select_ad_by_ad_id(ad_id)
	await dp.bot.edit_message_text(
		chat_id=int(ad.user_id), 
		message_id=msg_id_user,
		text=f'Комментарий администратора:\n\n{text}', 
		reply_markup=inline_keyboards.edit_button
		)
	await db_commands.delete_ad_by_ad_id(ad_id)
	await state.finish()
	await message.answer('Комментарий отправлен')


@dp.callback_query_handler(text_contains='delete_ad;')
async def deleting_ad(call: CallbackQuery, state: FSMContext):
	ad_id = int(call.data.split(';')[-1])
	msg_id = int(call.data.split(';')[-2])
	await call.message.delete()

	ad = await db_commands.select_ad_by_ad_id(ad_id)
	await dp.bot.edit_message_text(
		chat_id=int(ad.user_id), 
		message_id=msg_id,
		text=f'Ваше объявление удалено без права на восстановление', 
		reply_markup=inline_keyboards.backtomenu_keyboard
		)
	await db_commands.delete_ad_by_ad_id(ad_id)
	await state.finish()
	await call.message.answer('Объявление удалено')