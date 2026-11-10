from backend_api.app.core.schemas.item_base_type import (
    ItemBaseType,
    ItemBaseTypeCreate,
    ItemBaseTypeUpdate,
)

from data_retrieval_app.data_deposit.data_depositor_base import DataDepositorBase
from data_retrieval_app.utils import (
    get_item_base_types,
)


class ItemBaseTypeDataDepositor(
    DataDepositorBase[ItemBaseType, ItemBaseTypeCreate, ItemBaseTypeUpdate]
):
    def __init__(self) -> None:
        super().__init__(data_type="item_base_type", update_model=ItemBaseTypeUpdate)

        self.update_url = str(self.data_url)
        self.data_url += "?on_duplicate_pkey_do_nothing=true"
        self.current_data_by_unique_key = self._get_current_basetypes()

    def _get_current_basetypes(self) -> dict[str, ItemBaseType]:
        basetypes = get_item_base_types(self.pom_auth_headers)

        return {basetype.baseType: basetype for basetype in basetypes}

    def _check_for_complex_updates(self, new_data, current, updated):
        return False, updated

    def _preprocess_data(self, data):
        deposit_basetypes = list[ItemBaseTypeCreate]()
        for basetype in data:
            for key in list(basetype.keys()):
                if basetype[key] == "":
                    basetype.pop(key)

            deposit_basetypes.append(
                ItemBaseTypeCreate(
                    baseType=basetype["baseType"],
                    category=basetype["category"],
                    subCategory=basetype.get("subCategory"),
                )
            )

        return deposit_basetypes

    def _process_data(self, data):
        data = self._remove_duplicates(
            data, primary_key="itemBaseTypeId", unique_key="baseType"
        )
        return data
