import json
from typing import List
import pandas as pd

from app.external_data_retrieval.data_retrieval.poe_ninja_currency_retrieval.poe_ninja_currency_api import PoeNinjaCurrencyAPIHandler


def load_data():
    """
    Loads data from the poe.ninja currency API.
    """
    poe_ninja_currency_api_handler = PoeNinjaCurrencyAPIHandler(
        url="https://poe.ninja/api/data/currencyoverview?league=Affliction&type=Currency"
    )
    
    currencies, currency_details = poe_ninja_currency_api_handler._make_request()
    
    currencies_df = poe_ninja_currency_api_handler._json_to_df(currencies)
    currency_details_df = poe_ninja_currency_api_handler._json_to_df(currency_details)
    
    return currencies_df, currency_details_df


