# Makefile

.PHONY: runserver migrate createsuperuser startapp

runserver:
	poetry run python3 manage.py runserver

migrate:
	poetry run python3 manage.py migrate

createsuperuser:
	poetry run python3 manage.py createsuperuser

startapp:
	poetry run python3 manage.py startapp storage
