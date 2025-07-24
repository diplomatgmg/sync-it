from collections.abc import Sequence

from database.models import Profession
from database.models.enums import ProfessionEnum
from repositories import ProfessionRepository


__all__ = ["ProfessionService"]


class ProfessionService:
    """Сервис для бизнес-операций, связанных с профессиями."""

    def __init__(self, repo: ProfessionRepository) -> None:
        self.repo = repo

    async def get_profession_by_name(self, name: ProfessionEnum) -> Profession | None:
        return await self.repo.get_by_name(name)

    async def get_professions(self) -> Sequence[Profession]:
        return await self.repo.get_all()

    async def add_profession(self, profession: ProfessionEnum) -> None:
        """Создает и добавляет профессию в сессию (без коммита)."""
        profession_model = Profession(name=profession)
        self.repo.add(profession_model)
