from aiohttp import ClientConnectorError, ClientSession, InvalidURL

from s3upload.exceptions import DownloadException
from s3upload.interactors.downloader.base import Downloader, DownloadResult
from s3upload.utils.aiohttp import get_filename_from_response


class AiohttpDownloader(Downloader):
    def __init__(
        self,
        session: ClientSession,
    ) -> None:
        self.session: ClientSession = session

    async def download(self, url: str) -> DownloadResult:
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    raise DownloadException(
                        f"Invalid response status:{response.status}"
                    )
                content = await response.read()
                filename = get_filename_from_response(response)
        except (ClientConnectorError, InvalidURL) as e:
            raise DownloadException(repr(e))
        return DownloadResult(content, filename)
