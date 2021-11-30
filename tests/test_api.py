from time import sleep

from pytest import fixture, mark

from fastapi.testclient import TestClient

from app.main import app
from app.helper.database import db
from app.models.user import UserInDB
from app.helper.auth import get_password_hash

MOCK_USER = {
    "signup_user@gmail.com": {
        "username": "signup_user@gmail.com",
        "first_name": "Francisco",
        "last_name": "Giana",
        "email": "signup_user@gmail.com",
        "password": "secret"
    },
    "signup_user@gmail.com-missing-data": {
        "username": "signup_user@gmail.com",
        "first_name": "",
        "last_name": "Giana",
        "email": "signup_user@gmail.com-missing-data",
        "password": "secret"
    },
    "valid-user@email.com": {
        "username": "valid-user@email.com",
        "first_name": "Francisco",
        "last_name": "Giana",
        "email": "valid-user@email.com",
        "hashed_password": get_password_hash("valid-password"),
        "disabled": False,
    },
    "login@email.com": {
        "username": "login@email.com",
        "first_name": "Francisco",
        "last_name": "Giana",
        "email": "login@email.com",
        "hashed_password": get_password_hash("valid-password"),
        "password": "valid-password",
        "disabled": False,
    },
    "disabled@email.com": {
        "username": "disabled@email.com",
        "first_name": "Francisco",
        "last_name": "Giana",
        "email": "disabled@email.com",
        "hashed_password": get_password_hash("valid-password"),
        "disabled": True,
    }
}

STOCKS = {
    "FB": {"id": "FB", "name": "Facebook"},
    "AAPL": {"id": "AAPL", "name": "Apple"},
    "MSFT": {"id": "MSFT", "name": "Microsoft"},
    "GOOGL": {"id": "GOOGL", "name": "Google"},
    "AMZN": {"id": "AMZN", "name": "Amazon"}
}

MSG_INCORRECT_USR_OR_PASS = {'detail': 'Incorrect username or password'}
MSG_NOT_VALIDATE_CREDENTIALS = {'detail': 'Could not validate credentials'}
MSG_USR_EXIST = {'detail': 'Username already exists'}
MSG_NOT_AUTHENTICATED = {'detail': 'Not authenticated'}


def _login(client, username):
    user = MOCK_USER.get(username)
    response = client.post(
        "/auth/signin",
        data={
                "username": user.get("username"),
                "password": user.get("password")
            }
    )
    assert response.status_code == 200
    return (response.json()['token_type'], response.json()['access_token'])


@fixture()
def client():
    return TestClient(app)


@fixture()
def login(client, create_users, username="login@email.com"):
    return _login(client, username)


@fixture(scope="session")
def create_users():
    db.add(UserInDB(**MOCK_USER.get('valid-user@email.com')))
    db.add(UserInDB(**MOCK_USER.get('login@email.com')))
    db.add(UserInDB(**MOCK_USER.get('disabled@email.com')))


@mark.parametrize(
    "username, status_code, msg",
    [
        ("signup_user@gmail.com", 200, {}),
        ("signup_user@gmail.com", 400, MSG_USR_EXIST),
        ("signup_user@gmail.com-missing-data", 422,
            {'detail': [{'loc': ['body', 'first_name'],
             'msg': 'field required', 'type': 'value_error.missing'}]})
    ]
)
def test_signup(client, username, status_code, msg):

    response = client.post(
            "/auth/signup",
            data=MOCK_USER[username]
        )

    assert response.status_code == status_code
    assert response.json() == msg

    token_type, access_token = _login(client, username)
    assert token_type.lower() == "bearer"
    assert access_token is not None


@mark.parametrize(
    "username, password, expected",
    [
        ("non-exist-user", "test1", 401),
        ("valid-user@email.com", "valid-password", 200),
        ("valid-user@email.com", "non-valid-password", 401),
        ("", "valid-password", 422),
        ("valid-user@email.com", "", 422),
        ("disabled@email.com", "valid-password", 401),
    ]
)
def test_signin(client, create_users, username, password, expected):

    response = client.post(
            "/auth/signin",
            data={"username": username, "password": password}
        )

    assert response.status_code == expected
    if expected == 401:
        assert response.json() == MSG_INCORRECT_USR_OR_PASS


def test_me(client, login):
    _, access_token = login
    response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer {}".format(access_token)}
        )

    assert response.status_code == 200
    assert response.json() == {
        "username": "login@email.com",
        "email": "login@email.com",
        "first_name": "Francisco",
        "last_name": "Giana",
        "disabled": False
    }


# @mark.skip()
@mark.parametrize(
    "requests, delta, throttling",
    [
        (5, 1/4, True),
        (4, 1/4, False)
    ]
)
def test_throttling(client, login, requests, delta, throttling):
    _, access_token = login

    sleep(2)  # Wait 60 seconds to reset the throlling
    i = 0
    while i < requests:
        response = client.get(
            "/stocks",
            headers={"Authorization": "Bearer {}".format(access_token)}
        )
        i += 1
        if response.status_code != 200:
            break
        sleep(delta/requests)

    if throttling:
        assert response.status_code == 429
    else:
        assert response.status_code == 200


def test_health_check(client):
    response = client.get(
        "/health_check",
    )

    assert response.status_code == 200
    assert response.json() == {}


@mark.parametrize(
    "token, expected, body",
    [
        ("valid", 200, STOCKS),
        ("non-valid", 401, MSG_NOT_VALIDATE_CREDENTIALS),
        ("not-in-header", 401, MSG_NOT_AUTHENTICATED)
    ]
)
def test_stocks(client, login, token, expected, body):
    _, access_token = login if token == "valid" else ('fake', 'fake-token')
    response = client.get(
        "/stocks",
        headers={"Authorization": "Bearer {}".format(access_token)}
        if token != "not-in-header" else {}
    )

    assert response.status_code == expected
    assert response.json() == body


@mark.parametrize(
    "stock_id, expected",
    [
        ("FB", 200),
        ("PPPP", 400),
    ]
)
def test_stock_id(client, login, stock_id, expected):
    _, access_token = login
    response = client.get(
        f"/stocks/{stock_id}",
        headers={"Authorization": "Bearer {}".format(access_token)}
    )

    assert response.status_code == expected
