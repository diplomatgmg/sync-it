from parsers.schemas import TelegramChannelUrl


__all__ = ["channel_links"]


channel_usernames: set[str] = {
    "YotolabPython",
    "it_match_python",
    "easy_python_job",
    "vacancy_it_ulbitv",
    "python_djangojobs",
}

channel_links: set[TelegramChannelUrl] = {TelegramChannelUrl.create(u) for u in channel_usernames}
