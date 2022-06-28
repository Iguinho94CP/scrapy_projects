import scrapy


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['goodreads.com']
    start_urls = ['https://www.goodreads.com/quotes/tag/love']

    def parse(self, response):
        for quote in response.css('.leftContainer'):
            yield {
                'text': quote.css('.quoteText::text').get().strip(),
                'author': quote.css('.authorOrTitle::text').get().strip(),
                'tags': quote.css('.left a::text').getall(),
            }
        
        next_page = response.css('.next_page::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
