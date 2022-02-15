import pytest
from src.app import app

# https://flask.palletsprojects.com/en/2.0.x/testing/#fixtures
@pytest.fixture()
def app_fixture():
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture()
def client(app_fixture):
    return app_fixture.test_client()


def test_uses_https(client):
    response = client.get("/config/canvas.json")
    assert response.status_code == 200
    assert response.json["oidc_initiation_url"].startswith("https://")
    assert response.json["target_link_uri"].startswith("https://")
