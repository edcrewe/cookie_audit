from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from settings import DOMAINS, URLS
from items import CrawlAuditItem
from pipelines import JsonWriterPipeline

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
            #flash, javascript and framesets can be external cookie sources
            embed = hxs.select('//embed/@src').extract()
            embed.extend(hxs.select('//object/@data').extract())
            embed.extend(hxs.select('//script/@src').extract())
            embed.extend(hxs.select('//frameset/@src').extract())
            embed = set(embed)
            for url in embed:
                # Store embedded scripts / flash since also source of cookies
                # can we save flash cookies? - maybe needs separate firefox grab of url
                if url.startswith('/'):
                    url = 'http://www.bris.ac.uk%s' % url
                elif not url.startswith('http'):
                    rurl = response.url
                    if not rurl.endswith('/'):
                        urlbits = response.url.split('/')
                        rurl = '/'.join(urlbits[-1])
                    url = '%s%s' % (rurl, url)
                if not self.crawled(url):
                    newresponse = Request(url)
                    newitem = CrawlAuditItem()                
                    newitem['url'] = response.url
                    newitem['metatype'] = response.meta
                    newitem['links'] = 0
                    newitem.save()
            for url in links:
                if not self.crawled(url):
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
                for start in self.start_urls:
                    if url.startswith(start):
                        return original
                for domain in self.yield_allowed_domains:        
                    if url.endswith(domain):
                        return original
        return ''

    def crawled(self, url):
        """ Dont recrawl same urls """
        try:
            item = CrawlAuditItem.get(url__exact=url)
            if item:
                return True
        except:
            pass
        return False
