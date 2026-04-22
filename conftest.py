from dotenv import load_dotenv
import os
import pytest
import requests
import subprocess

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
    return {"name": "Jane Doe", "email": "jane@example.com", "age": 30}


@pytest.fixture(autouse=True)
def cleanup(env_url, auth_headers):
    yield
    try:
        requests.delete(f"{env_url}/users/jane@example.com", headers=auth_headers)
    except Exception:
        pass


def pytest_runtest_logreport(report):
    if report.failed and os.getenv("CREATE_GITHUB_ISSUES") == "true":
        title = f"[BUG] {report.nodeid}"
        error = str(report.longrepr) if report.longrepr else "No error details"
        body = (
            f"## Failing Test\n"
            f"{report.nodeid}\n\n"
            f"## Error\n"
            f"{error}\n\n"
            f"## Environment\n"
            f"- ENV: {os.getenv('ENV')}\n"
            f"- BASE_URL: {os.getenv('BASE_URL')}\n"
        )

        # Check if issue already exists
        result = subprocess.run(
            ["gh", "issue", "list", "--search", title, "--json", "title"],
            capture_output=True,
            text=True
        )

        if title not in result.stdout:
            subprocess.run([
                "gh", "issue", "create",
                "--title", title,
                "--body", body,
                "--label", "bug"
            ])
