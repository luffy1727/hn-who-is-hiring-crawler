import scrapy

class HackernewsItem(scrapy.Item):
    web = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    age = scrapy.Field()