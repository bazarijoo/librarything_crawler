from scrapy import Item, Field


class LibrarythingReview(Item):
    field_order = ['title', 'author', 'text', 'username', 'rating']

    title = Field()
    author = Field()
    text = Field()
    username = Field()
    rating = Field()