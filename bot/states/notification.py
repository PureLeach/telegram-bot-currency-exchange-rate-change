from aiogram.dispatcher.filters.state import State, StatesGroup


class AddNotificationState(StatesGroup):
    waiting_for_currency_selection = State()
    waiting_for_value_input = State()


class RemoveNotificationState(StatesGroup):
    waiting_for_index_input = State()


class RemoveAllNotificationState(StatesGroup):
    waiting_for_response = State()
