import os
from dataclasses import dataclass

@dataclass
class Env:
    HOST = os.getenv("localhost"),
    DATABASE = os.getenv("SQream"),
    USER = os.getenv("postgres"),
    PASSWORD = os.getenv("0543036908"),
    PORT = os.getenv("5432")

    # HOST = os.getenv("localhost"),
    # DATABASE = os.getenv("SQream"),
    # USER = os.getenv("postgres"),
    # PASSWORD = os.getenv("0543036908"),
    # PORT = os.getenv("5432")


