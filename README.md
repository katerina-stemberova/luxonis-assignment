# Luxonis assignment

This repo contains a setup needed to automatically obtain the data to satisfy [the assignment](#the-assignment) below.


## The assignment

Use `scrapy` framework to scrape the first 500 items (title, image url) from https://www.sreality.cz (flats, sell) and save it in the Postgresql database. Implement a simple HTTP server in python and show these 500 items on a simple page (title and image) and put everything to single docker compose command so that I can just run `docker-compose up` in the Github repository and see the scraped ads on http://127.0.0.1:8080 page.

Use the simplest way to achieve the goal.


## What's in this repo

The project is composed of 3 containers:
* scrapy
* postgres
* http-server

that are bound together by `docker-compose.yml`.

### Scrapy

`Scrapy`is responsible for obtaining (scraping) the data from the https://www.sreality.cz website and saving them into the database.

It is a custom container that needs to be built from its Dockerfile in order to run it. Its data can be found in the `scrapy` subfolder.

### Postgres

`Postgres` is the database that stores, holds, and provides the data when requested.

It uses a standard Postgres image from DockerHub.

### Flask

`HTTP server` is implemented by Flask and presents the data on a webpage.

It is a custom container that needs to be built from its Dockerfile in order to run it. Its data can be found in the `http_server` subfolder.


## How to run it

1. Open up a terminal in the repo's root directory
1. Execute:
    ```
    docker compose up
    ```
1. Wait
    * it shouldn't take longer than 2-3 minutes on the first run when the images have to be built
1. When the scraping finishes, open http://127.0.0.1:8080 in a browser to view the results

### Additional info

Running `docker compose up` will build and run containers as defined in `docker-compose.yml`.

When the containers start running, you should see in the terminal that `postgres` (DB) and `flask` (HTTP server) booted up first. Scraping (the `scrapy` container) starts in a few seconds. It should finish in a minute or less.

When you see "scrapy exited with code 0" in the terminal, the  data is ready and can be viewed in a browser.


## Assumptions and limitations

### Scrapy

* number of pages processed on https://www.sreality.cz is not configurable (it's hardcoded to produce 500 results as per the assignment)
* number of parallel requests is set to 4 (down from default 16) because it's quite resource intensive due to the need to render each page in the headless browser. This way it shouldn't kill the user's computer, but it takes about a minute to retrieve all data.
* there is an initial delay (7 s) to enable the DB to start up hard set directly in the app's code which is ugly and not flexible. Ideally this would be set up in the `docker-compose.yml` or use some more advanced technique to check if the DB is available

### Postgres

* data in the DB is ephemeral, i.e. it is lost when the Postgres container stops

### Flask

* the simple HTTP server currently used is intended just for development

### General

* exception handling is rather basic


## Final comments

The setup provided in this repo is more of a MVP rather than a production-ready system, so treat it as such.

I didn't have a chance to test it on a machine other than my own (running Debian) which I also used for development of the code, so _"works on my machine"_ effect might occur.

Some of the current limitations shouldn't be too hard to overcome (e.g. the ephemeral Postgres data which could be simply solved by using a persistent volume), but I tried to make it as simple as possible (as also pointed out in the assignment description). Time constraints also played a role.

All in all, it should work for demonstration purposes, which was the overall goal.
