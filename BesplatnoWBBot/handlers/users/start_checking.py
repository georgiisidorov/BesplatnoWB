import datetime
import logging
import random

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


async def check_subscription(chat_id, user_id):
	member = await dp.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
	return member.is_chat_member()


@dp.message_handler(state='*', text='/start')
async def start(message: Message, state: FSMContext):
	
	if message.from_user.id == message.chat.id:
		try:
			fullname = message.from_user.first_name + ' ' + message.from_user.last_name
		except TypeError:
			fullname = message.from_user.first_name

		await db_commands.add_user(
			message.from_user.id,
			message.from_user.username,
			fullname,
			'None',
			0
		)
		
		result = True
		for chat in config.chats_subscribed:
			result = result and await check_subscription(chat, message.from_user.id)

		data = await state.get_data()
		invoice_msgid = data.get('invoice_msgid')
		try:
			await dp.bot.delete_message(message.from_user.id, invoice_msgid)
		except Exception:
			pass
		await state.finish()

		if result == False:
			await state.update_data(msg_ids=[])

			await message.answer(
				f'Привет, {fullname}! Вы находитесь в боте, который управляет'
				' размещением Ваших публикаций в сообществе “Товар за отзыв WB / OZON”'
				'\n\nДля того, чтобы начать пользоваться нашим ботом'
				'\nОбязательно подпишитесь на само сообщество @rnoqqq и нажмите …👇',
				reply_markup=inline_keyboards.start_checking_keyboard
			)
		elif result == True:
			user = await db_commands.select_user_by_user_id(message.from_user.id)
			if user.ads_amount > 0: 
				txet = '\n\nДля размещения поста нажмите «Новое объявление»\n\n'
			else: 
				txet = '\n\nДля пополнения счёта нажмите «Оплатить тариф»\n\n'
				
			await message.answer(
				f'Сейчас Вы находитесь в Вашем личном кабинете.'
				f'\n\n<b>📌 Количество доступных публикаций: {user.ads_amount}</b>'
				f'{txet}Если возникли вопросы, то нажмите FAQ ❓ или напишите в поддержку',
				reply_markup=inline_keyboards.menu_user,
				parse_mode='html'
			)



@dp.callback_query_handler(text='start_checking')
async def start_checking(call: CallbackQuery, state: FSMContext):
	result = True
	for chat in config.chats_subscribed:
		result = result and await check_subscription(chat, call.from_user.id)

	if result:
		await call.answer()
		await call.message.edit_text(
			f'''Правила пользования нашим сервисом!

1. К публикации принимаются объявления с 1 фото (фото может содержать изображение от 1 до 4 товаров в виде коллажа)

2. В тексте объявления могут присутствовать от 1 до 4 ссылок на маркетплейсы (WB/OZON/YandexMarket и др).
 Ссылка может вести на конкретный товар, бренд, подборку или весь ассортимент вашего магазина.
При необходимости, в тексте объявления может указываться контакт в Телеграм вашего менеджера. 

3. Форматы рекламных размещений не связанных с непосредственной продажей товаров на маркетплейсах нужно согласовывать с техподдержкой ДО ОПЛАТЫ тарифов на размещение. 

4. В боте присутствует автоматизированная очередь публикаций, которая обновляется в режиме реального времени, перед оплатой тарифа ознакомьтесь с графиком публикаций и удостоверьтесь в наличии свободных слотов на необходимые вам дату и время.

ИНН: 505311158441 ОГРНИП: 320508100390715 
Договор оферта - disk.yandex.ru/i/6HzZHMsE_WkBbA
Техподдержка бота - @{config.admin_support}

Подтверждая данную оферту, Вы принимаете все правила нашего сервиса.''',
			reply_markup=inline_keyboards.confirm_oferta_keyboard,
			disable_web_page_preview=True
		)
	else:
		await call.answer('Бот не нашел Вас в списке подписавшихся. Проверьте Вашу подписку!', show_alert=True)


@dp.callback_query_handler(text='confirm_oferta')
async def confirm_oferta(call: CallbackQuery, state: FSMContext):
	await call.answer()
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
