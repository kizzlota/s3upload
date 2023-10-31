import asyncio
from asyncio import Semaphore

from dependency_injector.wiring import Provide, inject

from s3upload.config import Credentials
from s3upload.container import D
from s3upload.exceptions import DownloadException, UploadException
from s3upload.task.base import Task, TaskExecutor
from s3upload.utils.logger import logger


async def worker(
    task: Task, executor: TaskExecutor, semaphore: Semaphore
) -> None:
    async with semaphore:
        try:
            await executor.execute(task)
        except DownloadException as e:
            logger.error(f"Exception occur during download file: {str(e)}")
        except UploadException as e:
            logger.error(f"Exception occur during upload file: {str(e)}")


class Application:
    def __init__(
        self,
        urls: list[str],
        bucket: str,
        aws_key: str,
        aws_secret: str,
        aws_region: str,
        workers_count: int,
    ) -> None:
        self.urls: list[str] = urls
        self.bucket: str = bucket
        self.workers_count: int = workers_count
        self.credentials: Credentials = Credentials(
            aws_key, aws_secret, aws_region
        )

    async def __call__(self) -> None:
        container = D(credentials=self.credentials)
        container.wire(modules=[__name__])
        await self.main()

    def _create_tasks(self) -> list[Task]:
        logger.info("Creating tasks")
        tasks = [
            Task(
                download_url=url,
                s3_bucket=self.bucket,
            )
            for url in self.urls
        ]
        return tasks

    @inject
    async def main(
        self, executor: TaskExecutor = Provide[D.task_executor]
    ) -> None:
        logger.debug(
            f"Semaphore locked by number of workers: {self.workers_count}"
        )
        semaphore: Semaphore = Semaphore(self.workers_count)
        tasks = [
            asyncio.create_task(worker(task, executor, semaphore))
            for task in self._create_tasks()
        ]
        await asyncio.gather(*tasks)
