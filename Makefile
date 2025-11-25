mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

msg:
	python3 manage.py makemessages -l uz -l en

compile_msg:
	python3 manage.py compilemessages -i .venv

dbshell:
	docker exec -itu postgres pg psql -d rent_car

loaddata:
	python3 manage.py loaddata carbrand carcategory carcolor carfeature carprice cars feature

PHONE := $(word 2, $(MAKECMDGOALS))

admin:
	python3 manage.py createsuperuser --contact $(PHONE)

check:
	flake8 .
	isort .