import asyncio

from s3upload.interactors.uploader.base import Uploader


class TestUploader(Uploader):
    def __init__(self, *, delay: int | None = None) -> None:
        self.delay: int | None = delay

    async def upload(self, path: str, content: bytes) -> None:
        if self.delay is not None:
            await asyncio.sleep(self.delay)
