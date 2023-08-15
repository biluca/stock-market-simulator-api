.PHONY: dev

user:
	python3 manage.py createsuperuser

migrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

run:
	python3 manage.py runserver

shell:
	python3 manage.py shell

lint:
	pylint --load-plugins pylint_django --django-settings-module=assessment.settings **/*.py

black:
	python3 -m black --target-version=py37 .


