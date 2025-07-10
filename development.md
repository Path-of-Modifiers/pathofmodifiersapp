# Path of Modifiers - Development :computer:

For each of the modules to develop in frontend, backend\_api and backend\_data\_retrieval, please refer to their respective README's.

## Create and run docker containers in development

For local development and testing, we use the `override` containers. These have localized ports which can be accessed.

In directory `./src`, run:

```bash
docker compose watch
```

Now you can open the browser and interact with the following:

- Frontend: http://localhost:5173

- Backend web API based on OpenAPI: http://localhost:8000

- OpenAPI backend Swagger UI: http://localhost:8000/docs

- Adminer, database web administration: http://localhost:8080

- Traefik UI, to see how the routes are being handled by the proxy: http://localhost:8090


## Pre-commits and code linting

We use a tool called [pre-commit](https://pre-commit.com/#intro) for code linting and formatting.

When you install it, it runs right before making a commit in git. This way it ensures that the code is consistent and formatted even before it is committed.

You can find a file `.pre-commit-config.yaml` with configurations at the root of the project.

### Install pre-commit to run automatically

`pre-commit`is already part of the dependencies of the project, but you could also install it globally if you prefer to, following the [official pre-commit docs](https://pre-commit.com/#usage).

After having the pre-commit tool installed and available, you need to "install" it in the local repository, so that it runs automatically before each commit.

In ./src directory using uv, you could do it with:

```bash
uv run pre-commit install
```

Now whenever you try to commit, e.g. with:

```bash
git commit
```

...pre-commit will run and check and format the code you are about to commit, and will ask you to add that code (stage it) with git again before committing.

Then you can git add the modified/fixed files again and now you can commit.


### Running pre-commit hooks manually

You can also run pre-commit manually on all the files with:

```bash
uv run pre-commit run --all-files
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

### URLs

The production or staging URLs would use these same paths, but with your own domain.

#### Development URLs for local development:

Frontend: http://localhost:5173

Frontend dev: http://localhost:5174

Backend API: http://localhost:8000

Automatic Interactive Docs (Swagger UI): http://localhost:8000/docs

Automatic Alternative Docs (ReDoc): http://localhost:8000/redoc

pgAdmin: http://localhost:8881

Traefik UI: http://localhost:8090
