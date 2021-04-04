import scrapy


class LocationSpider(scrapy.Spider):
    name = 'location'
    allowed_domains = ['twitter.com']
    start_urls = ['http://twitter.com/']

    def parse(self, response):
        pass
