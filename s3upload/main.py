from pathlib import Path
from typing import Annotated, Final

from typer import Option, Typer

from s3upload.application import Application
from s3upload.utils import coroutine, resolve_default_config

DEFAULT_CONFIG: Final[Path] = resolve_default_config()
DEFAULT_WORKERS: Final[int] = 2

app = Typer()


@app.command()
@coroutine
async def main(
    urls: Annotated[list[str], Option("-u", "--url")],
    bucket: Annotated[str, Option("-b", "--bucket")],
    workers_count: Annotated[int, Option("-w", "--workers")] = DEFAULT_WORKERS,
    config: Annotated[Path, Option("-c", "--config")] = DEFAULT_CONFIG,
) -> None:
    application = Application(urls, bucket, workers_count, config)
    await application()
