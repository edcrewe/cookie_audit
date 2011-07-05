from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from settings import DOMAINS, URLS

class DomainSpider(BaseSpider):
    """ Domain spider crawls any subdomain that ends with *.mydomain.com 
        from the list of DOMAINS in settings
    """
    
    name = "domain"
    yield_allowed_domains = DOMAINS
    start_urls = URLS

    def parse(self, response):
        """ Generator func - Check its html - ie has encoding """
        if hasattr(response, 'encoding'):
            hxs = HtmlXPathSelector(response)
            for url in hxs.select('//a/@href').extract():
                url = self.domain_check(url)
                if url:
                    yield Request(url, callback=self.parse) 

    def domain_check(self, url):
        """ Test if top level domain is OK for next url 
            (so one link depth external)
        """
        original = url
        if url:
            if url.find('http')>-1:
                url = url.split('/')[2]
                for domain in self.yield_allowed_domains:        
                    if url.endswith(domain):
                        return original
        return ''
