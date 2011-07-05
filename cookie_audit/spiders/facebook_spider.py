from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class FacebookSpider(BaseSpider):
    """ Test spider that just crawls the anonymous part of facebook
        returning the cookies it sets
    """
    
    name = "facebook.com"
    allowed_domains = ["facebook.com"]
    start_urls = [
                  "http://www.facebook.com",
                  ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
        title = hxs.select('/title')
        h1 = hxs.select('/h1')
        print title, h1
