import asyncio
import os
from functools import wraps
from pathlib import Path
from typing import (
    Any,
    AsyncContextManager,
    AsyncGenerator,
    Callable,
    Coroutine,
)


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
    root_dir = Path(os.path.dirname(os.path.dirname(__file__)))
    return root_dir / "config.yaml"
