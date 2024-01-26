# Path of Modifiers Application  
Website application for checking prices on explicit and affixes specific items in Path of Exile  


## Download python requirements for fastapi-postgres-docker:
cd into /fastapi-postgres-docker
1. $ pip install pipreqs
2. $ pipreqs .
3. $ pip install -r requirements.txt


## Setup docker container for PostgreSQL database:
$ docker pull postgres:alpine  
$ docker run --name docker-pom_oltp_db_ct -e POSTGRES_PASSWORD=sjukebarna123 -d -p 5432:5432 postgres:alpine  
$ docker exec -it docker-pom_oltp_db_ct bash  


## Version on dependencies and download python venv
We use:  
Python version 3.12.1 ($ python -V)  
Pip version 23.3.2 ($ pip -V)  
PostgreSQL version 16.1  
Pydantic version: 2.5.3   

Activate python venv:
1. cd into \fastapi-postgres-docker
$ python3 -m venv venv  
$ source venv/Scripts/Activate  
Have venv in .gitignore  

## Postgresdatabase database:
Database name: pom_oltp_db  
Username: pom_oltp_superuser  
Password: sjukebarna123  

## Run API:
$ uvicorn main:app --reload

## Create database with PostgreSQL and make it available outside
1. $ psql -U postgres  
2. $ create database pom_oltp_db;  
3. $ CREATE USER pom_oltp_superuser WITH SUPERUSER ENCRYPTED PASSWORD 'sjukebarna123';  
4. $ grant all privileges on database pom_oltp_db to pom_oltp_superuser;  
5. $ \c pom_oltp_db   
6. $ psql -h localhost -p 5432 postgres  


Useful database commands:
1. Check tables: 
$ \dt  
2. User connection to db: 
$ \c pathofmodifiers_oltp_db  
3. Add tables to the db:   
cd into /fast_api-postgres-docker  
$ python  
$ import services  
$ services._add_tables()  
4. Check if database is running:
$ ps -ef | grep postgres  
6. Connect to postgres:
$ psql -U postgres  
8. Connect to database:
$ \c pathofmodifiers_db  
