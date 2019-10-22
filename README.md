# Personal Landingpage with HTML, CSS, nginx and docker

This repository features my basic personal landing page with HTML and CSS. It includes a few decent animations. Everything works without JavaScript and is pure HTML/CSS-powered.

To host the site, I bundle it with nginx in a docker container that I run on one of my virtual servers. Given that I seldomly change the page, I do not push it to a container registry but upload it directly to my server.



Build docker image
```
docker build -t ppage .
```


Export docker image, push via SSH and load into remote docker
```
docker save ppage | ssh -C root@simongasse.de docker load
```


Run docker image on the server
```
docker run --name mypp -d -p 80:80 ppage
```
