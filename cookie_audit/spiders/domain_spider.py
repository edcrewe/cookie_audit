from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from cookie_audit.settings import DOMAINS, URLS
from cookie_audit.items import CrawlAuditItem
from cookie_audit.pipelines import JsonWriterPipeline

class DomainSpider(BaseSpider):
    """ Domain spider crawls any subdomain that ends with *.mydomain.com 
        from the list of DOMAINS in settings
    """
    
    name = "domain"
    yield_allowed_domains = DOMAINS
    start_urls = URLS
    pipe = JsonWriterPipeline('crawl.json')

    def parse(self, response):
        """ Generator func - Check its html - ie has encoding """
        item = CrawlAuditItem()
        item['url'] = response.url
        item['metatype'] = response.meta
        if hasattr(response, 'encoding'):
            hxs = HtmlXPathSelector(response)
            links = hxs.select('//a/@href').extract()
            links = set(links)
            if response.url in links:
                links.remove(response.url)
            item['links'] = len(links)
            self.pipe.process_item(item)
            for url in links:
                url = self.domain_check(url)
                if url:
                    yield Request(url, callback=self.parse) 
            # Just save crawled pages not files/images
            try:
                item.save()
            except:
                self.pipe.process_item(item)        

    def domain_check(self, url):
        """ Test if top level domain is OK for next url 
            (so one link depth external)
            Or if matches with start URLs so for example could use Google
            to ensure domain coverage, eg. 
            with http://www.google.co.uk/search?q=site:*.mydomain.com
        """
        original = url
        if url:
            if url.find('http')>-1:
                url = url.split('/')[2]
                for domain in self.yield_allowed_domains:        
                    if url.endswith(domain):
                        return original
                for start in self.start_urls:
                    if url.startswith(start):
                        return original
        return ''
