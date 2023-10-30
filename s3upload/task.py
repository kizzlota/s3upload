from dataclasses import dataclass

from s3upload.interactors import Downloader, Uploader


@dataclass(frozen=True)
class Task:
    download_url: str
    s3_bucket: str
    upload_path: str


class TaskExecutor:
    def __init__(self, downloader: Downloader, uploader: Uploader) -> None:
        self.downloader: Downloader = downloader
        self.uploader: Uploader = uploader

    async def execute(self, task: Task) -> None:
        content = await self.downloader.download(task.download_url)
        await self.uploader.upload(
            f"{task.s3_bucket}/{task.upload_path}", content
        )
