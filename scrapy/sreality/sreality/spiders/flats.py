import scrapy
from scrapy_requests import HtmlRequest


class FlatsSpider(scrapy.Spider):
    name = "flats"
    
    def start_requests(self):
        urls = ["https://www.sreality.cz/hledani/prodej/byty"]

        # generate all pages to scrape
        # currently hardcoded to get 500 results in total
        for i in range(2,26):
            url = f"https://www.sreality.cz/hledani/prodej/byty?strana={i}"
            urls.append(url)

        # process each url in the list
        for url in urls:
            yield HtmlRequest(url=url, callback=self.parse, render=True, options={'sleep': 1, 'wait': 5})

    
    def parse(self, response):
        page = response.request.meta['page']

        # titles
        titles = page.html.find(".name.ng-binding")

        # pictures
        pic_elements = page.html.find("preact.ng-scope.ng-isolate-scope")

    
        # return a generator for the scraped item
        for title, pic_element in zip(titles, pic_elements):
            img = pic_element.find("img[src]", first=True)
            img_url = img.attrs.get('src')

            yield {
                "title": title.text,
                "url": img_url
            }
