# Path of Modifiers Application :game_die:

Website application for analyzing prices on items with customized parameters plotted on graphs in Path of Exile.

Not officially released, but currently testing in production :smiley:  

## :pencil: Technology Stack and Features

- [FastAPI](https://fastapi.tiangolo.com/) for the Python backend API.
- [SQLAlchemy](https://www.sqlalchemy.org/) for the Python SQL database interactions (ORM).
- [Pydantic](https://docs.pydantic.dev/latest/) for data validation and settings management.
- [PostgreSQL](https://www.postgresql.org/) as the SQL database.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/front.html) to automate migrations to database
- Continous stream requests to official [POE API endpoints](https://www.pathofexile.com/developer/docs) written in threaded Python
- [React](https://react.dev/) for the frontend.
- Using TypeScript, hooks, Vite, Tanstack and other tools for the frontend stack.
- [Chakra UI](https://v2.chakra-ui.com/) for the frontend components.
- An automatically generated frontend client through OpenAPI tools.
- [Docker Compose](https://docs.docker.com/compose/) for development and production.
- Tests with [Pytest](https://docs.pytest.org/en/stable/)
- [Cloudflare](https://www.cloudflare.com/en-gb/learning/what-is-cloudflare/) for networking
- [Traefik](https://traefik.io/) as a reverse proxy / load balancer.
- CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.

## :bike: Current goals we are working towards:

- Production testing through the Settlers POE league
- Comprehensive application testing end-to-end
- Rate limit security for the API
- Secure user account storage for tracking rates

## :checkered_flag: Future goals:

- Introduce other uniques where rolls matter
- Introduce synthesis implicit tracking
- Introduce fractured explicit tracking
- Confidence checking

## Dashboard - Front page

## Dashboard - Query Parameters for Glorious Vanity

## Dashboard - Plot graph


## How it works

Path of Modifiers uses a continous data retrieval system consuming [Path of Exile's Public Stashes Endpoint](https://www.pathofexile.com/developer/docs/reference#publicstashes), submitting new data to the database every ~10-15 minutes. 

The data is stored with its parameters used for querying. When queried, the data is aggregated and uses several methods to calculate the exchange rates between currencies, items and their modifiers. Secret methods are used to calculate the prizes to counteract price checking. Currently prices are displayed for every 10 minutes.

User are able to query items with their specified interest through the user interface. A graph gets generated based on the user's specifications.