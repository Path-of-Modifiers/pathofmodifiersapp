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


### URLs

The production or staging URLs would use these same paths, but with your own domain.

#### Development URLs for local development:

Frontend: http://localhost

Backend API: http://localhost/api/

Automatic Interactive Docs (Swagger UI): http://localhost/docs

Automatic Alternative Docs (ReDoc): http://localhost/redoc

pgAdmin: http://localhost:8081

Traefik UI: http://localhost:8090