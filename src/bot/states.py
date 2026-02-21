from aiogram.fsm.state import State, StatesGroup


class CheckoutState(StatesGroup):
    name = State()
    phone = State()
    address = State()
    comment = State()
    confirm = State()


class AdminCategoryState(StatesGroup):
    add_name = State()
    rename_pick = State()
    rename_name = State()


class AdminProductState(StatesGroup):
    add_category = State()
    add_name = State()
    add_description = State()
    add_price = State()
