import scrapy

class ShinsaItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    reg_start_at = scrapy.Field()
    reg_end_at = scrapy.Field()
    start_at = scrapy.Field()
    end_at = scrapy.Field()

class DanItem(scrapy.Item):
    shinsa_location = scrapy.Field()
    shinsa_start_at = scrapy.Field()
    name = scrapy.Field()

class DojoItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    province = scrapy.Field()
    province_code = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
