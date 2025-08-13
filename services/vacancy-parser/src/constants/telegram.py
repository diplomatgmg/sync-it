from schemas_old import TelegramChannelUrl


__all__ = ["channel_links"]


channel_usernames: set[str] = {
    "YotolabPython",
    "it_match_python",
    "easy_python_job",
    "vacancy_it_ulbitv",
    "python_djangojobs",
}

channel_links: set[TelegramChannelUrl] = {TelegramChannelUrl.create(username) for username in channel_usernames}
