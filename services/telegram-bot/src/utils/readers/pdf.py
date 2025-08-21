from pathlib import Path

from pypdf import PdfReader as PyPdfReader
from utils.readers import AbstractFileReader


__all__ = ["PdfReader"]


class PdfReader(AbstractFileReader):
    @staticmethod
    def read(file_path: str) -> str:
        path = Path(file_path)
        with path.open("rb") as file:
            reader = PyPdfReader(file)
            texts = (page.extract_text() for page in reader.pages)

            return "\n".join(text for text in texts if text.strip())
