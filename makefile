.PHONY: delete start
build: Dockerfile
	docker build -t ppage .

delete:
	docker rm -f mypp

start:
	docker run --name mypp -p 80:80 ppage

restart:
	docker rm -f mypp  || true && docker build -t ppage . && docker run --name mypp -d -p 80:80 ppage

updateRemote:
	docker build -t page . && ssh root@simongasse.de 'docker rm -f mypp || true' && docker save ppage | ssh -C root@simongasse.de docker load && ssh root@simongasse.de 'docker run --name mypp -d -p 80:80 ppage'
