# locustfile.py
from locust import HttpUser, between, task


class LoadTest(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def test_root(self):
        self.client.get("/system/hostname")

    @task(2)
    def test_cpu(self):
        self.client.get("/performance/cpu")

    # @task(1)
    # def test_memory(self):
    #     self.client.get("/performance/memory")
