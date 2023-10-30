import aioboto3
import aiohttp
from dependency_injector import containers, providers

from s3upload.config import Config
from s3upload.interactors import AiohttpDownloader, S3Uploader
from s3upload.task import TaskExecutor
from s3upload.utils import resource_from_context


class D(containers.DeclarativeContainer):
    config: providers.Singleton[Config] = providers.Singleton(Config)
    aiohttp_session = providers.Resource(aiohttp.ClientSession)
    boto3_session = providers.Singleton(aioboto3.Session)
    s3_client_context = providers.Factory(
        boto3_session.provided.client.call(
            service_name="s3",
            region_name=config.provided.aws.region,
            aws_access_key_id=config.provided.aws.key,
            aws_secret_access_key=config.provided.aws.secret,
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
        TaskExecutor, downloader=downloader, uploader=uploader
    )
