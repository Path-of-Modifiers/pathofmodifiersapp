# Path of Modifiers Application :game_die:

Website application for analyzing prices on items with customized parameters plotted on graphs in Path of Exile.

## :pencil: Technology Stack and Features

- [FastAPI](https://fastapi.tiangolo.com/) for the Python backend API.
- [SQLAlchemy](https://www.sqlalchemy.org/) for the Python SQL database interactions (ORM).
- [Pydantic](https://docs.pydantic.dev/latest/) for data validation and settings management.
- [TimescaleDB](https://www.timescale.com/) for both transactional and analytical processing database.
- [Redis](https://redis.io/) as a cache for tokens and rate limit tracking
- [Alembic](https://alembic.sqlalchemy.org/en/latest/front.html) to automate migrations to database
- Continous stream requests to official [PoE API endpoints](https://www.pathofexile.com/developer/docs) written in threaded Python
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

- Introduce other uniques where rolls matter
- Introduce synthesis implicit tracking
- Introduce fractured explicit tracking

## Dashboard - Front page

![Screenshot from 2024-08-13 13-34-17](https://github.com/user-attachments/assets/d76d8eb4-a2c0-412d-88d3-ddeaeb1ee58b)


## Dashboard - Query Parameters for Glorious Vanity

![Screenshot from 2024-08-13 13-35-25](https://github.com/user-attachments/assets/31c6a824-b490-4988-8f2c-19a773a74e44)


## Dashboard - Plot graph

![Screenshot from 2024-08-13 13-36-01](https://github.com/user-attachments/assets/381764e4-8b3e-46dd-9a63-0903eb9b6392)


## How it works

Path of Modifiers uses a continous data retrieval system consuming [Path of Exile's Public Stashes Endpoint](https://www.pathofexile.com/developer/docs/reference#publicstashes), submitting new data to the database every ~10-15 minutes.

The data is stored with its parameters used for querying. When queried, the data is aggregated and uses several methods to calculate the exchange rates between currencies, items and their modifiers. Secret methods are used to calculate the prizes to counteract price manipulation. Currently prices are displayed for every 10 minutes.

User are able to query items with their specified interest through the user interface. A graph gets generated based on the user's specifications.
