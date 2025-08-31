from aiogram.fsm.state import State, StatesGroup


__all__ = ["PreferencesState"]


class PreferencesState(StatesGroup):
    waiting_for_data = State()
    waiting_toggle_skills = State()
