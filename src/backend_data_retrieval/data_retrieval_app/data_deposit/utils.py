import csv
import logging
from pathlib import Path


def read_csv(
    filepath: Path, *, logger: logging.Logger
) -> tuple[list[dict[str, str]], dict[str, str]]:
    """
    Returns:
        list of lines as dict
        dict of comments
    """
    comments = dict[str, str]()
    with open(filepath) as infile:
        while True:
            position = infile.tell()
            line = infile.readline()

            if not line:
                break

            if line.startswith("#"):
                logger.info(line.rstrip())
                split_line = line[1:].split(":", 1)
                comments[split_line[0].strip()] = split_line[1].strip()
            else:
                # We found the CSV header, so go back to its beginning
                infile.seek(position)
                break

        lines = csv.DictReader(infile)

    return lines, comments
