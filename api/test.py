from locust import HttpUser, task, between
import random

class ApiUser(HttpUser):
    wait_time = between(1, 3)  # wait 1-3s between tasks
    
    questions = [
        "What is the capital of France?",
        "How do I install the theme?",
        "What is Academy LMS?",
        "How can I enable popup pro?",
        "Tell me about the changelog",
        "How do I activate the license?",
        "What are the basic site settings?",
        "How do I use auction course?",
        "What is the theme customization process?",
        "How do I import demo contents?"
    ]

    @task
    def say_my_name(self):
        question = random.choice(self.questions)
        self.client.post("/ask-question", json={"question": question})
