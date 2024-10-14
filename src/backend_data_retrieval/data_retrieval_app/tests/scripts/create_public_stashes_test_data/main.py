import copy
import json
import os
import sys
from collections.abc import Iterator

# TODO: REMOVE:
# Be in dir src.backend_data_retrieval before executing this script
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.././.."))
)
from data_retrieval_app.logs.logger import test_logger
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.utils.data_deposit_test_data_creator import (
    DataDepositTestDataCreator,
)
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.utils.scrap_and_mock_poe_api_docs_objs import (
    ScrapAndMockPoEAPIDocsObjs,
)
from data_retrieval_app.tests.utils import (
    replace_false_values,
)

# from data_retrieval_app.logs.logger import setup_logging
# TODO: Remove soon:
output_test_data_location_path = "data_retrieval_app/tests/test_data/"  #


def iterate_create_public_stashes_test_data() -> Iterator[tuple[int, str, list[dict]]]:
    scrap_and_mock_poe_api_docs_objs = ScrapAndMockPoEAPIDocsObjs()
    (
        public_stashes_mock_obj,
        item_mock_obj,
    ) = scrap_and_mock_poe_api_docs_objs.produce_mocks_from_docs()
    public_stashes_modifier_test_data_creator = DataDepositTestDataCreator(
        n_of_items=1000
    )

    for index, (
        modifier_file_name,
        items,
    ) in enumerate(
        public_stashes_modifier_test_data_creator.create_test_data_with_data_deposit_files()
    ):
        test_logger.info(f"Creating test data for file '{modifier_file_name}'")
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
def main():
    # setup_logging() #TODO Setup logging for script if needed
    for i, modifier_file_name, all_stashes in iterate_create_public_stashes_test_data():
        with open(
            f"{output_test_data_location_path}{i}_{modifier_file_name}.json", "w"
        ) as f:
            json.dump(all_stashes, f, indent=4)


if __name__ == "__main__":
    main()
