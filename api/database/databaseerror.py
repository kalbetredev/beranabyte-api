from dataclasses import dataclass


@dataclass
class DatabaseError(Exception):
    message: str
