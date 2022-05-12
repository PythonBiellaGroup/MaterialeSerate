import scrapy
from ..items import AmazonScrapperItem

class AmazonBotSpider(scrapy.Spider):
    name = 'amazon-bot'
    count=1
    start_urls = [
        'https://www.amazon.com/s?k=headphones&page=1&qid=1624791620&ref=sr_pg_3',
        "https://www.amazon.com/s?k=iphone&page=1&qid=1624792241&ref=sr_pg_2"               
        ]

    def parse(self, response):
        product=AmazonScrapperItem()
        name=response.css(".a-size-medium.a-text-normal::text").extract()
        no_reviews=response.css(".sg-col-12-of-20 .a-link-normal .a-size-base").css("::text").extract()
        price=response.css(".sg-col-12-of-20 .a-price-whole::text").extract()
        image_url=response.css(".s-image-fixed-height .s-image").css("::attr(src)").extract()
        product["p_name"]=name
        product["p_reviews"]=no_reviews
        product["p_price"]=price
        product["url"]=image_url
        yield product
    
        AmazonBotSpider.count+=1
        nxt_page="https://www.amazon.com/s?k=heaphones&page="+str(AmazonBotSpider.count)+"&qid=1624791620&ref=sr_pg_3"
        nxt_iphone_page="https://www.amazon.com/s?k=iphone&page="+str(AmazonBotSpider.count)+"&qid=1624792241&ref=sr_pg_2"
        if AmazonBotSpider.count<6:
            yield response.follow(nxt_page,callback=self.parse)
            yield response.follow(nxt_iphone_page,callback=self.parse)
