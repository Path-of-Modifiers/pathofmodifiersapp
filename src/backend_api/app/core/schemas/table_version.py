from dataclasses import dataclass
from typing import Annotated, Any

import pydantic as _pydantic
from packaging.version import Version
from pydantic_core import CoreSchema, core_schema


@dataclass(frozen=True)
class _VersionAnnotation:
    def __get_pydantic_core_schema__(
        self,
        source_type: Any,
        handler: _pydantic.GetCoreSchemaHandler,
    ) -> CoreSchema:
        def validate(value: Any) -> Version:
            if isinstance(value, Version):
                return value
            return Version(value)

        return core_schema.no_info_plain_validator_function(
            validate,
            json_schema_input_schema=core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                str,
                return_schema=core_schema.str_schema(),
            ),
        )


PydanticVersion = Annotated[Version, _VersionAnnotation()]


class TableVersionBase(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True, extra="ignore")

    tableName: str
    version: PydanticVersion


class TableVersion(TableVersionBase):
    pass


class TableVersionCreate(TableVersionBase):
    pass


class TableVersionUpdate(TableVersionBase):
    pass
