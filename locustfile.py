import os
from locust import HttpUser, task, between

class BenchmarkUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def generate(self):
        self.client.post("/generate", json={
            "prompt": "Explain what an API is in one sentence.",
            "model": os.getenv("LOAD_TEST_MODEL", "llama3.2:1b"),
            "max_tokens": 64,
            "temperature": 0.2
        })
