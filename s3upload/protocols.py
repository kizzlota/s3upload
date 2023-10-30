from typing import BinaryIO, Protocol


class S3Client(Protocol):
    async def upload_fileobj(
        self, stream: BinaryIO, bucket: str, blob_s3_key: str
    ) -> None:
        raise NotImplementedError
