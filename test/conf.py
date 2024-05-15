import pytest
from app import app
@pytest.fixture()
def app():
    return app
@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test(client):
    response = client.get("/cards")
    assert response.status_code == 200