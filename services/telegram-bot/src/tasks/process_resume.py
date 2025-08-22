import asyncio
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING, Any, cast

from celery_app import app
from clients import skill_client
from common.logger import get_logger
from core.loader import bot
from database.models.enums import PreferencesCategoryCodeEnum
from keyboard.inline.main import main_menu_keyboard
from keyboard.inline.update_skills import update_skills_keyboard
from schemas.user_preference import UserPreferenceCreate
from tasks.schemas import FileResumePayloadSchema, TextResumePayloadSchema
from unitofwork import UnitOfWork
from utils.extractors import TextExtractor

from services import UserPreferenceService


if TYPE_CHECKING:
    from celery import Task


__all__ = ["process_resume"]


logger = get_logger(__name__)


@app.task(name="process_resume", bind=True, max_retries=3)
def process_resume(self: "Task[Any, Any]", user_id: int, chat_id: int, data: dict[str, Any]) -> None:
    loop = asyncio.get_event_loop()

    data_type = data.get("type")

    try:
        if data_type == "text":
            text_schema = TextResumePayloadSchema(**data)
            text = text_schema.text
        elif data_type == "file":
            file_schema = FileResumePayloadSchema(**data)
            with NamedTemporaryFile(suffix=file_schema.suffix) as tmp:
                loop.run_until_complete(bot.download_file(file_schema.file_path, destination=tmp.name))
                extractor = TextExtractor()
                text = extractor.read(tmp.name)
        else:
            raise ValueError(f"Invalid data type: {data_type}")  # noqa: TRY301

        loop.run_until_complete(_extract_and_save_user_preferences(user_id, text, chat_id))
    except Exception as e:
        logger.exception("Error processing resume", exc_info=e)

        if self.request.retries >= cast("int", self.max_retries):
            loop.run_until_complete(
                bot.send_message(
                    chat_id,
                    "⚠️ Произошла ошибка при извлечении навыков.\nПроверьте корректность содержимого файла.",
                    reply_markup=main_menu_keyboard(),
                )
            )
        else:
            raise self.retry(countdown=60, exc=e) from e


async def _extract_and_save_user_preferences(user_id: int, text: str, chat_id: int) -> None:
    skills = await skill_client.extract_skills_from_text(text)
    if not skills:
        await bot.send_message(
            chat_id,
            "⚠️ В приведенном тексте не найдено ни одного навыка.",
            reply_markup=main_menu_keyboard(),
        )
        return

    async with UnitOfWork() as uow:
        service = UserPreferenceService(uow)
        added_preferences = await service.replace_user_preferences(
            user_id=user_id,
            category_code=PreferencesCategoryCodeEnum.SKILL,
            preferences=[
                UserPreferenceCreate(
                    user_id=user_id,
                    category_code=PreferencesCategoryCodeEnum.SKILL,
                    item_id=s.id,
                    item_name=s.name,
                )
                for s in skills
            ],
        )
        await uow.commit()

        added_skills_str = ", ".join(sorted(pref.item_name for pref in added_preferences))
        await bot.send_message(
            chat_id,
            f"✅ Ваши навыки успешно обновлены.\n\n"
            f"Теперь вы будете получать вакансии, релевантные под ваши навыки:\n"
            f"{added_skills_str}",
            reply_markup=update_skills_keyboard(),
        )
