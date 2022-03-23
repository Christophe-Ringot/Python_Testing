import server
import pytest


@pytest.fixture()
def client():
    flask_app = server.app
    with flask_app.test_client() as client:
        yield client


class Test():

    def test_status_code_200(self, client):
        response = client.get("/create_tournaments")
        assert response.status_code == 200

    def test_should_show_create_tournament_page(self, client):
        response = client.get("/create_tournaments")
        assert b'Create tournaments' in response.data

    def test_link_to_index(self, client):
        response = client.get("/create_tournaments")
        assert b'logout' in response.data

    def test_create_tournament(self, client):
        response = client.post('/create_tournaments',
                                      data={'club': 'Simply Lift',
                                            'name': 'Test',
                                            'date': '2020-10-22 13:30:00',
                                            'numberOfPlaces': '10'}
                                      )
        assert b'Great-tournament create !' in response.data
