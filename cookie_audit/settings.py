# Scrapy settings for cookie_audit project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'cookie_audit'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['cookie_audit.spiders']
NEWSPIDER_MODULE = 'cookie_audit.spiders'
DEFAULT_ITEM_CLASS = 'cookie_audit.items.CookieAuditItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

