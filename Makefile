prepare-venv:
	if [ -d "venv" ]; then rm -r venv; fi; python3 -m venv venv && . venv/bin/activate && pip3 install -r uwsgi_flask_backend/requirements.txt

build:
	docker-compose build

start:
	docker-compose up

# docker save sgasse/uwsgi_flask_backend | ssh -C root@simongasse.de 'docker load' && \
