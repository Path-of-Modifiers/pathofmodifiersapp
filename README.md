# Path of Modifiers Application :game_die:

Website application for analyzing prices on items with customized parameters plotted on graphs in Path of Exile.

## :clapper: How it works trailer :clapper:

https://github.com/user-attachments/assets/0efa4c0e-808c-4223-9a4f-781f886527e3

## :star: Features :star:
- Choose between 31 different uniques
- Search for modifiers you are interested in  
- Use ~ for advanced searches, as you would on trade site
- Select specific rolls, both numerical and text based.
- Combine multiple modifiers (currently only support "and" based queries)
- Choose between prices in Chaos or the most common currency (E.g Divines, Mirros, ect)
- Confidence indicators (still being finetuned)
- Share queries you have made, by sharing the (very big) url
- An API for easier exporting of data (requires login)
- No ads (for now at least)

## :pencil: Technology Stack

- [FastAPI](https://fastapi.tiangolo.com/) for the Python backend API.
- [SQLAlchemy](https://www.sqlalchemy.org/) for the Python SQL database interactions (ORM).
- [Pydantic](https://docs.pydantic.dev/latest/) for data validation and settings management.
- [TimescaleDB](https://www.timescale.com/) for both transactional and analytical processing database.
- [Redis](https://redis.io/) as a cache for tokens and rate limit tracking
- [Alembic](https://alembic.sqlalchemy.org/en/latest/front.html) to automate migrations to database
- Continuous stream requests to official [PoE API endpoints](https://www.pathofexile.com/developer/docs) written in threaded Python
- Unit testing with Pytest
- Homemade scripts to insert test data and test the backend
- [React](https://react.dev/) for the frontend.
- Using TypeScript, hooks, Vite, Tanstack and other tools for the frontend stack.
- [Chakra UI](https://v2.chakra-ui.com/) for the frontend components.
- An automatically generated frontend client through OpenAPI tools.
- [Docker Compose](https://docs.docker.com/compose/) for development and production.
- Tests with [Pytest](https://docs.pytest.org/en/stable/)
- [Cloudflare](https://www.cloudflare.com/en-gb/learning/what-is-cloudflare/) for networking
- [Traefik](https://traefik.io/) as a reverse proxy / load balancer.
- CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.
- [Vector](https://vector.dev/) for observability pipeliner, centralising all logs and metrics
- [Grafana Loki](https://grafana.com/docs/loki/latest/#grafana-loki) for storage and [Grafana](https://grafana.com/grafana/) for visualization of logs and metrics


## :bike: Current goals we are working towards:

- Production testing through the Settlers PoE league
- Comprehensive application testing end-to-end

## :checkered_flag: Future goals:

- More uniques where rolls matter
- Tracking for popular fractures for Non-Unique items
- Tracking for popular synthesis implicit
- Tracking for uniques with corrupted implicits
- Tracking for unidentified uniques
- Smarter queries (E.g count, or, not)
- Support for comparing multiple leagues (kinda hard without a new league)



## How it works

Path of Modifiers uses a continuous data retrieval system consuming [Path of Exile's Public Stashes Endpoint](https://www.pathofexile.com/developer/docs/reference#publicstashes), submitting new data to the database every ~10-15 minutes.

The data is stored with its parameters used for querying. When queried, the data is aggregated and uses several methods to calculate the exchange rates between currencies, items and their modifiers. Secret methods are used to calculate the prizes to counteract price manipulation. Currently prices are displayed for every 10 minutes.

User are able to query items with their specified interest through the user interface. A graph gets generated based on the user's specifications.
