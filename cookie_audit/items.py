# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CookieAuditItem(Item):
    """ Store the cookie details """
    host = Field()
    path = Field()
    name = Field()
    session = Field()
    secure = Field()
    p3p_policy = Field()
    p3p_status = Field()
    expires = Field()
    created = Field()
    last_accessed = Field()
