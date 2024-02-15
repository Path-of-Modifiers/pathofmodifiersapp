# Path of Modifiers Application  
Website application for checking prices on explicit and affixes specific items in Path of Exile  

## Current goals we are working towards:
 - Modifiers on unique jewels such as Watcher's Eye and Sublime Vision
 - Rolls for certain unique jewels such as Timeless Jewels and Voices.

## Future goals:
 - Introduce other uniques where rolls matter
 - Introduce synthesis implicit tracking
 - Introduce fractured explicit tracking

# Technical information
## Download python requirements:
 1. Enter a local virtual enviroment
 2. Make sure `poetry` package is installed
    - If not run `pip install poetry`
 3. cd into `.\src\backend\app`
 4. Run `poetry install`

## Docker-compose
1. Enter `.\src`
2. Run `docker-compose up -d`
    - This will trigger the override docker-compose

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