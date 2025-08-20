from database.models.enums import WorkFormatEnum


__all__ = ["map_to_work_format_enum"]


def map_to_work_format_enum(work_format: str) -> WorkFormatEnum | None:
    work_format = work_format.lower().strip()

    wf_enum = WorkFormatEnum.get_safe(work_format)
    if wf_enum:
        return wf_enum

    for wf_enum, aliases in work_formats_map.items():
        if any(alias in work_format for alias in aliases):
            return wf_enum

    return None


work_formats_map: dict[WorkFormatEnum, tuple[str, ...]] = {
    WorkFormatEnum.REMOTE: ("удалённая", "удаленная"),
    WorkFormatEnum.OFFICE: ("на месте работодателя", "офис"),
    WorkFormatEnum.HYBRID: ("гибрид",),
}
