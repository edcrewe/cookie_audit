# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

#from scrapy.contrib_exp.djangoitem import DjangoItem

from scrapy.item import Item, Field

class CookieAuditItem(Item):
    """ Store the cookie details """
    url = Field()
    page_title = Field()
    page_h1 = Field()
    version = Field()
    name = Field()
    value = Field()
    port = Field()
    port_specified = Field()
    domain = Field()
    domain_specified = Field()
    domain_initial_dot = Field()
    path = Field()
    path_specified = Field()
    secure = Field()
    expires = Field()
    discard = Field()
    comment = Field()
    comment_url = Field()
    rest = Field()
    rfc2109 = Field() 

class CrawlAuditItem(Item):
    """ Keep track of what is crawled """
    url = Field()
    links = Field()
    metatype = Field()
