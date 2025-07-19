import copy
import json
from collections.abc import Iterator
from typing import Any

from data_retrieval_app.logs.logger import test_logger
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.config import (
    script_settings,
)
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.utils.data_deposit_test_data_creator import (
    DataDepositTestDataCreator,
)
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.utils.scrap_and_mock_poe_api_docs_objs import (
    ScrapAndMockPoEAPIDocs,
)
from data_retrieval_app.tests.utils import (
    replace_false_values,
)

OUTPUT_TEST_DATA_LOCATION_PATH = "data_retrieval_app/tests/test_data/"


class PublicStashMockAPI:
    def __init__(self) -> None:
        scrap_and_mock_poe_api_docs_objs = ScrapAndMockPoEAPIDocs()
        (
            self.public_stashes_mock_obj,
            self.item_mock_obj,
        ) = scrap_and_mock_poe_api_docs_objs.produce_mocks_from_docs()

        self.public_stashes_modifier_test_data_creator = DataDepositTestDataCreator(
            n_of_items=script_settings.N_OF_ITEMS_PER_MODIFIER_FILE
        )
        self.public_stashes_modifier_test_data_creator.create_templates()
        self.leagues = [
            *script_settings.SOFTCORE_LEAGUES,
            *script_settings.HARDCORE_LEAGUES,
        ]

    def get_test_data(self) -> list[dict[str, Any]]:
        """Generates test data by modifying mock stashes and items based on league."""

        # Create base stashes for each league
        stashes = [
            replace_false_values(copy.deepcopy(self.public_stashes_mock_obj))
            | {"league": league}
            for league in self.leagues
        ]
        league_to_idx = {league: i for i, league in enumerate(self.leagues)}

        # Process modifier test data
        for (
            filename,
            items,
        ) in self.public_stashes_modifier_test_data_creator.create_test_data():
            test_logger.debug(f"Creating test data for file '{filename}'")
            for item in items:
                # Merge mocks and process item
                merged_item = replace_false_values(
                    copy.deepcopy({**self.item_mock_obj, **item})
                )
                stashes[league_to_idx[merged_item["league"]]]["items"].append(
                    merged_item
                )

        return stashes


def iterate_create_public_stashes_test_data() -> (
    Iterator[tuple[int, str, list[dict[str, Any]]]]
):
    scrap_and_mock_poe_api_docs_objs = ScrapAndMockPoEAPIDocs()
    (
        public_stashes_mock_obj,
        item_mock_obj,
    ) = scrap_and_mock_poe_api_docs_objs.produce_mocks_from_docs()
    public_stashes_modifier_test_data_creator = DataDepositTestDataCreator(
        n_of_items=script_settings.N_OF_ITEMS_PER_MODIFIER_FILE
    )
    public_stashes_modifier_test_data_creator.create_templates()

    for index, (
        modifier_file_name,
        items,
    ) in enumerate(public_stashes_modifier_test_data_creator.create_test_data()):
        test_logger.debug(f"Creating test data for file '{modifier_file_name}'")
        all_stashes = []
        current_public_stashes_mock_modified = replace_false_values(
            copy.deepcopy(public_stashes_mock_obj)
        )
        for item in items:
            merged_complete_item_dict = {**item_mock_obj, **item}
            merged_complete_item_dict_modified = replace_false_values(
                copy.deepcopy(merged_complete_item_dict)
            )
            current_public_stashes_mock_modified["items"].append(
                merged_complete_item_dict_modified
            )

        all_stashes.append(current_public_stashes_mock_modified)

        yield index, modifier_file_name, all_stashes


# Script that creates test data for public_stashes
# NOTE: The POE api docs mocks are mocked only to this applications' interests. So some key-attribute values are not the same
# as in the POE api docs. This is due to our lazyness since many key-attributes gets filtered anyway.
def main() -> None:
    # setup_logging() #TODO Setup logging for script if needed
    for i, modifier_file_name, all_stashes in iterate_create_public_stashes_test_data():
        with open(
            f"{OUTPUT_TEST_DATA_LOCATION_PATH}{i}_{modifier_file_name}.json", "w"
        ) as f:
            json.dump(all_stashes, f, indent=4)


if __name__ == "__main__":
    main()
