#from datetime import datetime

from django.contrib import admin
from django.contrib.admin import ModelAdmin 

from report.models import CookieAuditModel, CrawlAuditModel

admin.site.register(CookieAuditModel)
admin.site.register(CrawlAuditModel)
