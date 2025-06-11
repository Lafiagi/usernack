# 🍕 Usersnack API

**Usersnack** is a pizza ordering API built with Django and Django REST Framework. It supports ordering pizzas with extras, calculating prices, and tracking inventory.

### 🌍 Hosted at:

**🔗** [https://api.ile-wa.com/usersnack/swagger/](https://api.ile-wa.com/usersnack/swagger/) — Swagger UI (deployed using Gunicorn + Apache on Ubuntu)

---

## 🚀 Features

* Order pizzas with extras
* Swagger documentation with DRF Spectacular
* CI with GitHub Actions + Flake8 linting + Pytest tests
* Dockerized deployment with Postgres and Redis
* Sample data preloaded in Docker with `populate_data` command

---

## 🧱 Tech Stack

* Python 3.13 / Django 5.2
* Django REST Framework
* PostgreSQL
* Redis (for Caching and Celery support)
* Gunicorn + Apache (production deployment)
* Docker & Docker Compose
* GitHub Actions (CI)

---

## 📦 Requirements

* Python ≥ 3.10
* PostgreSQL ≥ 13 (locally or via Docker)
* Redis (optional, for Celery)

---

## ⚙️ Running Locally (venv)

```bash
# 1. Clone the repo
git clone https://github.com/Lafiagi/usersnack.git
cd usersnack

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Then edit `.env` with your DB and secret key

# 5. Apply migrations
python manage.py migrate

# 6. (Optional) Load sample data
python manage.py populate_data

# 7. Run the server
python manage.py runserver
```

---

## 🐳 Running with Docker

```bash
# 1. Copy and configure environment
cp .env.example .env
# Set DB name, user, password

# 2. Start the stack
docker-compose up --build
```

* The API will be available at: [http://0.0.0.0:8000/swagger/](http://127.0.0.1:8000/swagger/)
* Sample data is automatically loaded with `populate_data` via Docker.

---

## 🧪 Running Tests

```bash
pytest
```

Tests use `pytest-django` and are located in `pizza/tests/`.

---

## ✅ Code Quality

* All code is linted using **flake8**
* CI is enforced via **GitHub Actions**:

  * ✅ Lint with `flake8`
  * ✅ Run all `pytest` tests
  * ✅ Runs on push to `main` and PRs

---

## 🔐 Environment Configuration (.env)

A sample `.env.example` is provided. You need:

```env
DEBUG=1
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:pass@localhost:5432/db
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=db
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
VERSION=v1
```

---

## 🧪 Swagger & API Docs

* Local: [http://127.0.0.1:8000/usersnack/swagger/](http://127.0.0.1:8000/usersnack/swagger/)
* Production: [https://api.ile-wa.com/usersnack/swagger/](https://api.ile-wa.com/usersnack/swagger/)

---

## 🛠 Deployment Stack

* Ubuntu + Apache (mod-proxy + mod-ssl)
* Gunicorn (running as a systemd service)
* Static and media handled via Apache aliases

---

Let me know if you'd like this split into sections like `/docs/`, or want badges for test/lint status using GitHub Actions.
