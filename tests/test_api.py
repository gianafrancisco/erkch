from time import sleep

from pytest import fixture, mark

from fastapi.testclient import TestClient

from app.main import app

FAKE_USER = {
    "fake_user_1": {
        "first_name": "Francisco",
        "last_name": "Giana",
        "email": "fake_user@gmail.com",
        "password": "secret"
    }
}


@fixture()
def client():
    return TestClient(app)


@fixture()
def login(client):
    response = client.post(
        "/auth/signin",
        data={"username": "gianafrancisco@gmail.com", "password": "secret"}
    )
    assert response.status_code == 200
    return response.json()['token_type'], response.json()['access_token']


def test_signup(client):

    response = client.post(
            "/auth/signup",
            data=FAKE_USER["fake_user_1"]
        )

    assert response.status_code == 200
    assert response.json() == {}


def test_me(client, login):
    _, access_token = login
    response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer {}".format(access_token)}
        )

    assert response.status_code == 200
    assert response.json() == {
        "username": "gianafrancisco@gmail.com",
        "email": "gianafrancisco@gmail.com",
        "first_name": "Francisco",
        "last_name": "Giana",
        "disabled": False
    }


@mark.parametrize(
    "requests, delta, throttling",
    [
        (10, 60, True),
        (4, 60, False)
    ]
)
def test_throttling(client, login, requests, delta, throttling):
    _, access_token = login

    sleep(60)  # Wait 60 seconds to reset the throlling
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

    if i == requests:
        assert response.status_code == 200
        assert throttling is False
    else:
        assert response.status_code == 429
        assert throttling is True
