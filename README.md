# Path of Modifiers Application  
Website application for checking prices on explicit and affixes specific items in Path of Exile  



## Setup docker container for PostgreSQL database:
1. docker pull postgres:alpine  
2. docker run --name fastapi-postgres-pathofmodifiers -e POSTGRES_PASSWORD=Arceus150901 -d -p 5432:5432 postgres:alpine  
2. docker exec -it fastapi-postgres-pathofmodifiers bash  


## Version on dependencies and download python venv
We use:  
Python version 3.10.11 ($ python -V)  
Pip version 23.3.2 ($ pip -V)  
PostgreSQL version 16.1  
Pydantic version: 2.5.3   

1. $ python3 -m venv venv  
2. $ source venv/Scripts/Activate  
3. Have venv in .gitignore  
4. pip3 install "fastapi[all]" SQLAlchemy psycopg2-binary pydantic  

## Postgresdatabase database:
Database name: pathofmodifiers_db  
Username: pathofmodifiersdbadmin  
Password: sjukebarna123  

## Run API:
$ uvicorn main:app --reload

## Create database with PostgreSQL  
1. $ psql -U postgres  
2. $ create database pathofmodifiers_db;  
3. $ CREATE USER pathofmodifiersdbadmin WITH SUPERUSER ENCRYPTED PASSWORD 'sjukebarna123';  
4. $ grant all privileges on database pathofmodifiers_db to pathofmodifiersdbadmin;  
5. Make db available outside:   
$ Connect to database: $ \c pathofmodifiers_db  
$ psql -h localhost -p 5432 postgres  


Useful database commands:
1. Check tables: $ \dt  
2. User connection to db: $ \c pathofmodifiers_db  
3. Add tables to the db:   
cd into /fast_api-postgres-docker  
$ python  
$ import services  
$ services._add_tables()  
4. Check if database is running: $ ps -ef | grep postgres  
5. Connect to postgres: $ psql -U postgres  
6. Connect to database: $ \c pathofmodifiers_db  