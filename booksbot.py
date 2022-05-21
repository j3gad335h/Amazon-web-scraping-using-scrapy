import scrapy
from ..items import FlipkartbooksbotItem
from time import process_time

t1 = process_time()


class BooksbotSpider(scrapy.Spider):
    name = 'booksbot'
    page_num = 2
    start_urls = [
        'https://www.flipkart.com/books/pr?sid=bks&q=books&otracker=categorytree'
    ]

    def parse(self, response):

        items = FlipkartbooksbotItem()
        data = response.css('._4ddWXP')
        title = []
        price = []
        rating = []
        author = []
        for content in data:
            t = content.css('.s1Q9rs::text').extract()
            p = content.css('._8VNy32 ._30jeq3::text').extract()
            r = content.css('._1lRcqv ._3LWZlK::text').extract()
            a = content.css('._3Djpdu::text').extract()
            title.append(t)  # list method is useful
            price.append(p)  # adding as list element result in missing values ignored
            rating.append(r)
            author.append(a)

        items['title'] = title
        items['price'] = price
        items['rating'] = rating
        items['author'] = author

        yield items

        next_page = f'https://www.flipkart.com/books/pr?sid=bks&q=books&otracker=categorytree&page={str(BooksbotSpider.page_num)}'
        if BooksbotSpider.page_num <= 25:
            BooksbotSpider.page_num += 1
            yield response.follow(next_page, callback=self.parse)

        t2 = process_time()
        print(f"Time taken: {t2 - t1} seconds")
