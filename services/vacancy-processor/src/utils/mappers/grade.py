from database.models.enums import GradeEnum


__all__ = ["map_to_grade_enum"]


def map_to_grade_enum(grade: str) -> GradeEnum | None:
    grade = grade.lower().strip()

    grade_enum = GradeEnum.get_safe(grade)
    if grade_enum:
        return grade_enum

    for grade_enum, aliases in grades_map.items():
        if grade in aliases:
            return grade_enum

    return None


grades_map: dict[GradeEnum, tuple[str, ...]] = {
    GradeEnum.INTERN: ("стажёр", "intern"),
    GradeEnum.MIDDLE: ("middle+",),
}
