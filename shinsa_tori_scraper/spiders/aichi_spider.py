import scrapy
import pdfplumber
import re
import uuid
import pandas as pd
from io import BytesIO
from helpers.string_helper import convert_full_to_half
from helpers.date_helper import convert_reiwa_to_ce_year, get_tokyo_pgsql_date
from ..items import ShinsaItem, DanItem

AICHI_HOST = 'http://www.aikyuren.com'

class AichiSpider(scrapy.Spider):
    name = "aichi_spider"
    allowed_domains = ["www.aikyuren.com"]
    start_urls = [f"{AICHI_HOST}/shinsanittei.html"]

    def parse(self, response):
        pdf_url = response.xpath('//*[@id="main"]/p[1]/a/@href').get()

        if pdf_url:
            yield scrapy.Request(url=f"{AICHI_HOST}/{pdf_url}", callback=self.parse_pdf)

    def parse_pdf(self, response):
        pdf_bytes = response.body
        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            page = pdf.pages[0]
            records = self.flatten_extract(page.extract_table())

            for record in records:
                shinsa_item = ShinsaItem()
                dan_item = DanItem()
                id = str(uuid.uuid4())
                name = record['name']
                loc = record['location']
                dan_dict = {
                    "sho": record['sho'],
                    "ni": record['ni'],
                    "san": record['san'],
                    "yon": record['yon'],
                    "go": record['go'],
                }

                if re.search('高校生講習会', name):
                    continue

                year = convert_reiwa_to_ce_year(int(record['year']))
                month = int(record['month'])
                s_day = record['day']
                end_at = None

                if re.search('\D+', s_day):
                    match = re.search('(\d+).+?(\d+)', s_day)
                    s_day = match.group(1)
                    e = int(match.group(2))
                    end_at = get_tokyo_pgsql_date(year, month, int(e))

                start_at = get_tokyo_pgsql_date(year, month, int(s_day))

                for k, v in dan_dict.items():
                    if v == '':
                        continue
                    dan_item['shinsa_location'] = loc
                    dan_item['shinsa_start_at'] = start_at
                    dan_item['name'] = k
                    yield dan_item

                shinsa_item['id'] = id
                shinsa_item['name'] = name
                shinsa_item['location'] = loc
                shinsa_item['start_at'] = start_at
                shinsa_item['end_at'] = end_at
                yield shinsa_item

    def flatten_extract(self, t):
        t.pop()

        df = pd.DataFrame(t[1:], columns=t[0])
        df.rename(columns={
            "№": "no",
            "審査区分": "type",
            "年": "year",
            "月": "month",
            "日": "day",
            "審 査 名": "name",
            "会 場 名": "location",
            "無指定": "none_kyo",
            "級": "kyo",
            "初": "sho",
            "弐": "ni",
            "参": "san",
            "四": "yon",
            "五": "go",
            "備 考": "remark",
        }, inplace=True)
        for column in ["no", "year", "month", "day", "year"]:
            df[column] = df[column].apply(convert_full_to_half)

        return df.to_dict(orient='records')

