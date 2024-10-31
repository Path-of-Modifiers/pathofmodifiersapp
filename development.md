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

## How to run tests

This section describes how to run the various tests in this application.

### How to run tests in backend API

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

### How to run tests in backend data retrieval

Describes how to run tests in backend data retrieval.

#### Backend data retrieval test prerequisites

You need to build `Dockerfile.test` within module `backend_data_retrieval` root.

To build the container, perform this command:

```bash
docker build -t backend_data_retrieval_test -f backend_data_retrieval/Dockerfile.test backend_data_retrieval
```

#### Run tests in backend data retrieval

To run all tests in backend data retrieval, perform this command:

```bash
docker run --rm backend_data_retrieval_test
```

If you want to specify a test file, run it like this for example:

```bash
docker run --rm backend_data_retrieval_test data_retrieval_app/tests/external_data_retrieval/test_continuous_data_retrieval.py
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

## Access the Redis cache server

The redis server is used to handle ratelimit on the Path of Modifiers' API. A user's activity to endpoints are stored inside the Redis server to keep track of rates.

### Prerequisite

You need to have [Redis CLI](https://redis.io/docs/latest/develop/connect/cli/) installed on your computer.

### Access Redis Cache server

To access the Redis Cache server, run:

```bash
redis-cli -h $DOMAIN -p 6379 -a $REDIS_PASSWORD
```

### Redis Container Errors and Warnings

These are errors that may show up when creating a Redis container in our application.

#### Memory overcommit

```
WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition...
```

This warning can be fixed by enabling overcommit on reboot:

```bash
echo "vm.overcommit_memory = 1" | sudo tee /etc/sysctl.d/nextcloud-aio-memory-overcommit.conf
```

Enable it temporarily and immediately:

```bash
sysctl "vm.overcommit_memory=1"
```

## Pre-commits and code linting

We use a tool called [pre-commit](https://pre-commit.com/#intro) for code linting and formatting.

When you install it, it runs right before making a commit in git. This way it ensures that the code is consistent and formatted even before it is committed.

You can find a file `.pre-commit-config.yaml` with configurations at the root of the project.

### Install pre-commit to run automatically

`pre-commit`is already part of the dependencies of the project, but you could also install it globally if you prefer to, following the [official pre-commit docs](https://pre-commit.com/#usage).

After having the pre-commit tool installed and available, you need to "install" it in the local repository, so that it runs automatically before each commit.

In root directory `.`, using Poetry, you could do it with:

```bash
poetry -C src/backend_api run pre-commit install --config src/.pre-commit-config.yaml
```

Now whenever you try to commit, e.g. with:

```bash
git commit
```

...pre-commit will run and check and format the code you are about to commit, and will ask you to add that code (stage it) with git again before committing.

Then you can git add the modified/fixed files again and now you can commit.

### Running pre-commit hooks manually

You can also run pre-commit manually on all the files.

In root directory `.`, using Poetry, you could do it with:

```bash
poetry -C src/backend_api run pre-commit run --all-files --config src/.pre-commit-config.yaml
```


### Backup and restore database

Useful if you have gathered data and want to optimize and min max performance with different database architectures.

Or just create a safepoint before doing general migrations.

To backup the database in a file, make sure you are in a fitting folder to put the file (which is quite large).
Create the file:

```bash
docker exec -t src-db-1 pg_dumpall -c -U pom_oltp_superuser > pom_db_data_dump_`date +%Y-%m-%d"_"%H_%M_%S`.sql
```

To restore the database from the file:

```bash
cat your_dump.sql | docker exec -i src-db-1 psql -U pom_oltp_superuser -d pom_oltp_db
```

Source: [stackoverflow-backup-restore-postgres-db](https://stackoverflow.com/questions/24718706/backup-restore-a-dockerized-postgresql-database)

### URLs

The production or staging URLs would use these same paths, but with your own domain.

#### Development URLs for local development:

Frontend: http://localhost

Backend API: http://localhost/api/

Automatic Interactive Docs (Swagger UI): http://localhost/docs

Automatic Alternative Docs (ReDoc): http://localhost/redoc

pgAdmin: http://localhost:8081

Traefik UI: http://localhost:8090
