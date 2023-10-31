from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class DownloadResult:
    content: bytes
    filename: str | None = None


class Downloader(ABC):
    @abstractmethod
    async def download(self, url: str) -> DownloadResult:
        raise NotImplementedError
