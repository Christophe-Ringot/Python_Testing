import server
import pytest


@pytest.fixture()
def client():
    flask_app = server.app
    with flask_app.test_client() as client:
        yield client


class Test():

    def test_status_code_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_should_show_welcome_page(self, client):
        response = client.get("/")
        assert b'Welcome to the GUDLFT Registration Portal!' in response.data

    def test_sould_show_club_board(self, client):
        response = client.get("/")
        assert b'Name : Simply Lift' in response.data
