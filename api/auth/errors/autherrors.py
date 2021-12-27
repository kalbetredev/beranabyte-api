from dataclasses import dataclass


@dataclass
class AuthError(Exception):
    message: str
