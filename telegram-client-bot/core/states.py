from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    auth = State()
    select_lab = State()
    select_course = State()
    main_menu = State()
    profile = State()
    add_course = State()
    change_github = State()
