import asyncio

from app.external_data_retrieval.data_retrieval.poe_api_retrieval.poe_api import (
    APIHandler,
)


def main():
    auth_token = "750d4f685cfa83d024d86508e7ede4ab55b5acc7"
    url = "https://api.pathofexile.com/public-stash-tabs"

    n_wanted_items = 100
    n_unique_wanted_items = 15

    api_handler = APIHandler(
        url=url,
        auth_token=auth_token,
        n_wanted_items=n_wanted_items,
        n_unique_wanted_items=n_unique_wanted_items,
    )
    for df in api_handler.dump_stream(
        initial_next_change_id="2304265269-2292493816-2218568823-2460180973-2390424272"
    ):  # From poe.ninja
        print(df)
        df.to_csv("test.csv", index=False)
        quit()

    return 0


if __name__ == "__main__":
    main()
