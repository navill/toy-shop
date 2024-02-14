from locust import HttpUser, task, between


class ProductTest(HttpUser):
    wait_time = between(0.5, 2)

    @task
    def hello_world(self):
        self.client.get("/items/test")
