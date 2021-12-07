The project is based on [FastAPI](https://fastapi.tiangolo.com). It is pretty similar to Flask but brings modern python functionalities like
async programming and typing into play.

For MongoDB, I am using [Beanie](https://roman-right.github.io/beanie/), which is based on [Motor](https://motor.readthedocs.io/en/stable/)
(which is based on [pymongo](https://pymongo.readthedocs.io/en/stable/)). It is a neat ODM and borrows heavily
from [SQLAlchemy](https://www.sqlalchemy.org)/[Django ORM](https://docs.djangoproject.com/en/3.2/topics/db/).

Both FastAPI and ODMantic use [Pydantic](https://pydantic-docs.helpmanual.io) under the hood.

You can see the repo as an SOA backend, where all services are implemented in a single repository. Should we find enough time, we can easily refactor
the backend into individual microservices. The effort needed for refactoring will be minimal. We will have to put up a tiny [main.py](./main.py)
for a particular service and move corresponding [model](./models) and [router](./routers) files into separate repositories.

I am also using [bandit](/.vscode/launch.json), [black](https://black.readthedocs.io/en/stable/), and [pylint](https://pylint.pycqa.org/en/latest/) for code quality.

## Running the application locally:

1. Clone the repository
1. Create virtualenv
1. Install dependencies `pip install -r requirements/local.txt`
1. Update the .env file to match the application settings

    The values in .env file are set up so that running from docker works with no changes needed. **Please update the .env file with correct mongo connection string** and other application defaults.
1. run `uvicorn server.main:app`
1. With that you should be able to access the [Swagger UI](http://127.0.0.1:8000/docs) or [ReDoc page](http://127.0.0.1:8000/redoc).

If you are using VSCode, there is a [launch config](./.vscode/launch.json) in the .vscode folder.

## Running with docker

1. Clone the repository
1. Ensure the docker is running
1. Run `docker compose up -d`

This will build the webapp image and also run mongodb locally in a container. Please refer to docker-compose.yml for more details.

## Script for generating dummy user and taxi data

Use generate_data.py to generate the dummy data in following manner
1. Creating dummy user data in json format

    `python generate_data.py user --count 60`

    The data will be saved in **user_data.json** in current working directory.

1. Creating dummy taxi data in json format

    `python generate_data.py taxi --count 60`

    The data will be saved in **taxi_data.json** in current working directory

1. Creating dummy user and taxi data in json format

    `python generate_data.py all --count 60`

    The data will be saved in **user_data.json** and **taxi_data.json** in current working directory

Use `--persist-in-database` with any of the commands above to save the data in database.

