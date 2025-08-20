import re
from typing import Self

from common.logger import get_logger
from database.models.enums import GradeEnum, ProfessionEnum, SkillCategoryEnum, SkillEnum, WorkFormatEnum
from utils.mappers import map_to_profession_enum, map_to_skill_category_and_skill_enum
from utils.mappers.grade import map_to_grade_enum
from utils.mappers.work_format import map_to_work_format_enum


__all__ = ["VacancyExtractor"]


logger = get_logger(__name__)


class VacancyExtractor:
    """
    Класс извлечения ключевых данных из текста вакансии:
    - профессию
    - грейд
    - формат работы
    - навыки
    - описание (обязанности, требования и пр.)
    """

    def __init__(self) -> None:
        self._paragraphs: list[str] | None = None

        self.company_name: str | None = None
        self.profession: ProfessionEnum = ProfessionEnum.UNKNOWN
        self.salary: str | None = None
        self.grades: list[GradeEnum] = []
        self.work_formats: list[WorkFormatEnum] = []
        self.skills: list[tuple[SkillCategoryEnum, SkillEnum]] = []

        self.workplace_description: str | None = None
        self.responsibilities: str | None = None
        self.requirements: str | None = None
        self.conditions: str | None = None

    def extract(self, vacancy: str) -> "Self":
        """Извлекает данные из текстового представления вакансии."""
        cleaned_vacancy = self._clean_vacancy(vacancy)
        logger.debug("Start extracting vacancy: \n%s", cleaned_vacancy)

        self.company_name = self._parse_company_name(cleaned_vacancy)
        self.profession = self._parse_profession(cleaned_vacancy)
        self.salary = self._parse_salary(cleaned_vacancy)
        self.grades = self._parse_grades(cleaned_vacancy)
        self.work_formats = self._parse_work_formats(cleaned_vacancy)
        self.skills = self._parse_skills(cleaned_vacancy)

        self.workplace_description = self._parse_multiline_field(cleaned_vacancy, "О месте работы")
        self.responsibilities = self._parse_multiline_field(cleaned_vacancy, "Обязанности")
        self.requirements = self._parse_multiline_field(cleaned_vacancy, "Требования")
        self.conditions = self._parse_multiline_field(cleaned_vacancy, "Условия")

        logger.debug("Extracted vacancy: %s", self)
        return self

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
    def _parse_company_name(message: str) -> str | None:
        """Извлекает название компании из сообщения."""
        pattern = r"Компания:\s(.*)"
        match = re.search(pattern, message)
        if not match:
            logger.warning("Company pattern not found in message: %s", message)
            return None

        return match.group(1).strip()

    @staticmethod
    def _parse_profession(message: str) -> ProfessionEnum:
        """Извлекает профессию из сообщения."""
        pattern = r"Профессия:\s(.*)"
        match = re.search(pattern, message)
        if not match:
            logger.warning("Profession pattern not found in message: %s", message)
            return ProfessionEnum.UNKNOWN

        profession_str = match.group(1).strip()

        return map_to_profession_enum(profession_str)

    @staticmethod
    def _parse_salary(message: str) -> str | None:
        """Извлекает зарплату из сообщения."""
        pattern = r"Зарплата:\s(.*)"
        match = re.search(pattern, message)
        if not match:
            logger.warning("Salary pattern not found in message: %s", message)
            return None

        salary_str = match.group(1).strip()
        if not salary_str:
            return None
        if salary_str == "Неизвестно":
            return None
        if "обсуждается" in salary_str.lower():
            return None
        if "собеседов" in salary_str.lower():
            return None

        return salary_str

    @staticmethod
    def _parse_grades(message: str) -> list[GradeEnum]:
        """Извлекает значение грейда из сообщения."""
        pattern = r"Позиция:\s(.*)"
        match = re.search(pattern, message)
        if not match:
            logger.warning("Grade pattern not found in message: %s", message)
            return [GradeEnum.UNKNOWN]

        grades: list[GradeEnum] = []

        grade_str = match.group(1).strip()
        # Junior/Middle/Senior
        grade_parts = re.split(r"/", grade_str)  # noqa: RUF055 убрать noqa после добавления паттерна

        for part in grade_parts:
            clean_part = part.strip()

            grade = map_to_grade_enum(clean_part)
            if not grade:
                logger.warning("Unknown grade part: %s", clean_part)
                continue

            grades.append(grade)

        if not grades:
            grades = [GradeEnum.UNKNOWN]

        return grades

    @staticmethod
    def _parse_work_formats(message: str) -> list[WorkFormatEnum]:
        """Извлекает значение формата работы из сообщения."""
        pattern = r"Тип занятости:\s(.*)"
        match = re.search(pattern, message)
        if not match:
            logger.warning("Work format pattern not found in message: %s", message)
            return [WorkFormatEnum.UNKNOWN]

        work_formats: list[WorkFormatEnum] = []

        work_format_str = match.group(1).strip()
        # Удаленка/Гибрид | Удаленка, Гибрид
        work_format_parts = re.split(r"[/,]", work_format_str)

        for part in work_format_parts:
            clean_part = part.strip()

            work_format = map_to_work_format_enum(clean_part)
            if not work_format:
                logger.warning("Unknown work format part: %s", clean_part)
                continue

            work_formats.append(work_format)

        if not work_formats:
            work_formats = [WorkFormatEnum.UNKNOWN]

        return work_formats

    @staticmethod
    def _parse_skills(message: str) -> list[tuple[SkillCategoryEnum, SkillEnum]]:
        """Извлекает навыки из сообщения."""
        pattern = r"Навыки:\s(.*)"
        match = re.search(pattern, message)
        if not match:
            logger.warning("Skills pattern not found in message: %s", message)
            return []

        skills: list[tuple[SkillCategoryEnum, SkillEnum]] = []

        skills_str = match.group(1).strip()
        # Python, Git
        skills_parts = re.split(r",", skills_str)  # noqa: RUF055 убрать noqa после добавления паттерна

        for part in skills_parts:
            clean_part = part.strip()

            category, skill = map_to_skill_category_and_skill_enum(clean_part)
            if not skill or not category:
                logger.warning("Unknown skill part: %s", clean_part)
                continue

            skills.append((category, skill))

        return skills

    def _parse_multiline_field(self, message: str, field_name: str) -> str | None:
        """
        Извлекает многострочное текстовое поле из вакансии.

        Ищет блок с заголовком field_name, например 'Обязанности', и
        захватывает текст до следующего заголовка или конца текста.
        """
        if not self._paragraphs:
            self._paragraphs = message.split("\n\n")

        pattern = rf"{field_name}:[\s\n]*(.*?)(?=\n\n\w+:|$)"  # на эльфийском
        match = re.search(pattern, message, re.DOTALL)
        if not match:
            logger.warning('Not found multiline field: "%s" for message:\n%s', field_name, message)
            return None

        content = match.group(1).strip()
        return content or None
