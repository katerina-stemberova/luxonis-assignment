# Luxonis assignment

## The assignment

Use `scrapy` framework to scrape the first 500 items (title, image url) from https://www.sreality.cz (flats, sell) and save it in the Postgresql database. Implement a simple HTTP server in python and show these 500 items on a simple page (title and image) and put everything to single docker compose command so that I can just run `docker-compose up` in the Github repository and see the scraped ads on http://127.0.0.1:8080 page.

Use the simplest way to achieve the goal.


## Steps

1. [ ] scraping
    * [ ] how to scrape anything with `scrapy`
    * [ ] how to scrape what we want with `scrapy`
    * [ ] how to save it to a Postgresql DB
1. [ ] HTTP server
    * [ ] how to implement a simple server in python
    * [ ] how to display the scraped results
      * diplay a webpage
      * read stuff from DB and display it in a webpage
1. [ ] docker
    * [ ] dockerize everything
    * [ ] docker compose
