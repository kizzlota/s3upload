from unittest.mock import patch

import pytest
from mocks.downloader import TestDownloader
from mocks.uploader import TestUploader

from s3upload.interactors.downloader.base import DownloadResult
from s3upload.task.base import Task
from s3upload.task.impl import TaskExecutorImpl


@pytest.fixture
def task():
    yield Task("example.com", "test_bucket")


@pytest.mark.asyncio
async def test_executor_download(task: Task) -> None:
    with patch.object(TestDownloader, "download") as DownloaderMock:
        executor = TaskExecutorImpl(
            downloader=TestDownloader(
                result=DownloadResult(
                    content=b"test_content", filename="test_filename.test"
                )
            ),
            uploader=TestUploader(),
        )

        await executor.execute(task)

        DownloaderMock.assert_called_once_with(task.download_url)


@pytest.mark.asyncio
async def test_executor_upload(task: Task) -> None:
    with patch.object(TestUploader, "upload") as UploaderMock:
        executor = TaskExecutorImpl(
            downloader=TestDownloader(
                result=DownloadResult(
                    content=b"test_content", filename="test_filename.test"
                )
            ),
            uploader=TestUploader(),
        )

        await executor.execute(task)

        UploaderMock.assert_called_once_with(
            f"{task.s3_bucket}/test_filename.test", b"test_content"
        )
