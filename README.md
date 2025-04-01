# KYUDO TORI BACKEND

## Start API
```bash
uvicorn app.main:app --reload
```

## Start Virtual Environment
```bash
# root path
# open
source .venv/bin/activate

# close
deactivate
```

## Scrapy
Need to start venv first

```bash
# /root
cd shinsa_tori_scraper

scrapy genspider example_spider example.com

scrapy crawl example_spider
```
