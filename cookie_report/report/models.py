from django.db import models

# Create your models here.

class CookieAuditModel(models.Model):
    """ Store the cookie details """
    url = models.URLField(max_length=500, blank=True, default='',
                          help_text = 'Crawled url')
    page_title = models.CharField(max_length=500, null=True, blank=True)
    page_h1 = models.CharField(max_length=500, null=True, blank=True)
    version = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    value = models.TextField(blank=True)
    port = models.PositiveSmallIntegerField(null=True, default=80)
    port_specified = models.PositiveSmallIntegerField(blank=True, null=True)
    domain = models.CharField(max_length=255, null=True)
    domain_specified = models.BooleanField(default=False)
    domain_initial_dot = models.BooleanField(default=False)
    path = models.CharField(max_length=500, null=True)
    path_specified = models.BooleanField(default=False)
    secure = models.BooleanField(default=False)
    expires = models.DateTimeField(null=True)
    discard = models.BooleanField(default=False)
    comment = models.CharField(max_length=500, null=True)
    comment_url = models.URLField(max_length=500, null=True, default='')
    rest = models.CharField(max_length=100, null=True)
    rfc2109 = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s at %s' % (self.name, self.url)

class CrawlAuditModel(models.Model):
    """ Keep track of what is crawled """
    url = models.URLField(max_length=500, null=True, default='')
    links = models.PositiveSmallIntegerField(null=True)
    metatype = models.TextField(null=True)

    def __unicode__(self):
        return self.url
