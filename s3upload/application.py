from pathlib import Path
from uuid import uuid4

from dependency_injector.wiring import Provide, inject

from s3upload.config import load_config_from_yaml
from s3upload.container import D
from s3upload.task import Task, TaskExecutor


class Application:
    def __init__(
        self,
        urls: list[str],
        bucket: str,
        workers_count: int,
        config_path: Path,
    ) -> None:
        self.urls: list[str] = urls
        self.bucket: str = bucket
        self.workers_count: int = workers_count
        self.config_path: Path = config_path

    async def __call__(self) -> None:
        config = load_config_from_yaml(self.config_path)
        container = D(config=config)
        container.wire(modules=[__name__])
        await self.main()

    def _create_tasks(self) -> list[Task]:
        return [
            Task(
                download_url=url,
                s3_bucket=self.bucket,
                upload_path=f"{uuid4().hex}.zip",
            )
            for url in self.urls
        ]

    @inject
    async def main(
        self, executor: TaskExecutor = Provide[D.task_executor]
    ) -> None:
        for task in self._create_tasks():
            await executor.execute(task)
