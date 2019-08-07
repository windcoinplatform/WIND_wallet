import pytest

from TurtleNetwork import app


@pytest.fixture()
def test_client():
    flask_app = app

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


def login(client, seed, pk):
    return client.post('/login', data=dict(
        seed=seed,
        pk=pk
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_main_login_page(test_client):
    response = test_client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b'Log in' in response.data


def test_login_with_seed(test_client):
    response = login(test_client,'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data

def test_login_with_pk(test_client):
    response = login(test_client,'', '5LQ9aPY7St9Aw2igohPcesvWzBNkiN9BRn6UXW14nqvn')
    assert response.status_code == 200
    assert b'Leasing' in response.data
