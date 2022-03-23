from locust import HttpUser, task, between
import server


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.comp = "new competition"
        self.club = "She Lifts"
        self.client.post("/show_summary", {"email": "kate@shelifts.co.uk"})

    @task
    def index(self):
        with self.client.get(f'/',
                             catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure('resquest expired')

    @task
    def booking_display(self):
        with self.client.get(f'/book/{self.comp}/{self.club}',
                             catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure('resquest expired')

    @task
    def purchasing(self):
        form = {
            "competition": self.comp,
            "club": self.club,
            "places": 1
                }
        with self.client.post('/purchase_places',
                              form, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure('resquest expired')

    @task
    def create_tournament(self):
        form = {
            "name": "new competition",
            "date": "2023-10-22 13:30:00",
            "numberOfPlaces": 1
        }
        self.client.post('/create_tournaments', form, catch_response=True)

    @task
    def logout(self):
        with self.client.get(f'/logout',
                             catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure('resquest expired')