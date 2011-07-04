from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from cookie_audit.items import CookieAuditItem
SESSIONIDS = ['PHPSESSID','JSESSIONID','_CMS_ZopeId']
GET_VALUES = ['path','expires','created','last_accessed']

class UoBSpider(BaseSpider):
    """ Test spider that just crawls the anonymous part of facebook
        returning the cookies it sets
    """
    
    name = "uob"
    yield_allowed_domains = ["bris.ac.uk","bristol.ac.uk"]
    start_urls = [
                  "http://www.bris.ac.uk/science",
                  #"http://www.bristol.ac.uk/"
                  ]
    cookies = []

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        if response.headers.getlist('Set-Cookie'):
            self._set_cookie(response, hxs)
        for url in hxs.select('//a/@href').extract():
            if self.cookies:
                raise Exception(self.cookies)
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

    def _set_cookie(self, response, hxs):
        """log Set-Cookies headers but exclude cookie values"""
        if response:
            cl = response.headers.getlist('Set-Cookie')
            res = []
            for c in cl:
                cookie = CookieAuditItem()
                cookie['session'] = False
                cookie['secure'] = False
                for kv in c.split(';'):
                    try:
                        for k,v in kv.split('='):
                            if k in GET_VALUES:
                                cookie[k] = v
                                if k in SESSIONIDS:
                                    cookie['session'] = True
                    except:
                        pass
                    kv, tail = c.split(';', 1)
                    k = kv.split('=', 1)[0]
                    cookie['name'] = '%s %s' % (k, tail) 
                cookie['path'] = response.url
                cookie['content'] = c
                title = hxs.select('/html/head/title/text()').extract()
                if title:
                    cookie['page_title'] = title[0]
                h1 = hxs.select('/html/body/h1/text()').extract()
                if h1:
                    cookie['page_h1'] = h1[0]
                self.cookies.append(cookie)    
        if self.debug:
            log.msg('Set-Cookie: %s from %s' % (res, response.url))
