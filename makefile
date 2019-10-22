.PHONY: delete start
build: Dockerfile
	docker build -t ppage .

delete:
	docker rm -f mypp

start:
	docker run --name mypp -p 80:80 ppage

restart:
	docker rm -f mypp && docker build -t ppage . && docker run --name mypp -d -p 80:80 ppage
