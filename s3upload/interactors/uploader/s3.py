from io import BytesIO

from botocore.exceptions import ClientError

from s3upload.exceptions import UploadException
from s3upload.interactors.uploader.base import Uploader
from s3upload.protocols.s3 import S3Client


class S3Uploader(Uploader):
    def __init__(self, s3: S3Client) -> None:
        self.s3: S3Client = s3

    async def upload(self, path: str, content: bytes) -> None:
        bucket, blob_s3_key = path.split("/", 1)
        try:
            await self.s3.upload_fileobj(BytesIO(content), bucket, blob_s3_key)
        except ClientError as e:
            raise UploadException(str(e))
