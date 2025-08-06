__all__ = [
    "FINGERPRINT_SIMILARITY_THRESHOLD",
    "FINGERPRINT_STOPWORDS",
]

# Процент схожести между двумя fingerprint вакансий
FINGERPRINT_SIMILARITY_THRESHOLD = 0.75

# Слова, которые часто встречаются в описании вакансии
FINGERPRINT_STOPWORDS: set[str] = {
    "и",
    "с",
    "в",
}
