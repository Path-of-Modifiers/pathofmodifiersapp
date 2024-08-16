# Path of Modifiers - Development :computer:

## Download Python requirements

1.  Enter a local python virtual enviroment
2.  Make sure [poetry](https://python-poetry.org/docs/) package is installed
3.  In directory `./src/backend_api`, run:

```bash
poetry install
```

## Create and run docker containers in development

For local development and testing, we use the `override` containers. These have localized ports which can be accessed.

In directory `./src`, run:

```bash
docker-compose up -d
```

This will trigger the containers in `docker-compose.override.yml` file.

## Access pgAdmin

1. Go to [http://localhost:8881/](http://localhost:8881/) or access pgAdmin software on your own computer
2. User credentials:
   - Email: `${PGADMIN_DEFAULT_EMAIL}`
   - Password: `${PGADMIN_DEFAULT_PASSWORD}`
3. Register server credentials:
   - General &#8594; Enter a `'custom name'` for the server
   - Connection &#8594; Host name/address:
     - `${POSTGRES_SERVER}` if connecting in browser
     - `${DOMAIN}` if connecting to pgAdmin on your own computer
   - Connection &#8594; Username: `${POSTGRES_USER}`
   - Connection &#8594; Password: `${POSTGRES_PASSWORD}`
   - Leave everything else unchanged
4. Save
5. Tables can be found under:
   - `'custom name'>Databases>${POSTGRES_DB}>Schemas>public>Tables`

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

## Pre-commits and code linting

We use a tool called [pre-commit](https://pre-commit.com/#intro) for code linting and formatting.

When you install it, it runs right before making a commit in git. This way it ensures that the code is consistent and formatted even before it is committed.

You can find a file `.pre-commit-config.yaml` with configurations at the root of the project.

### Install pre-commit to run automatically

`pre-commit`is already part of the dependencies of the project, but you could also install it globally if you prefer to, following the [official pre-commit docs](https://pre-commit.com/#usage).

After having the pre-commit tool installed and available, you need to "install" it in the local repository, so that it runs automatically before each commit.

Using Poetry, you could do it with:

```bash
poetry run pre-commit install
```

Now whenever you try to commit, e.g. with:

```bash
git commit
```

...pre-commit will run and check and format the code you are about to commit, and will ask you to add that code (stage it) with git again before committing.

Then you can git add the modified/fixed files again and now you can commit.

### Running pre-commit hooks manually

You can also run pre-commit manually on all the files. To do it using Poetry:

```bash
poetry run pre-commit run --all-files
```

### URLs

The production or staging URLs would use these same paths, but with your own domain.

#### Development URLs for local development:

Frontend: http://localhost

Backend API: http://localhost/api/

Automatic Interactive Docs (Swagger UI): http://localhost/docs

Automatic Alternative Docs (ReDoc): http://localhost/redoc

pgAdmin: http://localhost:8081

Traefik UI: http://localhost:8090
