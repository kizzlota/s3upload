import aioboto3
import aiohttp
from dependency_injector import containers, providers

from s3upload.config import Credentials
from s3upload.interactors.downloader.aiohttp import AiohttpDownloader
from s3upload.interactors.uploader.s3 import S3Uploader
from s3upload.task.impl import TaskExecutorImpl
from s3upload.utils.common import resource_from_context


class D(containers.DeclarativeContainer):
    credentials: providers.Singleton[Credentials] = providers.Singleton(
        Credentials
    )
    aiohttp_session = providers.Resource(aiohttp.ClientSession)
    boto3_session = providers.Singleton(aioboto3.Session)
    s3_client_context = providers.Factory(
        boto3_session.provided.client.call(
            service_name="s3",
            region_name=credentials.provided.region,
            aws_access_key_id=credentials.provided.key,
            aws_secret_access_key=credentials.provided.secret,
        ),
    )
    s3_client = providers.Resource(
        resource_from_context, context=s3_client_context
    )
    downloader = providers.Factory(
        AiohttpDownloader,
        session=aiohttp_session,
    )
    uploader = providers.Factory(S3Uploader, s3=s3_client)
    task_executor = providers.Factory(
        TaskExecutorImpl, downloader=downloader, uploader=uploader
    )
