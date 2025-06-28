from common.logger import get_logger


__all__ = ["map_to_skill_name"]


logger = get_logger(__name__)


def map_to_skill_name(skill: str) -> str | None:
    skill = skill.lower().strip()

    for skills in skills_map.values():
        for normalized, aliases in skills.items():
            if skill in aliases:
                return normalized

    return None


skills_map: dict[str, dict[str, tuple[str, ...]]] = {
    "languages": {
        "Python": ("python", "python developer"),
        "JavaScript": ("javascript",),
        "TypeScript": ("typescript",),
        "HTML": ("html",),
        "CSS": ("css",),
        "SQL": ("sql",),
    },
    "backend": {
        "Django": ("django",),
        "Flask": ("flask",),
        "FastAPI": ("fastapi",),
    },
    "frontend": {
        "React": ("react",),
        "Vue": ("vue",),
        "Angular": ("angular",),
        "Svelte": ("svelte",),
    },
    "devops": {
        "Docker": ("docker",),
        "Kubernetes": ("kubernetes",),
    },
}
