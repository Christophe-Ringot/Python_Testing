import server
import pytest


@pytest.fixture()
def client():
    flask_app = server.app
    with flask_app.test_client() as client:
        yield client


class Test():

    def test_for_more_than_twelve(self, client):
        response = client.post('/purchase_places',
                                      data={'club': 'Simply Lift',
                                            'competition': 'new competition',
                                            'places': '15'}
                                      )
        assert b'you cannot book more than 12' in response.data

    def test_for_less_than_twelve(self, client):
        response = client.post('/purchase_places',
                                      data={'club': 'Simply Lift',
                                            'competition': 'new competition',
                                            'places': '12'}
                                      )
        assert b'Great-booking complete!' in response.data

    def test_for_a_correct_number_of_point(self, client):
        response = client.post('/purchase_places',
                          data={'club': 'She Lifts',
                                'competition': 'Fall Classic',
                                'places': '7'}
                          )
        assert response.status_code == 200

    def test_for_a_bad_number_of_places(self, client):
        response = client.post('/purchase_places',
                          data={'club': 'Iron Temple',
                                'competition': 'new competition',
                                'places': '5'}
                          )
        message = b"Not enough points"
        assert message in response.data

    def test_for_past_competition(self,client):
        response = client.post('/purchase_places',
                          data={'club': 'Simply Lift',
                                'competition': 'Fall Classic',
                                'places': '12'}
                          )
        assert b'Competition already done' in response.data

    def test_for_new_competition(self,client):
        response = client.post('/purchase_places',
                          data={'club': 'She Lifts',
                                'competition': 'new competition',
                                'places': '10'}
                          )
        assert b'Great-booking complete!' in response.data

    def test_points_update(self,client):
        club = [c for c in server.clubs if c['name'] == 'Simply Lift'][0]
        points = int(club['points'])
        response = client.post('/purchase_places',
                          data={'club': 'Simply Lift',
                                'competition': 'new competition',
                                'places': '1'}
                          )
        updated_points = int(club['points'])
        assert updated_points != points

    def test_for_less_than_competition_capacity(self, client):
        response = client.post('/purchase_places',
                          data={'club': 'Iron Temple',
                                'competition': 'new competition 2',
                                'places': '3'}
                          )
        assert b'You cannot take more places than is available'\
               in response.data