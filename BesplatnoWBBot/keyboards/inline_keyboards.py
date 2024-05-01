from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config
from services import db_commands


start_checking_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Проверить подписку", callback_data='start_checking')]
])


menu_user = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новое объявление 📨", callback_data='new_ad')],
        [InlineKeyboardButton(text="Посмотреть расписание 🔎", callback_data='checkschedule')],
        [InlineKeyboardButton(text="Мои объявления 🗂", callback_data='my_ads')],
        [InlineKeyboardButton(text="Оплатить тариф 💳", callback_data='tariffs')],
        [InlineKeyboardButton(text="FAQ ❓", callback_data='faq')],
        [InlineKeyboardButton(text="Поддержка 👨‍💻", url=f't.me/{config.admin_support}')]
])


edit_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Редактировать объявление 📝", callback_data='new_ad')]
])



menu_admin = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Принять объявление ✅", callback_data='accept_ad')],
        [InlineKeyboardButton(text="Отправить на редактирование 📝", callback_data='edit_ad')],
        [InlineKeyboardButton(text="Удалить объявление ❌", callback_data='delete_ad')]
])


async def tariffs():
        buttons = []
        list_of_tariffs = await db_commands.select_tariffs()
        for tariff in list_of_tariffs:
                if (str(tariff.ads_amount)[-1] == '1') and (tariff.ads_amount != 11):
                        post = 'пост'
                elif (str(tariff.ads_amount)[-1] in ['2', '3', '4']) and (tariff.ads_amount not in [12, 13, 14]):
                        post = 'поста'
                else:
                        post = 'постов'
                buttons.append([InlineKeyboardButton(
                        text=f"{tariff.ads_amount} {post} - {tariff.price}₽", 
                        callback_data=f'{tariff.price};{tariff.ads_amount};rub'
                        )
                ])

        buttons.append([InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu')])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        return keyboard


ads_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Запланированные", callback_data='planned')],
        [InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu')]
])


backtomenu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu')]
])


return_to_my_ads_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад ◀️", callback_data='return_to_my_ads')]
])


return_to_my_ads_repeat_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад ◀️", callback_data='return_to_my_ads_repeat')]
])


confirm_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена 🚫", callback_data='cancel'),
        InlineKeyboardButton(text="Подтвердить ✅", callback_data="confirm")]
])

confirm_oferta_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить оферту 📝", callback_data='confirm_oferta')]
])



# slider_keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="◀️", callback_data='minus'),
#         InlineKeyboardButton(text="▶️", callback_data='plus')],
#         [InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu_back')]
# ])


# slider_keyboard_VIP = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="◀️", callback_data='minus_VIP'),
#         InlineKeyboardButton(text="▶️", callback_data='plus_VIP')],
#         [InlineKeyboardButton(text="Сменить фотографию", callback_data='change_photo')],
#         [InlineKeyboardButton(text="Удалить ❌", callback_data='not_confirm'),
#         InlineKeyboardButton(text="Одобрить ✅", callback_data='confirm')],
#         [InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu_back')]
# ])


# slider_keyboard_VIP_2 = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="◀️", callback_data='minus_VIP_2'),
#         InlineKeyboardButton(text="▶️", callback_data='plus_VIP_2')],
#         [InlineKeyboardButton(text="Удалить отзыв ❌", callback_data='not_confirm_2')],
#         [InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu_back')]
# ])


# slider_keyboard_VIP_empty = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Вернуться к отзывам", callback_data='check_feedbacks_again')],
#         [InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu_back')]
# ])


# slider_keyboard_VIP_empty_2 = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Вернуться к отзывам", callback_data='check_feedbacks_again_2')],
#         [InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu_back')]
# ])




# backtomenu_del_keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Главное меню ↩️", callback_data='menu_del')]
# ])


