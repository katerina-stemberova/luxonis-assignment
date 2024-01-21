import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.flats import FlatsSpider

# FIXME: this is ugly, ideally should be handled in docker-compose.yml
time.sleep(7)

# Get the project settings
settings = get_project_settings()

# Create a CrawlerProcess with project settings
process = CrawlerProcess(settings)

# Add the spider to the process
process.crawl(FlatsSpider)

# Start the crawling process
process.start()
