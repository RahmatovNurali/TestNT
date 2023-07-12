mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

admin:
	python3 manage.py createsuperuser

del:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

req:
	pip3 freeze > requirements.txt

install-req:
	pip3 install -r requirements.txt

check:
	flake8 .
	isort .