import asyncio

from s3upload.interactors.downloader.base import Downloader, DownloadResult


class TestDownloader(Downloader):
    def __init__(
        self, result: DownloadResult, *, delay: int | None = None
    ) -> None:
        self.result: DownloadResult = result
        self.delay: int | None = delay

    async def download(self, url: str) -> DownloadResult:
        if self.delay is not None:
            await asyncio.sleep(self.delay)
        return self.result
