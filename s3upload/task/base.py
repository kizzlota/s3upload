from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    download_url: str
    s3_bucket: str


class TaskExecutor(ABC):
    @abstractmethod
    async def execute(self, task: Task) -> None:
        raise NotImplementedError
