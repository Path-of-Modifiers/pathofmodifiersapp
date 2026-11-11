import os
from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, TypeAdapter

from data_retrieval_app.data_deposit.utils import read_csv
from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import data_deposit_logger as logger
from data_retrieval_app.pom_api_authentication import (
    get_superuser_token_headers,
)
from data_retrieval_app.utils import send_request_safe


class DataDepositorBase[
    DBModel: BaseModel,
    CreateModel: BaseModel,
    UpdateModel: BaseModel,
](ABC):
    current_data_by_unique_key: dict[str, DBModel]

    def __init__(
        self,
        data_type: Literal["modifier", "item_base_type", "league"],
        update_model: type[UpdateModel],
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

        self.update_model = update_model

    @abstractmethod
    def _set_db_state(self):
        """Retrieves the relevant state of the database"""

    def _load_data(self) -> Iterator[list[dict[str, str]]]:
        for filename in os.listdir(self.new_data_location):
            filepath = Path(self.new_data_location, filename)

            logger.info(f"Loading new data from '{filename}'.")
            data, self.logged_file_comments = read_csv(filepath, logger=logger)

            yield data

    def _check_for_simple_updates(
        self,
        new_data: CreateModel,
        current: DBModel,
        primary_key: str,
        skip_fields: list[str] | None,
    ) -> tuple[bool, UpdateModel]:
        need_update = False
        updated = self.update_model.model_validate(
            {primary_key: getattr(current, primary_key)}
        )
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
        primary_key: str,
        skip_fields: list[str] | None = None,
    ) -> bool:
        need_simple_update, updated = self._check_for_simple_updates(
            new_data, current, primary_key, skip_fields
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

    def _get_unique_key_val(
        self, datum: CreateModel, unique_key: str | list[str]
    ) -> tuple[str]:
        if isinstance(unique_key, str):
            unique_key = [unique_key]

        return tuple(getattr(datum, key) for key in unique_key)

    def _remove_duplicates(
        self,
        data: list[CreateModel],
        *,
        primary_key: str,
        unique_key: str | list[str] | None = None,
        skip_fields: list[str] | None = None,
    ) -> list[CreateModel]:
        if unique_key is None:
            unique_key = primary_key

        non_duplicates = dict[tuple[str], CreateModel]()
        did_update = False

        for datum in data:
            unique_key_val = self._get_unique_key_val(datum, unique_key)
            if unique_key_val in self.current_data_by_unique_key:
                did_update = (
                    self._check_for_updates(
                        datum,
                        self.current_data_by_unique_key[unique_key_val],
                        primary_key,
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
    def _preprocess_data(self, data: list[dict[str, str]]) -> list[CreateModel]:
        """Turns csv data into the pydantic model"""

    @abstractmethod
    def _process_data(self, data: list[CreateModel]) -> list[CreateModel]:
        """Finishes processing the data"""

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
        self._set_db_state()
        for raw_data in self._load_data():
            data = self._preprocess_data(raw_data)
            data = self._process_data(data)
            self._insert_data(data)
