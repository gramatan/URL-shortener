"""Repo for shortener."""
from config.config import URL_CHARS


class URLRepository:
    """Repo for shortener."""

    def __init__(self, url_storage: list):
        """
        Repo for shortener.

        Args:
            url_storage: storage for urls.
        """
        self.url_storage = url_storage
        self.allowed_chars = URL_CHARS
        self.base = len(self.allowed_chars)

    def encode(self, index: int) -> str:
        """
        Encode index to short url.

        Args:
            index: URL index in storage.

        Returns:
            str: short url.
        """
        chars = []
        while index:
            chars.append(self.allowed_chars[index % self.base])
            index //= self.base
        return ''.join(reversed(chars)) or self.allowed_chars[0]

    def decode(self, short_url: str) -> int:
        """
        Decode short url to index.

        Args:
            short_url: short url.

        Returns:
            int: index in storage.
        """
        index = 0
        for char in short_url:
            index = index * self.base + self.allowed_chars.index(char)
        return index

    async def store(self, long_url: str) -> str:
        """
        Store long url to storage and return short url.

        Args:
            long_url: long url.

        Returns:
            str: short url.
        """
        if long_url in self.url_storage:
            return self.encode(self.url_storage.index(long_url))

        self.url_storage.append(long_url)
        return self.encode(len(self.url_storage) - 1)

    async def retrieve(self, short_url: str) -> str | None:
        """
        Retrieve long url by short url.

        Args:
            short_url: short url.

        Returns:
            str | None: long url or nothing.
        """
        index = self.decode(short_url)
        if 0 <= index < len(self.url_storage):
            return self.url_storage[index]
        return None
