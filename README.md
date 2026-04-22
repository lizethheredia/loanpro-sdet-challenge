# LoanPro SDET Challenge

API test suite for the LoanPro SDET take-home challenge.

## Tech Stack
- Python 3.11
- pytest
- requests
- Allure reporting
- GitHub Actions CI/CD

## Test Coverage
- `GET /users` — list all users
- `POST /users` — create user
- `GET /users/{email}` — get by email
- `PUT /users/{email}` — update user
- `DELETE /users/{email}` — delete user (auth required)

Both `dev` and `prod` environments run in parallel.

## Bugs Found
See [BUGS.md](BUGS.md) for the 3 bugs discovered.

## Allure Report
👉 [View Live Report](https://lizethheredia.github.io/loanpro-sdet-challenge/)

## Run Locally
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/test_users.py -v
```