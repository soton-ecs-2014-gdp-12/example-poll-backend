from locust import HttpLocust, TaskSet, task
import random
import json


class UserBehavior(TaskSet):

    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def vote(self):
        val = random.randint(1, 20)
        self.client.post("/vote", json.dumps(dict(questionResult=val, annotation=val,  result=val)))

    @task(3)
    def results(self):
        val = random.randint(1, 20)
        self.client.get('/results/' + str(val) + '/' + str(val))


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000