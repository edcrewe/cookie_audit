from scrapy.contrib.downloadermiddleware.cookies import CookiesMiddleware
from cookie_audit.pipelines import JsonWriterPipeline
from scrapy.selector import HtmlXPathSelector
from cookie_audit.items import CookieAuditItem
from scrapy import log
COOKIE_ATTRS = ['version','name','value', 'port',
                'port_specified','domain','domain_specified', 
                'domain_initial_dot','path', 'path_specified', 
                'secure', 'expires', 'discard', 
                'comment', 'comment_url', 'rest', 'rfc2109']

class SaveCookiesMiddleware(CookiesMiddleware):
    """ Subclass the standard cookies middleware but store the cookies data """
    pipe = JsonWriterPipeline()

    def process_response(self, request, response, spider):
        if 'dont_merge_cookies' in request.meta:
            return response

        # extract cookies from Set-Cookie and drop invalid/expired cookies
        jar = self.jars[spider]
        jar.extract_cookies(response, request)
        # cookie_audit - add save cookies
        self._save_cookies(response, request, jar)
        self._debug_set_cookie(response)

        return response

    def _debug_cookie(self, request):
        """log Cookie header for request - if not empty"""
        if self.debug:
            c = request.headers.get('Cookie')
            c = c and [p.split('=')[0] for p in c.split(';')]
            if c:
                log.msg('Cookie: %s for %s' % (c, request.url), level=log.DEBUG)


    def _debug_set_cookie(self, response):
        """log Set-Cookies headers but exclude cookie values"""
        if self.debug:
            cl = response.headers.getlist('Set-Cookie')
            if cl:
                res = []
                for c in cl:
                    kv, tail = c.split(';', 1)
                    k = kv.split('=', 1)[0]
                    res.append('%s %s' % (k, tail))
                if res:
                    log.msg('Set-Cookie: %s from %s' % (res, response.url))


    def _save_each_cookie(self, cookie, hxs, url):
        """ Save cookie data and setting page info """
        if cookie:
            item = CookieAuditItem()
            for attr in COOKIE_ATTRS:
                item[attr] = str(getattr(cookie, attr, ''))
            if hxs:
                item['url'] = url
                title = hxs.select('/html/head/title/text()').extract()
                if title:
                    item['page_title'] = title[0]
                h1 = hxs.select('/html/body/h1/text()').extract()
                if h1:
                    item['page_h1'] = h1[0]
            self.pipe.process_item(item, hxs)

    def _save_cookies(self, response, request, jar):
        """Save responses where cookies are set """
        if response:
            hxs = HtmlXPathSelector(response)
            cookies = jar.make_cookies(response, request)
            for cookie in cookies:
                self._save_each_cookie(cookie, hxs, response.url)
            return
