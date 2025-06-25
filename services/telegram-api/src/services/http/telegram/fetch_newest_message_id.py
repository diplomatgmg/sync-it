from bs4 import BeautifulSoup
from common.logger import get_logger
import httpx


__all__ = ["fetch_newest_message_id"]


logger = get_logger(__name__)


async def fetch_newest_message_id(channel_username: str) -> int | None:
    """Возвращает ID самого последнего (новейшего) сообщения из публичного канала."""
    channel_url = f"https://t.me/s/{channel_username}"

    async with httpx.AsyncClient() as client:
        response = await client.get(channel_url)

        # Если это группа, канал закрыт или его не существует
        if response.is_redirect:
            logger.info("Channel %s is not public or does not exist")
            return None

        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    last_message_widget = soup.select("div.tgme_widget_message")[-1]
    data_post = last_message_widget.attrs["data-post"]

    newest_message_id = int(str(data_post).split("/")[-1])
    logger.debug("Newest message id is %s", newest_message_id)

    return newest_message_id
