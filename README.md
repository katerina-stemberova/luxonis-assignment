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
      * [ ] scrape multiple pages
    * [x] how to save it to a Postgresql DB
      * [x] run the DB in a container
      * [x] connect to the DB using [psycopg2](https://github.com/psycopg/psycopg2)
      * [x] output the scraped results to the DB
1. [ ] HTTP server
    * [ ] how to implement a simple server in python
    * [ ] how to display the scraped results
      * diplay a webpage
      * read stuff from DB and display it in a webpage
1. [ ] docker
    * [ ] dockerize everything
    * [ ] docker compose


## Assumptions

Python
* `scrapy` is installed
* `requests-html` is installed
* `scrapy-requests` is installed
* `psycopg2-binary` is installed

Docker
* postgres docker container is running locally (on 0.0.0.0:5432)

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

Using PostgreSQL without previous knowledge can be tricky. The easiest approach was found to be avoiding the local installation and running it directly in a docker container. The trickiest part is setting up the user, password, and authorization mode right. The only auth mode that seemed to work was "trust", i.e., setting `POSTGRES_HOST_AUTH_METHOD=trust` as an env variable when running the container.
