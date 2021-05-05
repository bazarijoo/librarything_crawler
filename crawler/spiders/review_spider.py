from librarything_crawler.items import LibrarythingReview
import scrapy


class ReviewSpider(scrapy.Spider):
    name = 'review'

    start_url = 'https://www.librarything.com/ajax_zeitgeist_reviewsmore.php?ztype=3'
    # allowed_domains = ['librarything.com']
    offset = 0

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        items = response.css('a')
        main_page_url = 'https://' + response.url.split("/")[-2]
        for i in range(0, len(items), 2):
            url = main_page_url + items[i].css('a::attr(href)').extract_first() + '/reviews'

            yield scrapy.Request(url=url, callback=self.parseBook)

    def create_ajax_request(self, work_id):
        url = 'https://www.librarything.com/ajax_profilereviews.php'
        formdata = {
            'view': "",
            'sort': '0',
            'offset': '0',
            'type': '3',
            'container': 'wp_reviews',
            'showCount': str(10000),
            'workid': str(work_id),
            'mode': 'profile'
        }

        return url, formdata

    def parseBook(self, response):
        title = response.css('div.headsummary h1::text').get()
        author = response.css('div.headsummary a::text').get()
        work_id = response.url.split('/')[-2]

        url, formdata = self.create_ajax_request(work_id)

        # for element in response.css('div.workSection div.bookReview'):
        #     rating_img_src = element.css('span.rating img::attr(src)').extract_first()
        #     digits = [s for s in rating_img_src if s.isdigit()]
        #     rating = ''.join(digits)

        yield scrapy.FormRequest(url, callback=self.parse_show_all_review, formdata=formdata,
                                 cb_kwargs={'title': title, 'author': author})

    def parse_show_all_review(self, response, title, author):
        for element in response.css('div.workSection div.bookReview'):
            review_text = element.css('div.commentText::text').get()
            username = element.css('div.commentFooter span.controlItems a::text').get()

            rating_img_src = element.css('span.rating img::attr(src)').extract_first()

            if rating_img_src:
                rating = ''.join([s for s in rating_img_src if s.isdigit()])
            else:
                rating = ''

            review = LibrarythingReview()
            review['title'] = title
            review['author'] = author
            review['text'] = review_text
            review['username'] = username
            review['rating'] = rating

            yield review