# Path of Modifiers Application  
Website application for checking prices on explicit and affixes specific items in Path of Exile  

## Current goals we are working towards:
 - Beta release before next the next expansion in the end of July

## Future goals:
 - Introduce other uniques where rolls matter
 - Introduce synthesis implicit tracking
 - Introduce fractured explicit tracking

# Technical information
## Download python requirements:
 1. Enter a local python virtual enviroment
 2. Make sure `poetry` package is installed
    - If not run `pip install poetry`
 3. cd into `.\src\backend\app`
 4. Run `poetry install`

## Create and run docker containers
1. Enter `.\src`
2. Run `docker-compose up -d`
    - This will trigger the override docker-compose

## Access pgAdmin
1. Go to `http://localhost:8888/`
2. Enter credentials
   - email: `user@pgadmin.com`
   - password: ${PGAdmin}
3. Add server
   - General &#8594; `Name = pom_oltp_db`
   - Connection &#8594; `Host name/address = db`
      - Use `Host name/address = localhost` if connecting with pgAdmin on own computer
   - Connection &#8594; `username = pom_oltp_superuser`
   - Connection &#8594; `password = ${POSTGRES_PASSWORD}`
   - Leave everything else unchanged
4. Save
5. Tables can be found under:
   - pom_oltp_db>Databases>pom_oltp_db>Schemas>Tables
## Local alembic migrations
This section describes how to migrate changes made in database models to the local database postgres server

Run `docker container exec -it src-backend-1 bash` to enter the local backend container

### How to migrate alembic database model changes
1. Run `alembic revision --autogenerate -m "Message"` to create a alembic revision
   - [What does and doesn't Alembic autamtically detect](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)
2. Review the generated migration template
3. Run `alembic upgrade head` to migrate database changes

### How to revert the database to an alembic revision
- Run `alembic downgrade -1` to revert to the last revision made

## Current tech-stack
 - Docker\
    &#8594; To set up containers
 - Fast-API\
    &#8594; To handle communication with database
 - SQLAlchemy\
    &#8594; To set up database
 - Alembic\
    &#8594; To enable database version controll
 - GitHub\
    &#8594; To enable code version controll
 - Traefik\
    &#8594; To handle proxy and https communication
 - Poetry\
    &#8594; To handle python packages
 - pgAdmin\
    &#8594; To view and modify the database



    
