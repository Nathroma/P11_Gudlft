from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    
    def on_start(self):
        self.client.post("showSummary", {"email": "john@simplylift.co"})

    def on_stop(self):
        self.client.get("logout")

    @task
    def display(self):
        self.client.get("display")

    @task
    def booking(self):
        self.client.get("book/Fall%20Classic/She%20Lifts")

    @task
    def purchase(self):
        self.client.post("purchasePlaces", data={
            "club": "Simply Lift",
            "competition": "Fall Classic",
            "places": 5
        })
