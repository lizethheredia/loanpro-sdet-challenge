from dotenv import load_dotenv
import os
import pytest
import requests

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
ENV = os.getenv("ENV", "dev")


@pytest.fixture
def env_url():
    return f"{BASE_URL}/{ENV}"


@pytest.fixture
def auth_headers():
    return {"Authentication": AUTH_TOKEN}


@pytest.fixture
def sample_user():
    return {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "age": 30
    }


@pytest.fixture(autouse=True)
def cleanup(env_url, auth_headers):
    yield
    try:
        requests.delete(
            f"{env_url}/users/jane@example.com",
            headers=auth_headers
        )
    except Exception:
        pass