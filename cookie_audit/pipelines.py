# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

#class CookieAuditPipeline(object):
#    def process_item(self, item, spider):
#        return item

import json

class JsonWriterPipeline(object):

    def __init__(self, filename='items.json'):
        self.file = open(filename, 'wb')

    def process_item(self, item):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
