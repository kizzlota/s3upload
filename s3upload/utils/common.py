import asyncio
import os
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import (
    Any,
    AsyncContextManager,
    AsyncGenerator,
    Callable,
    Coroutine,
)
from uuid import uuid4


def coroutine(func: Callable[..., Coroutine]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> None:
        asyncio.run(func(*args, **kwargs))

    return wrapper


async def resource_from_context(
    context: AsyncContextManager,
) -> AsyncGenerator:
    async with context as resource:
        yield resource


def resolve_default_config() -> Path:
    root_dir = Path(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    return root_dir / "config.yaml"


def generate_filename() -> str:
    return f"{uuid4().hex}_{datetime.utcnow().strftime('%Y-%m-%d-%H-%M')}.zip"
