from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
	AdText = State()
	AdPhoto = State()
	Comment = State()