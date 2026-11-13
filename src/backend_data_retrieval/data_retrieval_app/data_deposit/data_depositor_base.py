import json
import os
from abc import ABC, abstractmethod
from collections.abc import Iterator
from enum import Enum
from pathlib import Path
from typing import Any

from backend_api.app.core.schemas.table_version import TableVersionCreate
from packaging.version import Version
from pydantic import BaseModel, TypeAdapter

from data_retrieval_app.data_deposit.update_schema import UpdateJSONSchemaBase
from data_retrieval_app.data_deposit.utils import read_csv
from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import data_deposit_logger as logger
from data_retrieval_app.pom_api_authentication import (
    get_superuser_token_headers,
)
from data_retrieval_app.utils import get_table_version, send_request_safe


class FileType(Enum):
    NEW_DATA = 1
    UPDATE_DATA = 2


class DataDepositorBase[
    DBModel: BaseModel,
    CreateModel: BaseModel,
    UpdateModel: BaseModel,
    UpdateJSONSchema: UpdateJSONSchemaBase,
](ABC):
    current_data_by_unique_key: dict[tuple[str, ...], DBModel]

    def __init__(
        self,
        *,
        data_type: str,
        unique_key: str | list[str],
        primary_key: str | None = None,
        create_model: type[UpdateModel],
        update_model: type[UpdateModel],
        update_json_schema: type[UpdateJSONSchema] = UpdateJSONSchemaBase,
    ) -> None:
        self.base_url = settings.BACKEND_BASE_URL
        self.pom_auth_headers = get_superuser_token_headers(self.base_url)

        self.new_data_location = (
            f"data_retrieval_app/data_deposit/{data_type}/{data_type}_data"
        )

        data_type_parts = data_type.split("_")
        data_type = data_type_parts.pop(0)
        while data_type_parts:
            data_type += data_type_parts.pop(0).capitalize()
        self.data_type = data_type
        self.data_url = f"{self.base_url}/{data_type}/"

        if unique_key is None:
            unique_key = primary_key
        if isinstance(unique_key, str):
            unique_key = [unique_key]

        self.unique_key = unique_key
        self.primary_key = primary_key

        self.update_model = update_model
        self.create_model = create_model
        self.update_json_schema = update_json_schema

        self.cur_version = get_table_version(self.data_type, self.pom_auth_headers)

    @abstractmethod
    def _set_db_state(self):
        """Retrieves the relevant state of the database"""

    def _load_data(self) -> Iterator[tuple[FileType, list[dict[str, Any]]]]:
        versions = list[Version]()
        for version_dir in os.listdir(self.new_data_location):
            version = Version(version_dir)
            if self.cur_version is None or version > Version(
                "1.0"
            ):  # self.cur_version.version:
                versions.append(version)
            else:
                logger.info(f"Skipping {version=} for {self.data_type}")

        versions.sort()
        for version in versions:
            dir_path = Path(self.new_data_location, str(version))
            for filename in os.listdir(dir_path):
                filepath = dir_path / filename

                logger.info(f"Loading new data from '{filename}'.")
                if filename.endswith(".csv"):
                    data, self.logged_file_comments = read_csv(filepath, logger=logger)
                    yield FileType.NEW_DATA, data
                elif filename.endswith(".json"):
                    with open(filepath) as infile:
                        data = json.load(infile)
                    yield FileType.UPDATE_DATA, data
                else:
                    raise NotImplementedError

        if self.cur_version is None:
            method = "post"

        elif version > self.cur_version.version:
            method = "put"
        else:
            return

        send_request_safe(
            method,
            f"{self.base_url}/tableVersion/",
            json=TableVersionCreate(
                tableName=self.data_type, version=version
            ).model_dump(),
            headers=self.pom_auth_headers,
            logger=logger,
        )

    def _check_for_simple_updates(
        self,
        new_data: CreateModel,
        current: DBModel,
        updated: UpdateModel,
        skip_fields: list[str] | None,
    ) -> tuple[bool, UpdateModel]:
        need_update = False
        for field in new_data.model_fields:
            if skip_fields is not None and field in skip_fields:
                continue

            new = getattr(new_data, field)
            old = getattr(current, field)
            if not (new == old or (isinstance(old, bool) and old)):
                # update rows which have a different value
                # ignore rows which are bools that are already True
                setattr(updated, field, new)
                need_update = True

        return need_update, updated

    @abstractmethod
    def _check_for_complex_updates(
        self, new_data: CreateModel, current: DBModel, updated: UpdateModel
    ) -> tuple[bool, UpdateModel]:
        """Performs more complex logic for checking for updates"""

    def _check_for_updates(
        self,
        new_data: CreateModel,
        current: DBModel,
        skip_fields: list[str] | None = None,
    ) -> bool:
        updated = self.update_model.model_validate(
            {self.primary_key: getattr(current, self.primary_key)}
        )
        need_simple_update, updated = self._check_for_simple_updates(
            new_data, current, updated, skip_fields
        )

        need_complex_update, updated = self._check_for_complex_updates(
            new_data, current, updated
        )

        need_update = need_simple_update or need_complex_update
        if need_update:
            send_request_safe(
                "put",
                self.data_url,
                json=updated.model_dump(exclude_none=True, exclude_unset=True),
                headers=self.pom_auth_headers,
                logger=logger,
            )

        return need_update

    def _get_unique_key_val(self, datum: CreateModel) -> tuple[str]:
        return tuple(getattr(datum, key) for key in self.unique_key)

    def _set_unique_key_val(
        self, datum: CreateModel, vals: Any | list[Any]
    ) -> tuple[str]:
        if not isinstance(vals, list):
            vals = [vals]

        for key, val in zip(self.unique_key, vals, strict=True):
            setattr(datum, key, val)

    def _set_updated_fields(self, model: BaseModel, update_datum: UpdateJSONSchema):
        base_fields = set(UpdateJSONSchemaBase.model_fields)
        child_fields = update_datum.model_fields_set

        extra_fields = child_fields - base_fields - set(self.unique_key)
        for field in extra_fields:
            updated_val = getattr(update_datum, field)
            setattr(model, field, updated_val)

    def _remove_duplicates(
        self,
        data: list[CreateModel],
        *,
        skip_fields: list[str] | None = None,
    ) -> list[CreateModel]:
        non_duplicates = dict[tuple[str], CreateModel]()
        did_update = False

        for datum in data:
            unique_key_val = self._get_unique_key_val(datum)
            if unique_key_val in self.current_data_by_unique_key:
                did_update = (
                    self._check_for_updates(
                        datum,
                        self.current_data_by_unique_key[unique_key_val],
                        skip_fields,
                    )
                    or did_update
                )
                continue

            if unique_key_val in non_duplicates:
                raise ValueError(
                    f"Found the same instance twice (first: {non_duplicates[unique_key_val]}, second: {datum})"
                )

            non_duplicates[unique_key_val] = datum

        if did_update:
            logger.info(f"Updated {self.data_type} using new data")

        return list(non_duplicates.values())

    def _post_update(self, updated: UpdateModel):
        send_request_safe(
            "put",
            self.data_url,
            json=updated.model_dump(exclude_none=True, exclude_unset=True),
            headers=self.pom_auth_headers,
            logger=logger,
        )

    @abstractmethod
    def _preprocess_new_data(self, data: list[dict[str, str]]) -> list[CreateModel]:
        """Turns csv data into the pydantic model"""

    @abstractmethod
    def _process_new_data(self, data: list[CreateModel]) -> list[CreateModel]:
        """Finishes processing the data"""

    def _process_update_data(
        self,
        raw_data: list[dict[str, Any]],
    ) -> list[CreateModel]:
        data = TypeAdapter(list[self.update_json_schema]).validate_python(raw_data)
        # to_be_removed_pks = []
        to_be_updated = list[UpdateModel]()
        to_be_posted = list[CreateModel]()

        for data_update in data:
            # TODO make this more generic
            unique_key_val = (data_update.old,)
            if unique_key_val not in self.current_data_by_unique_key:
                raise RuntimeError(
                    f"Tried to update something that does not exist, unique key value: {data_update.old}"
                )

            old = self.current_data_by_unique_key[unique_key_val]

            clone = TypeAdapter(self.create_model).validate_python(old.model_dump())
            if data_update.remove:
                # to_be_removed_pks.append(getattr(old, primary_key))
                raise NotImplementedError
            elif data_update.patch:
                self._set_updated_fields[UpdateJSONSchema](clone, data_update)
                to_be_updated.append(clone)
            elif data_update.post:
                if data_update.set_deprecated:
                    old_update = TypeAdapter(self.update_model).validate_python(
                        {**old.model_dump(), "deprecated": True}
                    )
                    to_be_updated.append(old_update)

                self._set_unique_key_val(clone, data_update.new)
                self._set_updated_fields(clone, data_update)

                to_be_posted.append(clone)

        for updated in to_be_updated:
            send_request_safe(
                "put",
                self.data_url,
                json=updated.model_dump(exclude_none=True, exclude_unset=True),
                headers=self.pom_auth_headers,
                logger=logger,
            )

        return to_be_posted

    def _insert_data(self, data: list[CreateModel]) -> None:
        if not data:
            return

        logger.info("Inserting data into database.")
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        headers.update(self.pom_auth_headers)
        send_request_safe(
            "post",
            self.data_url,
            json=TypeAdapter(list[CreateModel]).dump_python(data),
            headers=headers,
        )

        logger.info("Successfully inserted data into database.")

    def deposit_data(self) -> None:
        for filetype, raw_data in self._load_data():
            self._set_db_state()
            if filetype == FileType.NEW_DATA:
                data = self._preprocess_new_data(raw_data)
            elif filetype == FileType.UPDATE_DATA:
                data = self._process_update_data(raw_data)

            data = self._process_new_data(data)
            self._insert_data(data)
