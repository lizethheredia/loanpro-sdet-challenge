import pytest
import requests
import os

BASE_URL = os.getenv("BASE_URL")
ENV = "dev"


class TestGetUsers:
    def test_get_all_users_returns_200(self, dev_url):
        response = requests.get(f"{dev_url}/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestCreateUser:
    def test_create_user_returns_201(self, dev_url, sample_user):
        response = requests.post(f"{dev_url}/users", json=sample_user)
        assert response.status_code == 201
        assert response.json()["email"] == sample_user["email"]

    def test_create_duplicate_user_returns_409(self, dev_url, sample_user):
        requests.post(f"{dev_url}/users", json=sample_user)
        response = requests.post(f"{dev_url}/users", json=sample_user)
        assert response.status_code == 409

    def test_create_user_missing_fields_returns_400(self, dev_url):
        response = requests.post(f"{dev_url}/users", json={"name": "No Email"})
        assert response.status_code == 400

    def test_create_user_invalid_age_returns_400(self, dev_url):
        response = requests.post(
            f"{dev_url}/users",
            json={"name": "Bad Age", "email": "badage@example.com", "age": 200},
        )
        assert response.status_code == 400


class TestGetUserByEmail:
    def test_get_existing_user_returns_200(self, dev_url, sample_user):
        requests.post(f"{dev_url}/users", json=sample_user)
        response = requests.get(f"{dev_url}/users/{sample_user['email']}")
        assert response.status_code == 200
        assert response.json()["email"] == sample_user["email"]

    def test_get_nonexistent_user_returns_404(self, dev_url):
        response = requests.get(f"{dev_url}/users/nobody@example.com")
        assert response.status_code == 404


class TestUpdateUser:
    def test_update_user_returns_200(self, dev_url, sample_user):
        requests.post(f"{dev_url}/users", json=sample_user)
        updated = {**sample_user, "name": "Jane Updated", "age": 31}
        response = requests.put(f"{dev_url}/users/{sample_user['email']}", json=updated)
        assert response.status_code == 200
        assert response.json()["name"] == "Jane Updated"

    def test_update_nonexistent_user_returns_404(self, dev_url, sample_user):
        response = requests.put(f"{dev_url}/users/nobody@example.com", json=sample_user)
        assert response.status_code == 404


class TestDeleteUser:
    def test_delete_user_returns_204(self, dev_url, sample_user, auth_headers):
        requests.post(f"{dev_url}/users", json=sample_user)
        response = requests.delete(
            f"{dev_url}/users/{sample_user['email']}", headers=auth_headers
        )
        assert response.status_code == 204

    def test_delete_without_auth_returns_401(self, dev_url, sample_user):
        requests.post(f"{dev_url}/users", json=sample_user)
        response = requests.delete(f"{dev_url}/users/{sample_user['email']}")
        assert response.status_code == 401

    def test_delete_nonexistent_user_returns_404(self, dev_url, auth_headers):
        response = requests.delete(
            f"{dev_url}/users/nobody@example.com", headers=auth_headers
        )
        assert response.status_code == 404
