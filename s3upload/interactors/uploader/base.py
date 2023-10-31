from abc import ABC, abstractmethod


class Uploader(ABC):
    @abstractmethod
    async def upload(self, path: str, content: bytes) -> None:
        raise NotImplementedError
