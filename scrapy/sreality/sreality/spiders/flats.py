import scrapy
from scrapy_requests import HtmlRequest


class FlatsSpider(scrapy.Spider):
    name = "flats"
    
    def start_requests(self):
        # TODO: parse also following pages to get the desired 500 results
        urls = ["https://www.sreality.cz/hledani/prodej/byty"]

        for url in urls:
            yield HtmlRequest(url=url, 
                              callback=self.parse, 
                              render=True, 
                              options={'sleep': 1, 'wait': 5})

    
    def parse(self, response):
        page = response.request.meta['page']

        # titles
        titles = page.html.find(".name.ng-binding")

        # pictures
        pic_elements = page.html.find("preact.ng-scope.ng-isolate-scope")

    
        for title, pic_element in zip(titles, pic_elements):
            img = pic_element.find("img[src]", first=True)
            # TODO: what to do if there is no pic
            # get() returns None
            img_url = img.attrs.get('src')

            # return a generator for the scraped item
            yield {
                # TODO: check encoding
                # in 'scrapy crawl flats' ouput it appears a bit weird
                # (only title, image_url is ok)
                "title": title.text,
                "url": img_url
            }
