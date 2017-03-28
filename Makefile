.PHONY: client server build

server:
	gunicorn server:app -c gunicorn.conf.py

client:
	python client.py

build:
	pip install -r requirements.txt
