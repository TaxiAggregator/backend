The project is based on [FastAPI](https://fastapi.tiangolo.com). It is pretty similar to Flask but brings modern python functionalities like
async programming and typing into play.

For MongoDB, I am using [Beanie](https://roman-right.github.io/beanie/), which is based on [Motor](https://motor.readthedocs.io/en/stable/)
(which is based on [pymongo](https://pymongo.readthedocs.io/en/stable/)). It is a neat ODM and borrows heavily
from [SQLAlchemy](https://www.sqlalchemy.org)/[Django ORM](https://docs.djangoproject.com/en/3.2/topics/db/).

Both FastAPI and ODMantic use [Pydantic](https://pydantic-docs.helpmanual.io) under the hood.

You can see the repo as an SOA backend, where all services are implemented in a single repository. Should we find enough time, we can easily refactor
the backend into individual microservices. The effort needed for refactoring will be minimal. We will have to put up a tiny [main.py](./main.py)
for a particular service and move corresponding [model](./models) and [router](./routers) files into separate repositories.

If you would like to run the code locally:
1. Clone the repo
2. Create virtualenv
3. Install dependencies `pip install -r requirements/local.txt`
4. run `uvicorn main:app`
5. With that you should be able to access the [Swagger UI](http://127.0.0.1:8000/docs) or [ReDoc page](http://127.0.0.1:8000/redoc).

If you are using VSCode, there is a [launch config](./.vscode/launch.json) in the .vscode folder.

I am also using [bandit](/.vscode/launch.json), [black](https://black.readthedocs.io/en/stable/), and [pylint](https://pylint.pycqa.org/en/latest/) for code quality.
