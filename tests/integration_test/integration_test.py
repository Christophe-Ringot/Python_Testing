import pytest
import server


@pytest.fixture()
def client():
    server.app.testing = True
    server.clubs = server.load_clubs()
    server.competitions = server.load_competitions()
    with server.app.test_client() as client:
        return client


class TestIntegration():

    def test_client_can_login_and_logout(self, client):
        index = client.get("/")
        login = client.get("/", data={'email': 'john@simplylift.co'})
        logout = client.get("/logout")

        assert index.status_code == 200
        assert login.status_code == 200
        assert logout.status_code == 302

    def test_client_login_and_book_places_and_logout(self, client):

        client.get("/")
        client.get("/", data={'email': 'john@simplylift.co'})
        client.get("/show_summary")
        client.get("book/new%20competition/Simply%20Lift")
        client.get("/show_summary")
        logout = client.get("/logout")

        club_points = server.clubs[0]['points']
        competition_places = server.competitions[2]['numberOfPlaces']

        client.post("/purchase_places",
                    data={'places': 1, 'club': 'Simply Lift',
                               'competition': 'new competition'},
                    follow_redirects=True)

        new_club_points = server.clubs[0]['points']
        new_competition_point = server.competitions[2]['numberOfPlaces']

        assert new_club_points == 14
        assert new_competition_point == 149
        assert logout.status_code == 302

    def test_client_login_create_tournament_and_logout(self, client):

        client.get("/")
        client.get("/", data={'email': 'john@simplylift.co'})
        client.get("/show_summary")
        client.get("/create_tournaments")
        logout = client.get("/logout")

        club_points = server.clubs[0]['points']
        competition_places = server.competitions[2]['numberOfPlaces']

        response = client.post('/create_tournaments',
                                      data={'club': 'Simply Lift',
                                            'name': 'Test',
                                            'date': '20203-10-22 13:30:00',
                                            'numberOfPlaces': '10'},
                               follow_redirects=True)

        assert b'Great-tournament create !' in response.data
        assert logout.status_code == 302
