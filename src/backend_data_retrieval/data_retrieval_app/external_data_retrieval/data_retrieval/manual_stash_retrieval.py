import json
import os

from pydantic import TypeAdapter

from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.poe import (
    Stash,
)


def filter_by_owner(stashes: list[Stash], *owners: str) -> list[Stash] | None:
    interesting_stashes = list[Stash]()
    for stash in stashes:
        if stash.account_name in owners:
            interesting_stashes.append(stash)

    if len(interesting_stashes) == 0:
        return None

    return interesting_stashes


def stashes_to_json(next_change_id: str, stashes: list[Stash]):
    if not os.path.exists("stashes"):
        os.mkdir("stashes")
    with open(f"stashes/{next_change_id}.json", "w") as file:
        json.dump(TypeAdapter(list[Stash]).dump_python(stashes), file)
