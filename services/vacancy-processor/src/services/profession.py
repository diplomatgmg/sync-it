from common.shared.services import BaseUOWService
from database.models import Profession
from database.models.enums import ProfessionEnum
from schemas.profession import ProfessionCreate, ProfessionRead
from unitofwork import UnitOfWork


__all__ = ["ProfessionService"]


class ProfessionService(BaseUOWService[UnitOfWork]):
    """Сервис для бизнес-операций, связанных с профессиями."""

    async def get_profession_by_name(self, name: ProfessionEnum) -> ProfessionRead | None:
        profession = await self._uow.professions.get_by_name(name)

        return ProfessionRead.model_validate(profession) if profession else None

    async def get_professions(self) -> list[ProfessionRead]:
        professions = await self._uow.professions.get_all()

        return [ProfessionRead.model_validate(p) for p in professions]

    async def add_profession(self, profession: ProfessionCreate) -> ProfessionRead:
        profession_model = Profession(**profession.model_dump())
        created_profession = await self._uow.professions.add(profession_model)

        return ProfessionRead.model_validate(created_profession)
