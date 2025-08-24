from bs4 import BeautifulSoup
from common.logger import get_logger
from schemas import ChannelMessageSchema


__all__ = ["TelegramParser"]


logger = get_logger(__name__)


class TelegramParser:
    @staticmethod
    def parse_message_id(html_content: str) -> int:
        soup = BeautifulSoup(html_content, "html.parser")
        last_message_widget = soup.select("div.tgme_widget_message")[-1]
        data_post = last_message_widget.attrs["data-post"]

        return int(str(data_post).split("/")[-1])

    @staticmethod
    def parse_detailed_message(
        html_content: str, channel_username: str, message_id: int
    ) -> ChannelMessageSchema | None:
        soup = BeautifulSoup(html_content, "html.parser")
        data_post_value = f"{channel_username}/{message_id}"

        message_block = soup.select_one(f'div.tgme_widget_message[data-post="{data_post_value}"]')
        if message_block is None:
            # Если сообщение удалено
            logger.info("Message with id %s was deleted", message_id)
            return None

        data_post = message_block.attrs.get("data-post")
        if data_post != data_post_value:
            logger.error(
                "Data-post value mismatch for message with id %s. Expected %s, got %s",
                message_id,
                data_post_value,
                data_post,
            )
            return None

        is_not_supported_message = message_block.select_one("div.message_media_not_supported")
        # Сообщение не поддерживается: Please open Telegram to view this post
        if is_not_supported_message is not None:
            logger.info("Message with id %s is not supported", message_id)
            return None

        message_text_block = message_block.select_one("div.tgme_widget_message_text")
        # Если в сообщении нет текста (Только картинки, видео, документы и т.д.)
        if message_text_block is None:
            logger.info("Message text block not found for message with id %s", message_id)
            return None

        message_time_block = message_block.select_one("time.time")
        if message_time_block is None:
            logger.warning("Message time not found for message with id %s", message_id)
            return None

        message_datetime_str = str(message_time_block.attrs["datetime"])

        for br in message_text_block.find_all("br"):
            br.replace_with("\n")

        return ChannelMessageSchema(
            id=message_id,
            datetime=message_datetime_str,
            text=message_text_block.get_text().strip(),
        )
