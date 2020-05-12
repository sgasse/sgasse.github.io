# Personal Landingpage with HTML, CSS, nginx and docker

This repository features my basic personal landing page with HTML and CSS, served and templated with flask/jinja2. It includes a few decent animations. Everything works without JavaScript.

To host the site, I bundle it in a docker container running a uwsgi server. This is then served with a nginx docker container in a docker-compose setup on one of my virtual servers.

The background of the website changes according to the season. This is handeled by flask, which templates the right background through jinja2 into the style of the html file.

Additionally, I implemented a basic news crawler that queries the current top ten articles from a major German news site every hour. The sentiment of the articles are assessed with the word corpus of the project ['Deutscher Wortschatz/Leipzig Corpora Collection'](https://wortschatz.uni-leipzig.de/de/download) by the University of Leipzig. You can access the list of news colored by their sentiment at [simongasse.de/news](http://www.simongasse.de/news)


## Commands to build and deploy the website

Build docker image
```
docker-compose build
```

Start container environment
```
docker-compose up
```


## Commands for the previous version with one docker container

Export docker image, push via SSH and load into remote docker
```
docker save ppage | ssh -C root@simongasse.de docker load
```

Run docker image on the server
```
docker run --name mypp -d -p 80:80 ppage
```

Several of those commands are bundled in the `Makefile` for development.
