from abc import ABC, abstractmethod
from io import BytesIO

from aiohttp import ClientSession

from s3upload.protocols import S3Client


class Downloader(ABC):
    @abstractmethod
    async def download(self, url: str) -> bytes:
        raise NotImplementedError


class Uploader(ABC):
    @abstractmethod
    async def upload(self, path: str, content: bytes) -> None:
        raise NotImplementedError


class AiohttpDownloader(Downloader):
    def __init__(
        self,
        session: ClientSession,
    ) -> None:
        self.session: ClientSession = session

    async def download(self, url: str) -> bytes:
        async with self.session.get(url) as response:
            content = await response.read()
        return content


class S3Uploader(Uploader):
    def __init__(self, s3: S3Client) -> None:
        self.s3: S3Client = s3

    async def upload(self, path: str, content: bytes) -> None:
        bucket, blob_s3_key = path.split("/", 1)
        await self.s3.upload_fileobj(BytesIO(content), bucket, blob_s3_key)
