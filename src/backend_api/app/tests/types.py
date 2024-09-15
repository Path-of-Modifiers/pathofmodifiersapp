from collections.abc import Awaitable, Callable
from typing import Any

from app.crud.base import ModelType

AsyncFunction = Callable[[Any, Any], Awaitable[Any]]

ObjectGeneratorFunc = Callable[[], tuple[dict, ModelType]]
