import pytest
from api import app
from tests.testdatabase import TestDatabase
from api.utils.constants import messages


@pytest.fixture
def init_db(autouse=True):
    app.database = TestDatabase()


@pytest.mark.asyncio
async def test_create_new_blog_mutation():
    mutation = """
        mutation TestMutation($newBlog: NewBlog!) {
            createNewBlog(newBlog: $newBlog) {
                ... on Blog {
                    title
                }
            }
        } 
    """

    response = await app.schema.execute(
        mutation,
        variable_values={
            "newBlog": {
                "title": "new blog",
                "topic": "topic 3",
                "summary": "new summary",
                "imageUrl": "",
                "content": "blog content",
            }
        },
    )

    assert response.errors is None
    assert response.data["createNewBlog"] == {
        "title": "new blog",
    }


@pytest.mark.asyncio
async def test_create_new_blog_mutation_should_return_blog_title_taken_error():
    mutation = """
        mutation TestMutation($newBlog: NewBlog!) {
            createNewBlog(newBlog: $newBlog) {
                ... on BlogTitleTaken {
                    error {
                        message
                    }
                }
            }
        } 
    """

    response = await app.schema.execute(
        mutation,
        variable_values={
            "newBlog": {
                "title": "new blog",
            }
        },
    )

    response = await app.schema.execute(
        mutation,
        variable_values={
            "newBlog": {
                "title": "new blog",
            }
        },
    )

    assert response.errors is None
    assert (
        response.data["createNewBlog"]["error"]["message"] == messages.BLOG_TITLE_TAKEN
    )


@pytest.mark.asyncio
async def test_update_blog_mutation():
    mutation = """
        mutation TestMutation($updatedBlog: UpdatedBlog!) {
            updateBlog(updatedBlog: $updatedBlog) {
                ... on Blog {
                    title
                }
            }
        } 
    """

    response = await app.schema.execute(
        mutation,
        variable_values={
            "updatedBlog": {
                "id": "0",
                "title": "updated blog",
            }
        },
    )

    assert response.errors is None
    assert response.data["updateBlog"] == {
        "title": "updated blog",
    }


@pytest.mark.asyncio
async def test_update_blog_mutation_should_return_blog_not_found_error():
    mutation = """
        mutation TestMutation($updatedBlog: UpdatedBlog!) {
            updateBlog(updatedBlog: $updatedBlog) {
                ... on BlogNotFound {
                    error {
                        message
                    }
                }
            }
        } 
    """

    response = await app.schema.execute(
        mutation,
        variable_values={
            "updatedBlog": {
                "id": "aa",
                "title": "updated blog",
            }
        },
    )

    assert response.errors is None
    assert response.data["updateBlog"]["error"]["message"] == messages.BLOG_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_blog_mutation():
    mutation = """
        mutation TestMutation($blogId: String!) {
            deleteBlog(blogId: $blogId) {
                ... on Success {
                    message
                }
            }
        } 
    """

    response = await app.schema.execute(mutation, variable_values={"blogId": "7"})

    assert response.errors is None
    assert response.data["deleteBlog"]["message"] == messages.BLOG_DELETED_SUCCESSFULLY


@pytest.mark.asyncio
async def test_delete_blog_mutation_should_return_blog_not_found_error():
    mutation = """
         mutation TestMutation($blogId: String!) {
            deleteBlog(blogId: $blogId) {
                ... on BlogNotFound {
                    error {
                        message
                    }
                }
            }
        } 
    """

    response = await app.schema.execute(mutation, variable_values={"blogId": "xx"})

    assert response.errors is None
    assert response.data["deleteBlog"]["error"]["message"] == messages.BLOG_NOT_FOUND


@pytest.mark.asyncio
async def test_publish_blog_mutation():
    mutation = """
        mutation TestMutation($blogId: String!) {
            publishBlog(blogId: $blogId) {
                ... on Blog {
                    id,
                    isPublished
                }
            }
        } 
    """

    blog_id = "5"
    response = await app.schema.execute(mutation, variable_values={"blogId": blog_id})

    assert response.errors is None
    assert response.data["publishBlog"] == {"id": blog_id, "isPublished": True}


@pytest.mark.asyncio
async def test_delete_blog_mutation_should_return_blog_not_found_error():
    mutation = """
         mutation TestMutation($blogId: String!) {
            publishBlog(blogId: $blogId) {
                ... on BlogNotFound {
                    error {
                        message
                    }
                }
            }
        } 
    """

    response = await app.schema.execute(mutation, variable_values={"blogId": "xx"})

    assert response.errors is None
    assert response.data["publishBlog"]["error"]["message"] == messages.BLOG_NOT_FOUND


@pytest.mark.asyncio
async def test_increment_view_count_mutation():
    mutation = """
        mutation TestMutation($blogId: String!) {
            incrementBlogViewCount(blogId: $blogId) {
                ... on Blog {
                    id,
                    viewCount
                }
            }
        } 
    """
    blog_id = "5"
    blog_view_count = app.database.get_blog_by_id(blog_id).view_count

    response = await app.schema.execute(mutation, variable_values={"blogId": blog_id})

    assert response.errors is None
    assert response.data["incrementBlogViewCount"] == {
        "id": blog_id,
        "viewCount": blog_view_count + 1,
    }


@pytest.mark.asyncio
async def test_increment_view_count_mutation_should_return_blog_not_found_error():
    mutation = """
         mutation TestMutation($blogId: String!) {
            incrementBlogViewCount(blogId: $blogId) {
                ... on BlogNotFound {
                    error {
                        message
                    }
                }
            }
        } 
    """

    response = await app.schema.execute(mutation, variable_values={"blogId": "xx"})

    assert response.errors is None
    assert (
        response.data["incrementBlogViewCount"]["error"]["message"]
        == messages.BLOG_NOT_FOUND
    )
