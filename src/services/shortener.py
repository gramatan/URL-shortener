"""Services for URL Shortener."""
import validators


class ShortenerService:
    """Service for URL Shortener."""

    def __init__(self, url_storage: list):
        """
        Service for URL Shortener.

        Args:
            url_storage: memory storage.
        """
        self.url_storage = url_storage

    async def get_short(
        self,
        long_url: str,
    ):
        """
        Save long url to the storage and return short url.

        Args:
            long_url: long url

        Returns:
            str: short url
        """
        if not validators.url(long_url):
            if not validators.url(f'http://{long_url}'):  # noqa: WPS504
                return None
            else:
                long_url = f'http://{long_url}'

        self.url_storage.append(long_url)
        return str(len(self.url_storage) - 1)

    async def get_long(
        self,
        short_url: str,
    ):
        """
        Get long url by the short url.

        Args:
            short_url: short url.

        Returns:
            str: long url.
        """
        try:
            if 0 <= int(short_url) < len(self.url_storage):
                return self.url_storage[int(short_url)]
        except Exception:
            return None
