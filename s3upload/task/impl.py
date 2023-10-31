from s3upload.interactors.downloader.base import Downloader
from s3upload.interactors.uploader.base import Uploader
from s3upload.task.base import Task, TaskExecutor
from s3upload.utils.common import generate_filename
from s3upload.utils.logger import logger


class TaskExecutorImpl(TaskExecutor):
    def __init__(self, downloader: Downloader, uploader: Uploader) -> None:
        self.downloader: Downloader = downloader
        self.uploader: Uploader = uploader

    async def execute(self, task: Task) -> None:
        logger.debug("waiting for acquire semaphore")
        logger.info(f"Downloading file. URL: {task.download_url}")
        result = await self.downloader.download(task.download_url)
        filename = result.filename or generate_filename()
        logger.info(f"Uploading file: {filename}")
        await self.uploader.upload(
            f"{task.s3_bucket}/{filename}",
            result.content,
        )
