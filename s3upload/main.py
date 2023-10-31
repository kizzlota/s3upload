from pathlib import Path
from typing import Annotated, Final

from typer import Option, Typer

from s3upload.application import Application
from s3upload.utils.common import coroutine, resolve_default_config
from s3upload.utils.logger import logger

DEFAULT_CONFIG: Final[Path] = resolve_default_config()
DEFAULT_WORKERS: Final[int] = 2

app = Typer()


@app.command()
@coroutine
async def main(
    urls: Annotated[list[str], Option("-u", "--url")],
    bucket: Annotated[str, Option("-b", "--bucket")],
    aws_key: Annotated[str, Option("--aws-key", "-k")],
    aws_secret: Annotated[str, Option("--aws-secret", "-s")],
    aws_region: Annotated[str, Option("--aws-region", "-r")],
    workers_count: Annotated[int, Option("-w", "--workers")] = DEFAULT_WORKERS,
) -> None:
    logger.debug("Initializing app")
    application = Application(
        urls=urls,
        bucket=bucket,
        aws_key=aws_key,
        aws_secret=aws_secret,
        aws_region=aws_region,
        workers_count=workers_count,
    )
    await application()
