from collections.abc import Sequence

from common.shared.services import BaseService
from database.models import Profession
from database.models.enums import ProfessionEnum
from repositories import ProfessionRepository


__all__ = ["ProfessionService"]


class ProfessionService(BaseService[ProfessionRepository]):
    """Сервис для бизнес-операций, связанных с профессиями."""

    async def get_profession_by_name(self, name: ProfessionEnum) -> Profession | None:
        return await self._repo.get_by_name(name)

    async def get_professions(self) -> Sequence[Profession]:
        return await self._repo.get_all()

    async def add_profession(self, profession: ProfessionEnum) -> None:
        """Создает и добавляет профессию в сессию (без коммита)."""
        profession_model = Profession(name=profession)
        self._repo.add(profession_model)
