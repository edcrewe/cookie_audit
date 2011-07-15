from django.db import models

# Create your models here.

class CookieAuditModel(models.Model):
    """ Store the cookie details """
    url = models.URLField(max_length=500, blank=True, default='',
                          help_text = 'Crawled url')
    page_title = models.CharField(max_length=500, blank=True)
    page_h1 = models.CharField(max_length=500, blank=True)
    version = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    value = models.TextField(blank=True)
    port = models.PositiveSmallIntegerField(null=False, default=80)
    port_specified = models.PositiveSmallIntegerField(blank=True)
    domain = models.CharField(max_length=255, blank=True)
    domain_specified = models.BooleanField(default=False)
    domain_initial_dot = models.BooleanField(default=False)
    path = models.CharField(max_length=500, blank=True)
    path_specified = models.BooleanField(default=False)
    secure = models.BooleanField(default=False)
    expires = models.DateTimeField()
    discard = models.BooleanField(default=False)
    comment = models.CharField(max_length=500, blank=True)
    comment_url = models.URLField(max_length=500, blank=True, default='')
    rest = models.CharField(max_length=100, blank=True)
    rfc2109 = models.BooleanField(default=False)

class CrawlAuditModel(models.Model):
    """ Keep track of what is crawled """
    url = models.URLField(max_length=500, blank=True, default='')
    links = models.PositiveSmallIntegerField(blank=True)
    metatype = models.TextField(blank=True)
