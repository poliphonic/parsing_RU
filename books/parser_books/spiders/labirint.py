import scrapy
from scrapy.http import HtmlResponse
from parser_books.items import ParserBooksItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['www.labirint.ru']
    start_urls = ['https://www.labirint.ru/genres/3136/?page=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//div[@class="pagination-next"]/a/@href'
                                   ).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        books_links = response.xpath('//a[@class="product-title-link"]/@href'
                                     ).getall()

        for link in books_links:
            yield response.follow(link, callback=self.parse_books)

    def parse_books(self, response: HtmlResponse):
        book_name = response.xpath('//a/span[@class="product-title"]/text()'
                                   ).get()
        book_author = response.xpath('//div[@class="product-author"]/a/@title'
                                     ).get()
        book_price = response.xpath('//span[@class="price-val"]/span//text()'
                                    ).get()
        old_book_price = response.xpath('//span[@class="price-old"]/span//'
                                        'text()').get()
        book_url = response.url
        yield ParserBooksItem(name=book_name, author=book_author,
                              price=book_price, old_price=old_book_price,
                              url=book_url)
