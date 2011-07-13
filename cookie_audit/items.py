# Define here the models for your scraped items
# switch to plain scrapy dicts if no django available

try:
    from models import CookieAuditItem, CrawlAuditItem
except:
    from dicts import CookieAuditItem, CrawlAuditItem
