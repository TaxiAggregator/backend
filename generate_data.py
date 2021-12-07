"""script for generating user data"""
import json
from argparse import ArgumentParser
from asyncio import run

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from server.config import CONFIG
from server.models import Taxi, User, __beanie_models__
from tests.factories import TaxiFactory, UserFactory


async def create_users(count, persist_in_database=False):
    """creates dummy users; saves output as json; persist to database"""
    users = UserFactory.create_batch(count)

    if persist_in_database:
        print("saving to database")
        await User.insert_many(users)

    users = [user.dict() for user in users]
    [  # pylint:disable=expression-not-assigned
        user.pop("id") for user in users
    ]
    with open("user_data.json", "w", encoding="UTF-8") as user_data:
        json.dump(users, user_data)


async def create_taxis(count, persist_in_database=False):
    """creates dummy taxis; saves output as json; persist to database"""
    taxis = TaxiFactory.create_batch(count)

    if persist_in_database:
        print("saving to database")
        await Taxi.insert_many(taxis)

    taxis = [taxi.dict() for taxi in taxis]
    [  # pylint:disable=expression-not-assigned
        taxi.pop("id") for taxi in taxis
    ]
    with open("taxi_data.json", "w", encoding="UTF-8") as taxi_data:
        json.dump(taxis, taxi_data)


async def _main(arguments):
    """initialize the script"""
    database = AsyncIOMotorClient(CONFIG.mongo_connection)[CONFIG.mongo_db]
    await init_beanie(database=database, document_models=__beanie_models__)
    if any(x in arguments["obj_type"] for x in ["user", "all"]):
        await create_users(
            arguments.get("count"),
            arguments.get("persist_in_database"),
        )
    if any(x in arguments["obj_type"] for x in ["taxi", "all"]):
        await create_taxis(
            arguments.get("count"),
            arguments.get("persist_in_database"),
        )


def main(arguments):
    """run async function"""
    run(_main(arguments))


if __name__ == "__main__":
    parser = ArgumentParser(
        description="create dummy data for the collection specified as positional argument"
    )
    parser.add_argument(
        "obj_type", action="append", choices=["user", "taxi", "all"]
    )
    parser.add_argument(
        "-c",
        "--count",
        help="number of objects to be created",
        type=int,
        default=0,
    )
    parser.add_argument(
        "--persist-in-database",
        action="store_true",
        help="stores the data in respective collection if this flag is used",
    )
    args = parser.parse_args()
    main(vars(args))
