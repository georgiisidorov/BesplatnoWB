from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ContentType, MediaGroup, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, PreCheckoutQuery
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, BadRequest
import asyncio

import config
from data import texts
from keyboards import inline_keyboards
from loader import dp
from services import db_commands


@dp.callback_query_handler(text='neanunahui')
async def inactive_button(call: CallbackQuery, state: FSMContext):
	await call.answer()


@dp.callback_query_handler(text='faq')
async def faq(call: CallbackQuery, state: FSMContext):
	await call.message.edit_text(
		texts.msg_faq, 
		reply_markup=inline_keyboards.backtomenu_keyboard,
		parse_mode='html'
	)


@dp.callback_query_handler(text='menu')
async def menu(call: CallbackQuery, state: FSMContext):
	await call.answer()
	data = await state.get_data()
	msg_ids = data.get('msg_ids')
	if msg_ids is not None:
		for msg_id in msg_ids:
			await dp.bot.delete_message(call.from_user.id, msg_id)

	await state.finish()
	await state.update_data(msg_ids=[])
	user = await db_commands.select_user_by_user_id(call.from_user.id)
	if user.ads_amount > 0: 
		txet = '\n\nДля размещения поста нажмите «Новое объявление»\n\n'
	else: 
		txet = '\n\nДля пополнения счёта нажмите «Оплатить тариф»\n\n'
			
	await call.message.edit_text(
		f'Сейчас Вы находитесь в Вашем личном кабинете.\n\n'
		f'<b>📌 Количество доступных публикаций: {user.ads_amount}</b>'
		f'{txet}Если возникли вопросы, то нажмите FAQ ❓ или напишите в поддержку',
		reply_markup=inline_keyboards.menu_user,
		parse_mode='html'
	)


@dp.callback_query_handler(text='cancel')
async def cancelling(call: CallbackQuery, state: FSMContext):
	data = await state.get_data()
	msg_id = data.get('msg_id')
	await dp.bot.delete_message(call.from_user.id, msg_id)
	await call.message.edit_text(
		f'''Вы не подтвердили объявление :(''',
		reply_markup=inline_keyboards.edit_button
	)


@dp.callback_query_handler(text='return_to_my_ads')
async def returning_to_my_ads(call: CallbackQuery, state: FSMContext):
	data = await state.get_data()
	msg_ids = data.get('msg_ids')
	if msg_ids is not None:
		for msg_id in msg_ids:
			await dp.bot.delete_message(call.from_user.id, msg_id)

	await state.finish()
	await state.update_data(msg_ids=[])

	await call.message.edit_text(
		'Выберите тип объявлений', 
		reply_markup=inline_keyboards.ads_keyboard
	)


@dp.callback_query_handler(text='my_ads')
async def my_ads(call: CallbackQuery, state: FSMContext):
	ads = await db_commands.select_ads_by_user_id(call.from_user.id)
	if ads == []:
		await call.message.edit_text(
			'У Вас пока нет объявлений', 
			reply_markup=inline_keyboards.backtomenu_keyboard
		)	
	else:
		await call.message.edit_text(
			'Выберите тип объявлений', 
			reply_markup=inline_keyboards.ads_keyboard
		)

