import os
import tomllib

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


from eflips.model import Scenario, Vehicle



if os.path.exists("config.toml"):
    with open("config.toml", "rb") as fp:
        config = tomllib.load(fp)
else:
    raise FileNotFoundError("config.toml not found.")


def construct_database_url(db_name: str, db_user: str, db_password: str, db_host: str, db_port: int):
    """
    Constructs a database URL for use with SQLAlchemy.

    :param db_name: The name of the database.
    :param db_user: The username to connect to the database.
    :param db_password: The password to connect to the database.
    :param db_host: The host of the database.
    :param db_port: The port of the database.
    :return: A SQLAlchemy database URL.
    """
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


if __name__ == "__main__":


    # get the database URL from config.toml. Be sure to modify config.toml.sample to config.toml and fill in the database
    DB_URL = construct_database_url(
        config["database"]["dbname"],
        config["database"]["user"],
        config["database"]["password"],
        config["database"]["host"],
        config["database"]["port"])


    engine = create_engine(DB_URL)

    with Session(engine) as session:


        # Here all data from the database are accessible with session.query. See documents of sqlalchemy and eflips-model for more information.

        # Get a scenario
        scenario = session.query(Scenario).all()[0]

        # Example: Get all vehicles from a scenario

        total_vehicle_count = session.query(Vehicle).filter(Vehicle.scenario == scenario).count()

        print(total_vehicle_count)