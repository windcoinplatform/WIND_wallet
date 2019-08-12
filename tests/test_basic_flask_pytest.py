import pytest

from TurtleNetwork import app
from app.models.Token import Token


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
    response = login(test_client, 'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data


def test_login_with_pk(test_client):
    response = login(test_client, '', '5LQ9aPY7St9Aw2igohPcesvWzBNkiN9BRn6UXW14nqvn')
    assert response.status_code == 200
    assert b'Leasing' in response.data


def test_login_logout(test_client):
    response = login(test_client, 'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data
    response = logout(test_client)
    assert response.status_code == 200
    assert b'Log in' in response.data


def test_login_portfolio_info_logout(test_client):
    response = login(test_client, 'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data

    response = test_client.get("/portfolio", follow_redirects=True)
    assert response.status_code == 200
    assert b'Balance' in response.data
    assert b'Name' in response.data

    response = logout(test_client)
    assert response.status_code == 200
    assert b'Log in' in response.data


def test_login_gateway_overview_info_logout(test_client):
    response = login(test_client, 'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data

    response = test_client.get("/gateway/overview", follow_redirects=True)
    assert response.status_code == 200
    assert b'Gateway' in response.data
    assert b'fees' in response.data

    response = logout(test_client)
    assert response.status_code == 200
    assert b'Log in' in response.data


def test_login_lease_overview_info_logout(test_client):
    response = login(test_client, 'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data

    response = test_client.get("/lease/overview", follow_redirects=True)
    assert response.status_code == 200
    assert b'Lease' in response.data

    response = logout(test_client)
    assert response.status_code == 200
    assert b'Log in' in response.data


def test_login_data_overview_info_logout(test_client):
    response = login(test_client, 'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data

    response = test_client.get("/data", follow_redirects=True)
    assert response.status_code == 200

    response = logout(test_client)
    assert response.status_code == 200
    assert b'Log in' in response.data


def test_login_asset_create_info_logout(test_client):
    response = login(test_client, 'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data

    response = test_client.get("/asset/create", follow_redirects=True)
    assert response.status_code == 200

    response = logout(test_client)
    assert response.status_code == 200
    assert b'Log in' in response.data


def test_login_gateway_tn_info_logout(test_client):
    response = login(test_client, 'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data

    response = test_client.get("/gateway/waves", follow_redirects=True)
    assert response.status_code == 200
    assert b'3P' in response.data

    response = logout(test_client)
    assert response.status_code == 200
    assert b'Log in' in response.data


def test_login_details_asset_id_logout(test_client):
    response = login(test_client, 'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data

    response = test_client.get("/details/3vB9hXHTCYbPiQNuyxCQgXF6AvFg51ozGKL9QkwoCwaS", follow_redirects=True)
    assert response.status_code == 200
    assert b'Balance' in response.data

    response = logout(test_client)
    assert response.status_code == 200
    assert b'Log in' in response.data


def test_login_dex_logout(test_client):
    response = login(test_client, 'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data

    response = test_client.get("/dex", follow_redirects=True)
    assert response.status_code == 200

    response = logout(test_client)
    assert response.status_code == 200
    assert b'Log in' in response.data


def test_login_explorer_logout(test_client):
    response = login(test_client, 'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data

    response = test_client.get("/explorer", follow_redirects=True)
    assert response.status_code == 200

    response = logout(test_client)
    assert response.status_code == 200
    assert b'Log in' in response.data

def test_login_alias_logout(test_client):
    response = login(test_client, 'a', '')
    assert response.status_code == 200
    assert b'Leasing' in response.data

    response = test_client.get("/alias", follow_redirects=True)
    assert response.status_code == 200
    assert b'button' in response.data

    response = logout(test_client)
    assert response.status_code == 200
    assert b'Log in' in response.data


def test_state_transactions(test_client):
    addr = '3JrTHZ7wmfpHUscK5ENXTGgmrrfYgCbXfN2'
    amount = '50'
    response = test_client.get("/state/transactions/" + addr + "/" + amount)
    assert response.status_code == 200
    assert b'amount' in response.data
    assert b'sender' in response.data


def test_state_data(test_client):
    addr = '3JfmNT4duu54DrFX33rDM3mAJXGVnUSQLMF'
    response = test_client.get("/address/data/" + addr)
    assert response.status_code == 200
    assert b'key' in response.data
    assert b'type' in response.data
    assert b'value' in response.data


def test_state_alias_by_addr(test_client):
    addr = '3JfmNT4duu54DrFX33rDM3mAJXGVnUSQLMF'
    response = test_client.get("/state/aliases/by-address/" + addr)
    assert response.status_code == 200
    assert b'[' in response.data
    assert b']' in response.data


def test_state_alias_by_alias(test_client):
    alias = 'blackturtlebvba'
    response = test_client.get("/state/aliases/by-alias/" + alias)
    assert response.status_code == 200
    assert b'3JcB4Ux7akWqVHeSjvdqrB151LG812qk4qX' in response.data


def test_state_leases(test_client):
    addr = '3JrTHZ7wmfpHUscK5ENXTGgmrrfYgCbXfN2'
    response = test_client.get("/state/leases/" + addr)
    assert response.status_code == 200
    assert b'[' in response.data
    assert b']' in response.data


def test_token():
    token = Token('id', 8, 1000, '3JXXXXXXXXXX', 'TEST TOKEN', 'TEST TOKEN')
    assert token.id == 'id'
    assert token.decimals == 8
    assert token.amount == 1000
