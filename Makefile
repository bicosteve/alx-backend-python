environment:
	pipenv shell

server:
	python ./messaging_app/manage.py runserver


install:
	pipenv install -r requirements.txt


