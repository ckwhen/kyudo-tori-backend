import scrapy
import pdfplumber
import re
import datetime
import pandas as pd
from io import BytesIO
from helpers.string_helper import convert_full_to_half
from helpers.date_helper import convert_reiwa_to_ce_year

class AichiSpider(scrapy.Spider):
    name = "aichi_spider"
    allowed_domains = ["www.aikyuren.com"]
    start_urls = ["http://www.aikyuren.com/shinsanittei.html"]

    def parse(self, response):
        pdf_url = response.xpath('//*[@id="main"]/p[1]/a/@href').get()

        if pdf_url:
            yield scrapy.Request(url='http://www.aikyuren.com/' + pdf_url, callback=self.parse_pdf)

    def parse_pdf(self, response):
        pdf_bytes = response.body
        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            page = pdf.pages[0]
            records = self.flatten_extract(page.extract_table())

            for record in records:
                name = record['name']

                if re.search('高校生講習会', name):
                    continue

                year = convert_reiwa_to_ce_year(int(record['year']))
                start_day = record['day']
                month = int(record['month'])
                end_day = None

                if re.search('\D+', start_day):
                    match = re.search('(\d+).+?(\d+)', start_day)
                    start_day = match.group(1)
                    e = int(match.group(2))
                    end_day = datetime.datetime(year, month, int(e))

                yield {
                    'name': name,
                    'location': record['location'],
                    'start_at': datetime.datetime(year, month, int(start_day)),
                    'end_at': end_day,
                }

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

