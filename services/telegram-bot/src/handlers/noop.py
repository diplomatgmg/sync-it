from aiogram import F, Router
from aiogram.types import CallbackQuery
from callbacks.noop import NoopActionEnum, NoopCallback


__all__ = ["router"]


router = Router(name=NoopCallback.__prefix__)


@router.callback_query(NoopCallback.filter(F.action == NoopActionEnum.DO_NOTHING))
async def handle_noop_callback(query: CallbackQuery) -> None:
    await query.answer("Ничего не произошло")
