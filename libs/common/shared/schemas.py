from pydantic import HttpUrl, UrlConstraints


__all__ = ["HttpsUrl"]


class HttpsUrl(HttpUrl):
    """A custom URL type for validating URLs with https scheme."""

    _constraints = UrlConstraints(allowed_schemes=["https"])
