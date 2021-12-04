import pytest
from api import app
from tests.testdatabase import TestDatabase
from api.utils.constants import messages


@pytest.fixture
def init_db(autouse=True):
    app.database = TestDatabase()


@pytest.mark.asyncio
async def test_register_user_mutation():
    mutation = """
        mutation TestMutation($user: UserAuth!) {
            registerUser(user: $user) {
                ... on User {
                    email
                }
            }
        }
    """

    email = "kalbetre@gmail.com"
    response = await app.schema.execute(
        mutation,
        variable_values={
            "user": {
                "email": email,
                "password": "pass123"
            }
        }
    )

    assert response.errors is None
    assert response.data["registerUser"] == {
        "email": email,
    }


@pytest.mark.asyncio
async def test_register_user_mutation_returns_validation_error():
    mutation = """
        mutation TestMutation($user: UserAuth!) {
            registerUser(user: $user) {
                ... on InputValidationError {
                    errors {
                        input
                    }
                }
            }
        }
    """

    email = "kalbetre@gmailcom"
    response = await app.schema.execute(
        mutation,
        variable_values={
            "user": {
                "email": email,
                "password": "123"
            }
        }
    )

    assert response.errors is None
    assert response.data["registerUser"]["errors"] == [
        {"input": "email"},
        {"input": "password"},
    ]


@pytest.mark.asyncio
async def test_register_user_mutation_should_not_register_users_with_same_email():
    mutation = """
        mutation TestMutation($user: UserAuth!) {
            registerUser(user: $user) {
                ... on EmailAlreadyRegistered {
                    error {
                        message
                    }
                }
            }
        }
    """

    email = "kalbetre@gmail.com"
    await app.schema.execute(
        mutation,
        variable_values={
            "user": {
                "email": email,
                "password": "pass123"
            }
        }
    )

    response = await app.schema.execute(
        mutation,
        variable_values={
            "user": {
                "email": email,
                "password": "pass123"
            }
        }
    )

    assert response.errors is None
    assert response.data["registerUser"]["error"]["message"] == messages.EMAIL_TAKEN
