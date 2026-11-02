.PHONY: install run migrate migrations superuser test cov lint format check docker-up docker-down

install:
	pip install -r requirements/dev.txt
	pre-commit install

run:
	python manage.py runserver

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

superuser:
	python manage.py createsuperuser

test:
	pytest

cov:
	pytest --cov=apps --cov-report=term-missing

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .

check:
	python manage.py check
	python manage.py makemigrations --check --dry-run
	python manage.py spectacular --validate --fail-on-warn --file /dev/null

docker-up:
	docker compose up --build

docker-down:
	docker compose down
