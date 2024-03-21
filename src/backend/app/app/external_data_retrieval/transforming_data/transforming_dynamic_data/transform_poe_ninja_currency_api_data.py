import json
from typing import List
import pandas as pd


def load_test_data():
    """
    Temporary test data loader
    """
    with open("testing_data/2024_01_24 22_33.json", encoding="utf8") as infile:
        data = json.load(infile)

    return data
