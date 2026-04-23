from locust import HttpUser, task, between


class LoanProUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_all_users(self):
        self.client.get("/dev/users")

    @task(2)
    def get_user_by_email(self):
        self.client.get("/dev/users/jane@example.com")

    @task(1)
    def get_nonexistent_user(self):
        self.client.get("/dev/users/nobody@example.com")