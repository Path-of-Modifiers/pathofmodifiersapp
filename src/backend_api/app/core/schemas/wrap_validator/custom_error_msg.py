from collections.abc import Callable
from typing import Any

from pydantic import (
    ValidationInfo,
    WrapValidator,
)


def custom_error_msg(exc_factory: Callable[[str | None, Exception], Exception]) -> Any:
    def _validator(v: Any, next_: Any, ctx: ValidationInfo) -> Any:
        try:
            return next_(v, ctx)
        except Exception as e:
            raise exc_factory(ctx.field_name, e) from None

    return WrapValidator(_validator)
