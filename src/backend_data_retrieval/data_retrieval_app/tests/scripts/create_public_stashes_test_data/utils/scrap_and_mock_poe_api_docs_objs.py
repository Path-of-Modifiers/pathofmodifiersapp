import json
import uuid
from typing import Any

import requests
from bs4 import BeautifulSoup

from data_retrieval_app.external_data_retrieval.config import settings


class ScrapAndMockPoEAPIDocsObjs:
    def __init__(self) -> None:
        self.public_stashes_url = "https://www.pathofexile.com/developer/docs/reference#type-PublicStashChange"
        self.public_stashes_schema_id = "type-PublicStashChange"

        self.item_url = "https://www.pathofexile.com/developer/docs/reference#type-Item"
        self.item_schema_id = "type-Item"

    # Fetch the HTML content of the documentation page, simulating a browser request
    def _fetch_schema_from_web(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    # Parse the schema table using BeautifulSoup
    def _scrape_html_to_schema(
        self, html_content: str, schema_id: str
    ) -> list[tuple[str, Any]]:
        soup = BeautifulSoup(html_content, "html.parser")

        # Locate the schema by its id attribute
        schema_heading = soup.find("h3", id=schema_id)

        if not schema_heading:
            raise ValueError(f"Schema '{schema_id}' not found!")

        # Find the next table after the schema heading
        schema_table = schema_heading.find_next("table")

        if schema_table is None:
            raise ValueError(f"Schema table for '{schema_id}' not found!")

        # Extract rows of the table
        rows = schema_table.find_all("tr")

        # Parse the key-value pairs from the rows
        schema_data = []
        last_non_arrow_key = None
        nested_data = {}
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 2:
                key = columns[0].text.strip().replace("↳", "").strip()
                value_type = columns[1].text.strip()

                if "↳" in columns[0].text:
                    # This is a nested key, append it to the nested_data dictionary
                    if last_non_arrow_key:
                        nested_data[key] = value_type
                else:
                    # Add the previous nested data to the last non-arrow key if it exists
                    if last_non_arrow_key and nested_data:
                        schema_data.append((last_non_arrow_key, nested_data))
                        nested_data = {}  # Reset nested data after appending

                    # This is a non-arrow key, reset last_non_arrow_key
                    last_non_arrow_key = key
                    schema_data.append((key, value_type))

        # Handle any remaining nested data after loop
        if last_non_arrow_key and nested_data:
            schema_data.append((last_non_arrow_key, nested_data))

        return schema_data

    def _check_obj_key_value_type(self, obj: dict, key: str, value_type: Any):
        if "id" == key:
            obj[key] = str(uuid.uuid4())
        elif "league" == key:
            obj[key] = settings.CURRENT_SOFTCORE_LEAGUE
        elif "string" == value_type:
            obj[key] = ""
        elif "?string" == value_type:
            obj[key] = ""
        elif "bool" in value_type:
            obj[key] = False
        elif "int" in value_type:
            obj[key] = 0
        elif "array of string" in value_type:
            obj[key] = [""]
        elif "array of object" in value_type:
            obj[key] = []
        elif "array of Item" in value_type:
            obj[key] = []
        else:
            obj[key] = None  # Default self, to None for unknown types

        return obj

    # Create a mock obj with sample values based on the schema
    def _create_mock_obj_from_schema(self, schema_data: list[tuple[str, str]]) -> dict:
        mock_obj = {}

        for key, value_type in schema_data:
            if key == "influences":
                # Set specific influences to False
                mock_obj[key] = {
                    "shaper": False,
                    "elder": False,
                    "crusader": False,
                    "hunter": False,
                    "redeemer": False,
                    "warlord": False,
                }
            elif isinstance(value_type, dict):
                # Handle nested objs inside arrays
                nested_obj = {}
                for nested_key, nested_value_type in value_type.items():
                    nested_obj = self._check_obj_key_value_type(
                        nested_obj, nested_key, nested_value_type
                    )
                mock_obj[key] = [nested_obj]
            else:  # Ensure the parent key holds a list of objs
                mock_obj = self._check_obj_key_value_type(mock_obj, key, value_type)

        return mock_obj

    def _mock_schemas_from_web(self, url: str, schema_id: str) -> dict:
        html_content = self._fetch_schema_from_web(url)

        schema_data = self._scrape_html_to_schema(html_content, schema_id)

        if not schema_data:
            raise ValueError(f"Schema data for '{schema_id}' not found!")

        return self._create_mock_obj_from_schema(schema_data)

    def _remove_unwanted_columns_from_mock_obj(
        self, mock_obj: dict, unwanted_columns: list[str]
    ) -> dict:
        for unwanted_column in unwanted_columns:
            if unwanted_column in mock_obj:
                mock_obj.pop(unwanted_column)
        return mock_obj

    def mock_to_json_file(self, mock_obj: dict) -> str:
        """Save the objs to a JSON file."""
        json_file = json.dumps(mock_obj, indent=4)
        file_path = "data_retrieval_app/tests/test_data/" + mock_obj["id"] + ".json"
        with open(file_path, "w") as outfile:
            outfile.write(json_file)

    def produce_mocks_from_docs(self) -> tuple[dict, dict]:
        """
        Produce mocks from the POE API docs.

        **Returns**
            tuple[dict, dict]: public_stashes_mock_obj, item_mock_obj
        """
        public_stashes_mock_obj = self._mock_schemas_from_web(
            self.public_stashes_url, self.public_stashes_schema_id
        )
        # TODO: Make this filtering columns a global list
        unwanted_columns = [
            "ruthless",
            "lockedToCharacter",
            "lockedToAccount",
            "logbookMods",
            "crucible",
            "scourged",
            "hybrid",
            "ultimatumMods",
        ]
        item_mock_obj = self._mock_schemas_from_web(self.item_url, self.item_schema_id)
        item_mock_removed_unwanted_columns = (
            self._remove_unwanted_columns_from_mock_obj(
                mock_obj=item_mock_obj, unwanted_columns=unwanted_columns
            )
        )
        return public_stashes_mock_obj, item_mock_removed_unwanted_columns
