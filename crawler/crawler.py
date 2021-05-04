import scrapy
from job import HackernewsItem

class JobSpider(scrapy.Spider):
    name = "job_spider"

    start_urls = ['https://news.ycombinator.com/item?id=27025922']

    def parse(self, response):
        SET_SELECTOR  = 'td.default'
        result = []
        i = 0
        for jobset in response.css(SET_SELECTOR):
            items = HackernewsItem()
            items['title'] = jobset.css('span.commtext.c00::text').extract()
            items['web'] = jobset.css('span.commtext a::attr(href)').get()
            items['content'] = jobset.css('p ::text').extract()
            items['age'] = jobset.css('span.age a::text').extract_first()

            yield items

        next_page = response.css('.morelink::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)






