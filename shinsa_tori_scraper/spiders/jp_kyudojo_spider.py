import scrapy
import re
from geopy.geocoders import Nominatim
from helpers.string_helper import convert_full_to_half
from ..items import DojoItem

class JpKyudojoSpider(scrapy.Spider):
    name = "jp_kyudojo_spider"
    allowed_domains = ["www.kyudo.jp"]
    start_urls = ["https://www.kyudo.jp/map/"]

    def parse(self, response):
        records = response.xpath(
            '/html/body/main/div[2]/div[2]/div[1]/div[3]/div[@class="gym"]'
        )

        for i in range(0, len(records)):
            print(f'index: {i}')
            record = records[i]
            item = DojoItem()
            geolocator = Nominatim(user_agent="jp_kyudojo_spider")

            address = record.xpath('text()[2]').get()
            if address:
                address = convert_full_to_half(address.strip())
            else:
                address = None

            p = record.xpath('text()[3]').get()
            phone = p.strip().split('：')

            lat = record.xpath('div[@class="lat"]/text()').get()
            lat = re.sub(r'[^0-9\.]+', '', lat)
            lng = record.xpath('div[@class="lng"]/text()').get()
            lng = re.sub(r'[^0-9\.]+', '', lng)
            location = None
            print(f'Latitude, Longitude: {lat}, {lng}')
            if lat and lng:
                location = geolocator.reverse(f'{lat}, {lng}')
            else:
                location = geolocator.geocode(address)

            item["name"] = convert_full_to_half(record.xpath('b/text()').get())
            item["address"] = address
            item["phone"] = convert_full_to_half(phone[1]) if len(phone) > 1 and phone[1] else None
            item["province"] = location.raw['address'].get('province') if location else None
            item["province_code"] = location.raw['address'].get('ISO3166-2-lvl4') if location else None
            item["latitude"] = lat
            item["longitude"] = lng
            yield item
