# Define here the models for your scraped items
# switch to plain scrapy dicts if no django available

#try:
#    from models import CookieAuditItem, CrawlAuditItem
#except:
#    from dicts import CookieAuditItem, CrawlAuditItem

import os, sys, site
THISPATH = os.path.dirname(__file__)
sys.path.append(THISPATH.replace('cookie_audit','cookie_report'))
site.addsitedir(THISPATH.replace('uob/cookie_audit','/lib/python2.6/site-packages'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_settings'

from cookie_report.report.models import CookieAuditModel, CrawlAuditModel
from scrapy.contrib_exp.djangoitem import DjangoItem


class CookieAuditItem(DjangoItem):
    """ Store the cookie details """
    django_model = CookieAuditModel

class CrawlAuditItem(DjangoItem):
    """ Keep track of what is crawled """
    django_model = CrawlAuditModel
