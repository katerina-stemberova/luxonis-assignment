# Luxonis assignment

## The assignment

Use `scrapy` framework to scrape the first 500 items (title, image url) from https://www.sreality.cz (flats, sell) and save it in the Postgresql database. Implement a simple HTTP server in python and show these 500 items on a simple page (title and image) and put everything to single docker compose command so that I can just run `docker-compose up` in the Github repository and see the scraped ads on http://127.0.0.1:8080 page.

Use the simplest way to achieve the goal.


## Steps

1. [ ] scraping - [scrapy](https://scrapy.org)
    * [x] how to scrape anything with `scrapy`
    * [ ] scrape what we want with `scrapy`
      * [x] scrape dynamic pages with [requests-html](https://github.com/psf/requests-html) 
        * using [scrapy-requests](https://github.com/rafyzg/scrapy-requests) - `scrapy`'s middleware
      * [x] scrape multiple pages
    * [x] how to save it to a Postgresql DB
      * [x] run the DB in a container
      * [x] connect to the DB using [psycopg2](https://github.com/psycopg/psycopg2)
      * [x] output the scraped results to the DB
1. [x] HTTP server
    * [x] how to implement a simple server in python
    * [x] how to display the scraped results
      * display a webpage
      * read stuff from DB and display it in a webpage
1. [x] docker
    * [x] dockerize scrapy
    * [x] docker compose


## Assumptions and limitations

Docker
* data in the DB is ephemeral, i.e. it is lost when the Postgres container stops

Flask
* the HTTP server currently used is intended just for development


## Findings and notes

* sreality.cz relies heavily on javascript, which `scrapy` is unable to process on its own -> another tool needs to be used - `requests-html` (in the form of `scrapy-requests`)
* `scrapy-requests` settings (their README is wrong):
  ```
  DOWNLOADER_MIDDLEWARES = {
      'scrapy_requests.middleware.RequestsMiddleware': 543,
  }
  ```
  

## Process

Scraping

scrapy is well documented and many tutorials exist, it is thus not too difficult to get started even without previous knowledge of the library. The problem comes when you need to scrape a dynamic page, i.e. one that uses javascript to fetch its content, because scrapy isn't able to handle that on its own. That's exactly our case because sreality.cz relies heavily on javascript, and thus help of an additional tool is needed. The general idea is to use headless browser to (pre)render the page and use scrapy on the results afterwards. Several tools exist - Splash, Playwright, html-requests, etc. I found html-requests the simplest to use, though making the middleware scrapy-requests work wasn't straightforward because their README was inaccurate. But after some trial and error it finally worked.

Database

Using PostgreSQL without previous knowledge can be tricky. The easiest approach was found to be avoiding the local installation and running it directly in a docker container. The trickiest part is setting up the user, password, and authorization mode right. The only auth mode that seemed to work was "trust", i.e., setting `POSTGRES_HOST_AUTH_METHOD=trust` as an env variable when running the container. When "trust" is used, password becomes unnecessary, but `psycopg2` complains if it isn't provided.

Containers

When running scrapy in a container using a script, WORKDIR has to be set to the directory of the script, otherwise scrapy will just use default settings and not those from the project.

Pyppeteer in the container was spitting out errors: "pyppeteer.errors.BrowserError: Browser closed unexpectedly". After consulting [SO](https://stackoverflow.com/questions/72006251/pyppeteer-and-docker-error-browser-closed-unexpectedly), the problem turned out to be missing Chromium requirements. When those were installed in the container, it started working.

Postgres needs to have a static IP that will be known to scrapy in advance (at the time of docker build).
Example of how to create it: https://stackoverflow.com/questions/27937185/assign-static-ip-to-docker-container

^ containers need to be a part of the same network

Flask

The template file (html) needs to be stored in `templates` subfolder, otherwise Flask fails to find it.
