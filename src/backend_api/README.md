# Path of Modifiers API documentation

## Development

### Requirements

- [Docker Engine or Docker Desktop](https://docs.docker.com/engine/install/)
- [uv for Python package manager](https://docs.astral.sh/uv/)

### Docker compose

Check out the guide in [../development.md](https://github.com/Path-of-Modifiers/pathofmodifiersapp/blob/main/development.md)

### uv

Install dependencies and activate environment with:

```bash
cd backend_api

uv sync

source .venv/bin/activate
```


### Docker Compose Override


To have automatic syncing changes during development, run:

```bash
docker compose watch
```


## How to run tests

Describes how to run the tests in backend API.

For information about the api tests, please check out [Test module documentation](https://github.com/Path-of-Modifiers/pathofmodifiersapp/blob/main/src/backend_api/app/tests/README.md).


#### Backend API test prerequisites

Development docker containers must be running:

```bash
docker compose up -d
```

Start docker test containers:

```bash
docker compose -f docker-compose.test.yml up -d
```

#### Run simulated automated tests backend API

To run all of the tests backend container, run this command:

```bash
docker compose exec -T backend pytest
```

#### Run real environment tests backend API

To run tests to the real environment backend API, perform this command:

```bash
docker compose exec -T backend sh scripts/test_scripts/{test_script_name}.sh
```



## Alembic migrations

This section describes how to migrate changes made in database models to the database postgres server. Migrations are done inside the `backend` container, which runs our API.

To enter the `backend` container, run:

```bash
docker container exec -it src-backend-1 bash
```

### Migrate alembic database model changes

1. To create a alembic revision, run:

```bash
alembic revision --autogenerate -m "Message"
```

- Check out [What does and doesn't Alembic automatically detect](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)

2. Review the generated migration template
3. To migrate database changes, run:

```bash
alembic upgrade head
```

### Revert alembic database model changes

To revert to the latest changes made by an alembic revision, run:

```bash
alembic downgrade -1
```


## Routes

Description of each route is documented in [Path of Modifiers API Docs](https://pathofmodifiers.com/docs)

## Authentication

### User session authentication

The routes produces authentication outcomes based on user roles, privileges and scope. There are two main categories for routes required during authentication:
`User required` and `Non-user required` routes. Inside `User required` routes, there are two sub categories if a user is `Superuser` or `Not superuser`.

To determine if a route is `User required` or not, the hints are to look at the dependencies of the route. Dependencies are either provided in the route decoration `@route`
or inside the route arguments with a dependency type, like `current_user: CurrentUser`.

The figure below illustrates a general action path of authenticating a user session.

![alt text](https://i.ibb.co/FJcmNpf/authentication-login-example.png)

### Different user cache token types

Async Redis cache is used to cache different types of tokens during user authentication processes. Inside module `app/core/cache/user_cache` the different cache token types are specified.

Using different types of tokens provides versatility to how long different tokens last and multiple processes happening concurrently by a user.

To see how it works, check out the `app/core/cache/user_cache` module.

## Rate limit

Uses the same Async Redis cache to track rate limit between users. It is the same cache as storing user cache tokens.

There are two rate limitting modules: `SlowAPI rate limitter` and our own custom rate limitter.

The reason we use two different modules, are due to the complexity of the rate limits in our application. Slow API has the base functionality to rate limit most of our routes. It is easy to use and requires just a decorator when applying to a route. An important thing that SlowAPI doesn't support are rate limitting based on user roles. Since most of our routes doesn't need this functionality, we use the basic SlowAPI limitter for these routes. The `/plot` route requires rate limitting based on user roles, if the user has higher or lower privileges to do an amount of requests in a time frame. A more complex custom rate limitter is used to limit this route based on the user role.

Check out module `app/core/rate_limit` to see how rate limit is set up in the application.
