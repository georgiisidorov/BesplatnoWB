import datetime
import logging

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

# ---------------------------------- В Р Е М Я --------------------------------------

@dp.callback_query_handler(text='new_ad')
async def new_ad(call: CallbackQuery, state: FSMContext):		
	user = await db_commands.select_user_by_user_id(call.from_user.id)
	
	if user.ads_amount == 0:
		await call.message.edit_text(
			f'<b>📌 Количество доступных публикаций: 0</b>',
			reply_markup=inline_keyboards.tariffs,
			parse_mode='html'
		)
	else: 
		now = datetime.datetime.now()+datetime.timedelta(hours=3)
		time_now = now - datetime.datetime(now.date().year, now.date().month, now.date().day)
		today = now - time_now
		theminutes_350 = today + datetime.timedelta(minutes=350)
		theminutes_710 = today + datetime.timedelta(minutes=710)
		theminutes_1070 = today + datetime.timedelta(minutes=1070)

		start_i = 36
		if (now > theminutes_350) and (now <= theminutes_710):
			start_i = 36
		elif (now > theminutes_710) and (now <= theminutes_1070):
			start_i = 72
		elif (now > theminutes_1070):
			start_i = 108

		days = 0

		list_keyboard = []

		for i in range(start_i, start_i+36):
			time = today + datetime.timedelta(minutes=i*10)

			if (i + 1) % 3 == 1:
				set_buttons = []

			if time > now:
				ad = await db_commands.select_ad_by_date_and_time(time)
				if ad is None:
					set_buttons.append(
						InlineKeyboardButton(
							text=f"{(time	).strftime('%H:%M')}", 
							callback_data=f"time_new___ad;{time.strftime('%d.%m.%Y')};{time.strftime('%H:%M')}"
						)
					)
				if ad is not None:
					set_buttons.append(
						InlineKeyboardButton(
							text=f"🚫 {(time	).strftime('%H:%M')}", 
							callback_data='neanunahui'
						)
					)

				if (i + 1) % 3 == 0:
					list_keyboard.append(set_buttons)


			if time < now:
				set_buttons.append(
					InlineKeyboardButton(
						text=f"🚫 {(time	).strftime('%H:%M')}", 
						callback_data='neanunahui'
					)
				)

		if start_i == 36:
			list_keyboard.append(
				[InlineKeyboardButton(text="⬅️", callback_data='neanunahui'), 
				InlineKeyboardButton(text="➡️", callback_data=f'checktime;72;{days}')]
			)
		elif start_i == 72:
			list_keyboard.append(
				[InlineKeyboardButton(text="⬅️", callback_data=f'checktime;36;{days}'), 
				InlineKeyboardButton(text="➡️", callback_data=f'checktime;108;{days}')]
			)
		elif start_i == 108:
			list_keyboard.append(
				[InlineKeyboardButton(text="⬅️", callback_data=f'checktime;72;{days}'),
				InlineKeyboardButton(text="➡️", callback_data='neanunahui')]
			)

		
		list_keyboard.append([InlineKeyboardButton(text="Сменить дату 📆", callback_data=f'date_change_c_h_e_c_k;{days}')])
		list_keyboard.append([InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu')])

		time_new_ad_keyboard = InlineKeyboardMarkup(inline_keyboard=list_keyboard)

		await call.message.edit_text(
			f"Вы выбрали дату <b>{today.strftime('%d.%m.%Y')}</b>", 
			reply_markup=time_new_ad_keyboard,
			parse_mode='html'
		)


@dp.callback_query_handler(text='checkschedule')
async def checkschedule(call: CallbackQuery, state: FSMContext):

	now = datetime.datetime.now()+datetime.timedelta(hours=3)	
	time_now = now - datetime.datetime(now.date().year, now.date().month, now.date().day)
	today = now - time_now
	theminutes_350 = today + datetime.timedelta(minutes=350)
	theminutes_710 = today + datetime.timedelta(minutes=710)
	theminutes_1070 = today + datetime.timedelta(minutes=1070)

	start_i = 36
	if (now > theminutes_350) and (now <= theminutes_710):
		start_i = 36
	elif (now > theminutes_710) and (now <= theminutes_1070):
		start_i = 72
	elif (now > theminutes_1070):
		start_i = 108

	days = 0

	list_keyboard = []
	user = await db_commands.select_user_by_user_id(call.from_user.id)

	for i in range(start_i, start_i+36):
		time = today + datetime.timedelta(minutes=i*10)

		if (i + 1) % 3 == 1:
			set_buttons = []

		if time > now:
			ad = await db_commands.select_ad_by_date_and_time(time)
			if ad is None:
				if user.ads_amount == 0:
					set_buttons.append(
						InlineKeyboardButton(
							text=f"{(time	).strftime('%H:%M')}", 
							callback_data="tariffs"
						)
					)
				else:
					set_buttons.append(
						InlineKeyboardButton(
							text=f"{(time	).strftime('%H:%M')}", 
							callback_data=f"time_new___ad;{time.strftime('%d.%m.%Y')};{time.strftime('%H:%M')}"
						)
					)
			if ad is not None:
				set_buttons.append(
					InlineKeyboardButton(
						text=f"🚫 {(time	).strftime('%H:%M')}", 
						callback_data='neanunahui'
					)
				)

			if (i + 1) % 3 == 0:
				list_keyboard.append(set_buttons)


		if time < now:
			set_buttons.append(
				InlineKeyboardButton(
					text=f"🚫 {(time	).strftime('%H:%M')}", 
					callback_data='neanunahui'
				)
			)

	if start_i == 36:
		list_keyboard.append(
			[InlineKeyboardButton(text="⬅️", callback_data='neanunahui'), 
			InlineKeyboardButton(text="➡️", callback_data=f'checktime;72;{days}')]
		)
	elif start_i == 72:
		list_keyboard.append(
			[InlineKeyboardButton(text="⬅️", callback_data=f'checktime;36;{days}'), 
			InlineKeyboardButton(text="➡️", callback_data=f'checktime;108;{days}')]
		)
	elif start_i == 108:
		list_keyboard.append(
			[InlineKeyboardButton(text="⬅️", callback_data=f'checktime;72;{days}'),
			InlineKeyboardButton(text="➡️", callback_data='neanunahui')]
		)

	
	list_keyboard.append([InlineKeyboardButton(text="Сменить дату 📆", callback_data=f'date_change_c_h_e_c_k;{days}')])
	list_keyboard.append([InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu')])

	time_new_ad_keyboard = InlineKeyboardMarkup(inline_keyboard=list_keyboard)

	await call.message.edit_text(
		f"Вы выбрали дату <b>{today.strftime('%d.%m.%Y')}</b>", 
		reply_markup=time_new_ad_keyboard,
		parse_mode='html'
	)


@dp.callback_query_handler(text_contains='checktime;')
async def checktime(call: CallbackQuery, state: FSMContext):
	start_i = int(call.data.split(';')[-2])
	days = int(call.data.split(';')[-1])

	now = datetime.datetime.now()+datetime.timedelta(hours=3)	
	time_now = now - datetime.datetime(now.date().year, now.date().month, now.date().day)
	today = now - time_now
	the_day = today + datetime.timedelta(days=days)

	list_keyboard = []
	user = await db_commands.select_user_by_user_id(call.from_user.id)

	for i in range(start_i, start_i+36):
		time = the_day + datetime.timedelta(minutes=i*10)

		if (i + 1) % 3 == 1:
			set_buttons = []

		if time > now:
			ad = await db_commands.select_ad_by_date_and_time(time)
			if ad is None:
				if user.ads_amount == 0:
					set_buttons.append(
						InlineKeyboardButton(
							text=f"{(time	).strftime('%H:%M')}", 
							callback_data="tariffs"
						)
					)
				else:
					set_buttons.append(
						InlineKeyboardButton(
							text=f"{(time	).strftime('%H:%M')}", 
							callback_data=f"time_new___ad;{time.strftime('%d.%m.%Y')};{time.strftime('%H:%M')}"
						)
					)
			if ad is not None:
				set_buttons.append(
					InlineKeyboardButton(
						text=f"🚫 {(time	).strftime('%H:%M')}", 
						callback_data='neanunahui'
					)
				)

			if (i + 1) % 3 == 0:
				list_keyboard.append(set_buttons)


		if time < now:
			set_buttons.append(
				InlineKeyboardButton(
					text=f"🚫 {(time	).strftime('%H:%M')}", 
					callback_data='neanunahui'
				)
			)

	if start_i == 36:
		list_keyboard.append(
			[InlineKeyboardButton(text="⬅️", callback_data='neanunahui'), 
			InlineKeyboardButton(text="➡️", callback_data=f'checktime;72;{days}')]
		)
	elif start_i == 72:
		list_keyboard.append(
			[InlineKeyboardButton(text="⬅️", callback_data=f'checktime;36;{days}'), 
			InlineKeyboardButton(text="➡️", callback_data=f'checktime;108;{days}')]
		)
	elif start_i == 108:
		list_keyboard.append(
			[InlineKeyboardButton(text="⬅️", callback_data=f'checktime;72;{days}'),
			InlineKeyboardButton(text="➡️", callback_data='neanunahui')]
		)

	
	list_keyboard.append([InlineKeyboardButton(text="Сменить дату 📆", callback_data=f'date_change_c_h_e_c_k;{days}')])
	list_keyboard.append([InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu')])

	time_new_ad_keyboard = InlineKeyboardMarkup(inline_keyboard=list_keyboard)

	await call.message.edit_text(
		f"Вы выбрали дату <b>{the_day.strftime('%d.%m.%Y')}</b>", 
		reply_markup=time_new_ad_keyboard,
		parse_mode='html'
	)


@dp.callback_query_handler(text_contains='date_change_c_h_e_c_k;')
async def date_change_c_h_e_c_k(call: CallbackQuery, state: FSMContext):
	await call.answer()
	days = int(call.data.split(';')[-1])

	now = datetime.datetime.now()+datetime.timedelta(hours=3)	
	time_now = now - datetime.datetime(now.date().year, now.date().month, now.date().day)
	today = now - time_now

	list_keyboard = []

	for day in range(7):
		iter_day = today + datetime.timedelta(days=day)
		list_keyboard.append([InlineKeyboardButton(text=f"{iter_day.strftime('%d.%m.%Y')}", callback_data=f'checktime;36;{day}')])

	list_keyboard.append([InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu')])

	date_new_ad_keyboard = InlineKeyboardMarkup(inline_keyboard=list_keyboard)

	await call.message.edit_text(
		f"Выберите дату 👇", 
		reply_markup=date_new_ad_keyboard,
		parse_mode='html'
	)

#  ------------------------------- Ф О Т О -------------------------------------


@dp.callback_query_handler(state=States.AdText, text='menu')
async def menu_from_text(call: CallbackQuery, state: FSMContext):
	await call.answer()
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


@dp.callback_query_handler(state=States.AdPhoto, text='menu')
async def menu_from_photo(call: CallbackQuery, state: FSMContext):
	await call.answer()

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
		f'{txet}Если возникли вопросы, то нажмите FAQ ❓ или напишите в поддержку''',
		reply_markup=inline_keyboards.menu_user,
		parse_mode='html'
	)


@dp.callback_query_handler(text_contains='time_new___ad;')
async def time_new___ad(call: CallbackQuery, state: FSMContext):
	await call.answer()
	time = call.data.split(';')[2]
	date = call.data.split(';')[1]
	
	now = datetime.datetime.now()+datetime.timedelta(hours=3)	
	datetime_ad = datetime.datetime.strptime(f'{date} {time}', '%d.%m.%Y %H:%M')	
	if now < datetime_ad:
		msg = await call.message.edit_text(
			'Пришлите ОДНУ фотографию объявления', 
			reply_markup=inline_keyboards.backtomenu_keyboard
		)
		await state.update_data(msg_id=msg.message_id, date=date, time=time)
		await States.AdPhoto.set()


@dp.message_handler(state=States.AdPhoto, content_types=ContentType.VIDEO)
async def advideo(message: Message, state: FSMContext):
	data = await state.get_data()
	msg_id = data.get('msg_id')
	await dp.bot.delete_message(message.from_user.id, msg_id)
	await message.delete()
	msg = await message.answer(
		'Вы прислали видео, а нужна ОДНА фотография. Попробуйте ещё раз.',
		reply_markup=inline_keyboards.backtomenu_keyboard
	)
	await state.update_data(msg_id=msg.message_id)


@dp.message_handler(state=States.AdPhoto, content_types=ContentType.PHOTO)
async def adphoto(message: Message, state: FSMContext):
	data = await state.get_data()
	msg_id = data.get('msg_id')
	await dp.bot.delete_message(message.from_user.id, msg_id)
	
	await message.delete()
	msg = await message.answer(
		'Пришлите текст объявления'
	)	

	photo = message.photo[-1].file_id
	await state.update_data(photo=photo)

	await state.update_data(msg_ids=[msg.message_id])
	await States.AdText.set()


@dp.message_handler(state=States.AdText)
async def adtext(message: Message, state: FSMContext):
	await message.delete()
	data = await state.get_data()
	for msg_id in data.get('msg_ids'):
		await dp.bot.delete_message(message.from_user.id, msg_id)

	text = message.html_text
	if len(text) > 1024:
		msg = await message.answer('Присланный Вами текст больше 1024 знаков, что недопустимо. Попробуйте прислать текст ещё раз')
		await state.update_data(msg_ids=[msg.message_id])
	else:
		photo = data.get('photo')
		time = data.get('time')
		date = data.get('date')

		msg = await message.answer_photo(
			photo=photo,
			caption=text,
			parse_mode='html'
		)

		await state.finish()
		await state.update_data(
			msg_id=msg.message_id, 
			text=text, 
			photo=photo, 
			time=time,
			date=date
		)
		tttime = (datetime.datetime.strptime(f'{date} {time}', '%d.%m.%Y %H:%M')	).strftime("%d.%m.%Y %H:%M")
		await message.answer(
			f'Вы собираетесь опубликовать это объявление 👆 в {tttime}. Подтверждаете?',
			reply_markup=inline_keyboards.confirm_markup
		)


@dp.callback_query_handler(text='confirm')
async def confirm(call: CallbackQuery, state: FSMContext):		
	data = await state.get_data()
	text = data.get('text')
	photo = data.get('photo')
	time = data.get('time')
	date = data.get('date')
	msg_id = data.get('msg_id')
	datetttime = datetime.datetime.strptime(f'{date} {time}', '%d.%m.%Y %H:%M')	
	await db_commands.add_ad(
		user_id=call.from_user.id, 
		photo=photo, 
		accepted=False,
		publicated=False,
		text=text, 
		datetime_publication=datetttime
	)
	ad = await db_commands.select_ad_by_date_and_time(datetttime)
	await dp.bot.delete_message(call.from_user.id, msg_id)

	await call.message.edit_text(
		'Публикация объявления подтверждена!\n\n'
		'Однако прежде объявление должен проверить администратор, ожидайте...'
	)

	menu_admin = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text="Принять объявление ✅", callback_data=f'accept_ad;{call.message.message_id};{ad.id}')],
		[InlineKeyboardButton(text="Отправить на редактирование 📝", callback_data=f'edit_ad;{call.message.message_id};{ad.id}')],
		[InlineKeyboardButton(text="Удалить объявление ❌", callback_data=f'delete_ad;{call.message.message_id};{ad.id}')]
	])

	await dp.bot.send_photo(
		config.admin_id, 
		photo=photo, 
		caption=text, 
		reply_markup=menu_admin
	)




