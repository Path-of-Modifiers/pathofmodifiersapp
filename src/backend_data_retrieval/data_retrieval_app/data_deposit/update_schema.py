from backend_api.app.core.schemas.modifier import ModifierCreate
from pydantic import BaseModel, model_validator


class UpdateJSONSchemaBase(BaseModel):
    old: str | list[str]
    new: str | list[str] | None = None
    set_deprecated: bool = False
    remove: bool = False
    patch: bool = False
    post: bool = False

    @model_validator(mode="after")
    def validate_only_one_true(self) -> "UpdateJSONSchemaBase":
        if sum([self.remove, self.patch, self.post]) != 1:
            raise ValueError(
                "One of remove, patch, or post must (and only one may) be true"
            )

        return self


class ModifierUpdateJSONSchema(UpdateJSONSchemaBase, ModifierCreate):
    @model_validator(mode="before")
    def set_unique_key(cls, data: dict):
        if isinstance(data["old"], list) or isinstance(data["new"], list):
            raise RuntimeError("Old or new cannot be a list")

        data.setdefault("effect", data["old"])

        return data
