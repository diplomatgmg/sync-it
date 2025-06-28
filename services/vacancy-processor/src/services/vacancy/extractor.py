import re
from typing import Self

from common.logger import get_logger
from database.models.enums import GradeEnum, ProfessionEnum, WorkFormatEnum
from utils.mappers import map_to_profession_enum, map_to_skill_name


__all__ = ["VacancyExtractorService"]


logger = get_logger(__name__)


class VacancyExtractorService:
    """
    Класс извлечения ключевых данных из текста вакансии:
    - профессию
    - грейды
    - формат работы
    - навыки
    # TODO: - описание вакансии
    """

    def __init__(self) -> None:
        self.profession: ProfessionEnum | None = None
        self.grades: list[GradeEnum] | None = None
        self.work_formats: list[WorkFormatEnum] | None = None
        self.skills: list[str] | None = None

        self.workplace_description: str | None = None
        self.responsibilities: str | None = None
        self.requirements: str | None = None
        self.conditions: str | None = None

    def extract(self, vacancy: str) -> "Self":
        """Извлекает данные из текстового представления вакансии."""
        logger.debug("Start extracting vacancy: \n%s", vacancy)

        cleaned_vacancy = self._clean_vacancy(vacancy)

        self.profession = self._parse_profession(cleaned_vacancy)
        self.grades = self._parse_grades(cleaned_vacancy)
        self.work_formats = self._parse_work_formats(cleaned_vacancy)
        self.skills = self._parse_skills(cleaned_vacancy)

        return self

    def __repr__(self) -> str:
        return (
            "<VacancyExtractorService(\n"
            f"\tprofession={self.profession!r},\n"
            f"\tgrades={self.grades!r},\n"
            f"\twork_formats={self.work_formats!r},\n"
            f"\tskills={self.skills!r}\n"
            ")>"
        )

    @staticmethod
    def _clean_vacancy(vacancy: str) -> str:
        return (
            vacancy.replace("*", "")
            .replace("⸺", "-")  # Двойное тире
            .replace("—", "-")  # Длинное тире
            .replace("–", "-")  # Короткое тире
            .replace("―", "-")  # Горизонтальная черта
            .strip()
        )

    @staticmethod
    def _parse_profession(message: str) -> ProfessionEnum | None:
        """Извлекает профессию из сообщения."""
        pattern = r"Профессия:\s(.*)"
        match = re.search(pattern, message)
        if not match:
            return None

        profession_str = match.group(1)

        return map_to_profession_enum(profession_str)

    @staticmethod
    def _parse_grades(message: str) -> list[GradeEnum] | None:
        """Извлекает значение грейда из сообщения."""
        pattern = r"Позиция:\s(.*)"
        match = re.search(pattern, message)
        if not match:
            return None

        grades: list[GradeEnum] = []

        grade_str = match.group(1)
        # Junior/Middle/Senior
        grade_parts = re.split(r"/", grade_str)  # noqa: RUF055 убрать noqa после добавления паттерна

        for part in grade_parts:
            clean_part = part.strip()

            grade = GradeEnum.get_safe(clean_part)
            if not grade:
                logger.warning("Unknown grade part: %s (full: %s)", clean_part, grade_str)
                continue

            grades.append(grade)

        return grades

    @staticmethod
    def _parse_work_formats(message: str) -> list[WorkFormatEnum] | None:
        """Извлекает значение формата работы из сообщения."""
        pattern = r"Тип занятости:\s(.*)"
        match = re.search(pattern, message)
        if not match:
            return None

        work_formats: list[WorkFormatEnum] = []

        work_format_str = match.group(1)
        # Удаленка/Гибрид | Удаленка, Гибрид
        work_format_parts = re.split(r"[/,]", work_format_str)

        for part in work_format_parts:
            clean_part = part.strip()

            work_format = WorkFormatEnum.get_safe(clean_part)
            if not work_format:
                logger.warning("Unknown work format part: %s (full: %s)", clean_part, work_format_str)
                continue

            work_formats.append(work_format)

        return work_formats or None

    @staticmethod
    def _parse_skills(message: str) -> list[str] | None:
        """Извлекает навыки из сообщения."""
        pattern = r"Навыки:\s(.*)"
        match = re.search(pattern, message)
        if not match:
            return None

        # FIXME CategoryEnum + SkillEnum?
        skills: list[str] = []

        skills_str = match.group(1)
        # Python, Git
        skills_parts = re.split(r",", skills_str)  # noqa: RUF055 убрать noqa после добавления паттерна

        for part in skills_parts:
            clean_part = part.strip()

            skill = map_to_skill_name(clean_part)
            if not skill:
                logger.warning("Unknown skill part: %s (full: %s)", clean_part, skills_str)
                continue

            skills.append(skill)

        return skills or None
