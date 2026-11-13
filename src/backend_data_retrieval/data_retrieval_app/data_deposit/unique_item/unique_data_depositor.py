from backend_api.app.core.schemas.unique_item import (
    UniqueItem,
    UniqueItemCreate,
    UniqueItemUpdate,
)

from data_retrieval_app.data_deposit.data_depositor_base import DataDepositorBase
from data_retrieval_app.data_deposit.update_schema import UpdateJSONSchemaBase
from data_retrieval_app.utils import get_item_base_type_id_by_name, get_uniques


class UniqueItemDataDepositor(
    DataDepositorBase[
        UniqueItem, UniqueItemCreate, UniqueItemUpdate, UpdateJSONSchemaBase
    ]
):
    def __init__(self) -> None:
        super().__init__(
            data_type="unique_item",
            primary_key="uniqueItemId",
            unique_key=["name", "itemBaseTypeId"],
            create_model=UniqueItemCreate,
            update_model=UniqueItemUpdate,
        )

        self.update_url = str(self.data_url)
        self.data_url += "?on_duplicate_pkey_do_nothing=true"
        self.current_data_by_unique_key = self._get_current_unique_items()

    def _get_current_unique_items(self) -> dict[str, UniqueItem]:
        uniques = get_uniques(self.pom_auth_headers)

        return {(unique.name, unique.itemBaseTypeId): unique for unique in uniques}

    def _check_for_complex_updates(self, new_data, current, updated):
        return False, updated

    def _set_db_state(self):
        self.basetype_id_by_name = get_item_base_type_id_by_name(self.pom_auth_headers)

    def _preprocess_new_data(self, data):
        deposit_uniques = list[UniqueItemCreate]()
        for unique_item in data:
            for key in list(unique_item.keys()):
                if unique_item[key] == "":
                    unique_item.pop(key)

            deposit_uniques.append(
                UniqueItemCreate(
                    name=unique_item["name"],
                    itemBaseTypeId=self.basetype_id_by_name[unique_item["baseType"]],
                    iconSuffix=unique_item.get("iconSuffix"),
                )
            )

        return deposit_uniques

    def _process_new_data(self, data):
        data = self._remove_duplicates(data)
        return data

    def _preprocess_update_data(self, data):
        return None

    def _process_update_data(self, data):
        pass
