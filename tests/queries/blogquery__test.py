import pytest
from api import app
from api.utils.constants import messages
from tests.testdatabase import TestDatabase


@pytest.fixture
def init_db(autouse=True):
    app.database = TestDatabase()


def test_blogs_query_gets_all_blogs():
    query = """
        query {
            blogs {
                id
            }
        }
    """

    result = app.schema.execute_sync(query)

    assert result.errors is None

    blogs = app.database.get_all_blogs()
    assert result.data["blogs"] == [{"id": str(blog.id)} for blog in blogs]


def test_blogs_query_gets_published_blogs():
    query = """
        query {
            blogs(isPublished: true) {
                id
            }
        }
    """

    result = app.schema.execute_sync(query)

    assert result.errors is None

    blogs = app.database.get_all_blogs()
    assert result.data["blogs"] == [
        {"id": str(blog.id)} for blog in blogs if blog.is_published
    ]


def test_blog_query_gets_blog_by_id():
    query = """
        query {
            blog(blogId: "1") {
                ...on Blog {
                    title
                }
            }
        }
    """

    result = app.schema.execute_sync(query)

    assert result.errors is None

    blog = app.database.get_blog_by_id("1")

    assert result.data["blog"]["title"] == blog.title


def test_blog_query_gets_author_data():
    query = """
        query {
            blog(blogId: "1") {
                ...on Blog {
                    author {
                        id,
                        email
                    }
                }
            }
        }
    """

    result = app.schema.execute_sync(query)

    assert result.errors is None

    blog = app.database.get_blog_by_id("1")

    assert result.data["blog"]["author"]["id"] == blog.author().id
    assert result.data["blog"]["author"]["email"] == blog.author().email


def test_blog_query_returns_blog_not_found_error():
    query = """
        query {
            blog(blogId: "xx") {
                ...on BlogNotFound {
                    error {
                        message
                    }
                }
            }
        }
    """

    result = app.schema.execute_sync(query)

    assert result.data["blog"]["error"]["message"] == messages.BLOG_NOT_FOUND


def test_topics_query_gets_all_topics():
    query = """
        query {
            topics
        }
    """

    result = app.schema.execute_sync(query)

    assert result.errors is None

    topics = app.database.get_all_topics()
    assert result.data["topics"] == list(topics)
