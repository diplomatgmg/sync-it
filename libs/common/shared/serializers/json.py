from typing import Any

from common.shared.serializers import AbstractSerializer
import orjson


__all__ = ["JSONSerializer"]


class JSONSerializer(AbstractSerializer):
    def serialize(self, obj: Any) -> bytes:  # noqa: PLR6301
        return orjson.dumps(obj)

    def deserialize(self, obj: bytes) -> Any:  # noqa: PLR6301
        return orjson.loads(obj)
