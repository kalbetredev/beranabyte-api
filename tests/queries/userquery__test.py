import pytest
from api import app
from tests.testdatabase import TestDatabase
from api.utils.constants import messages


@pytest.fixture
def init_db(autouse=True):
    app.database = TestDatabase()


def test_user_query_returns_user_by_id():
    query = """
        query {
            user(userId: "UU-1") {
                ...on User {
                    id,
                    email
                }
            }
        }
    """

    result = app.schema.execute_sync(query)
    assert result.errors is None

    user = app.database.get_user_by_id("UU-1")
    assert result.data["user"] == {"id": user.id, "email": user.email}


def test_user_query_returns_user_not_found_error():
    query = """
        query {
            user(userId: "UU-XX") {
                ...on UserNotFound {
                    error {
                        message
                    }
                }
            }
        }
    """

    result = app.schema.execute_sync(query)
    assert result.errors is None

    assert result.data["user"]["error"]["message"] == messages.USER_NOT_FOUND
