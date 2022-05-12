# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonScrapperItem(scrapy.Item):
    # define the fields for your item here like:
    p_name = scrapy.Field()
    p_reviews=scrapy.Field()
    p_price=scrapy.Field()
    url=scrapy.Field()
