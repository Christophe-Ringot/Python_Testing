import server
import pytest


@pytest.fixture()
def client():
    flask_app = server.app
    with flask_app.test_client() as client:
        yield client


class Test():

    def test_status_code_200(self, client):
        email = {"email": "kate@shelifts.co.uk"}
        response = client.post('/show_summary', data=email)
        assert response.status_code == 200

    def test_should_show_summary_page(self, client):
        email = {"email": "kate@shelifts.co.uk"}
        response = client.post('/show_summary', data=email)
        assert b'Welcome, kate@shelifts.co.uk' in response.data

    def test_should_not_show_summary(self, client):
        email = {"email": "kate@shelifts.uk"}
        response = client.post('/show_summary', data=email,
                               follow_redirects=True)
        assert b'Sorry, that email wasnt found.' in response.data