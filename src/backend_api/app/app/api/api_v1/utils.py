from typing import Dict


def get_delete_return_message(
    prefix: str,
    mapping: Dict[str, str],
) -> str:
    """Returns a message indicating the object was deleted successfully.

    Args:
        prefix (str): Route prefix for the object.
        unique_identifier (str): Unique identifier for the object (main primary key name).
        unique_identifier_value (str): Value of the unique identifier.

    Returns:
        str: Message indicating the object was deleted successfully.
    """

    return f"{prefix} with mapping ({', '.join([key + ': ' + str(item) for key, item in mapping.items()])}) deleted successfully"
