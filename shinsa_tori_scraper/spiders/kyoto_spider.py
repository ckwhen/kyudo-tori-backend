import scrapy
import re
import uuid
from helpers.string_helper import convert_full_to_half
from helpers.date_helper import convert_reiwa_to_ce_year, get_annual_full_date, pgsql_format
from ..items import ShinsaItem, DanItem

class KyotoSpider(scrapy.Spider):
    name = "kyoto_spider"
    allowed_domains = ["kyotofu-kyudo.jp"]
    start_urls = ['https://kyotofu-kyudo.jp/jud_com_info.html']

    def parse(self, response):
        y = response.xpath('//*[@id="wsts"]/div/div[1]/div[1]/text()').get()
        y = self.get_year(convert_full_to_half(y))
        year = convert_reiwa_to_ce_year(int(y))

        records = response.xpath('//*[@id="jc"]/div/div[1]/table/tbody/tr')
        del records[0]

        for record in records:
            shinsa_item = ShinsaItem()
            dan_item = DanItem()
            id = str(uuid.uuid4())
            r = record.xpath('string(td/@rowspan)').get()
            rowspan = int(r.strip() or 0)

            if rowspan == 0:
                continue

            name = record.xpath('td[3]/text()').get()

            loc = record.xpath('td[4]/text()').get()
            if loc == '武道':
                loc = '武道センター'
            if loc == '綾部':
                loc = '綾部市総合運動公園弓道場'

            due = record.xpath('td[6]/text()').get()
            start = record.xpath('td[1]/text()').get()
            start_at = self.get_date(year, start)

            shinsa_item['id'] = id
            shinsa_item['name'] = name
            shinsa_item['location'] = loc
            shinsa_item['reg_end_at'] = self.get_date(year, due)
            shinsa_item['start_at'] = start_at
            yield shinsa_item

            for i in range(rowspan):
                d = records.xpath(f'//tr//following-sibling::tr[{i + 1}]/td[@class="type"]/text()').get()
                if d == '無指定':
                    continue
                d = re.sub(r'\s*', '', d)
                dan = 'sho'

                if d == '弐段':
                    dan = 'ni'
                if d == '参段':
                    dan = 'san'
                if d == '四段':
                    dan = 'yon'

                dan_item['shinsa_location'] = loc
                dan_item['shinsa_start_at'] = start_at
                dan_item['name'] = dan
                yield dan_item

    def get_year(self, input):
        return re.search('(\d+).*?', input).group()

    def get_date(self, year, md):
        match = re.search('(\d+).+?(\d+)', md)
        m = match.group(1)
        d = match.group(2)
        return get_annual_full_date(year, int(m), int(d)).strftime(pgsql_format)