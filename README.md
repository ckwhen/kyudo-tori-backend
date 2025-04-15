# KYUDO TORI BACKEND

> 一個協助弓道學習者查詢日本各地審查資訊的工具  
> 整合爬蟲、API、資料庫與前端呈現的專案

---

## 專案相關連結

- [kyudo-tori-frontend](https://github.com/ckwhen/kyudo-tori-frontend)：查詢與瀏覽審查資訊的前端模組（開發中）

---

## 專案介紹

**Kyudo Tori** 是為弓道學習者打造的資訊整合平台，目標是解決日本各地審查公告分散、不易查詢的困擾。

- 將各地方弓道連盟所公告的 HTML 或 PDF 形式的審查資訊自動擷取、轉換為結構化資料
- 將資料整理儲存於資料庫，並透過 API 提供給前端使用
- 前端介面開發中，將提供簡單易用的查詢體驗

---

## 功能一覽

- 自動爬取審查公告（支援HTML / PDF）
- 提供 RESTful API 提供給前端使用

---

## 技術架構

| 部分 | 技術 |
|------|------|
| 後端 | FastAPI / PostgreSQL / SQLAlchemy |
| 爬蟲 | Scrapy / pdfplumber / htmlparser |
| 部署 | Docker / docker-compose（開發中） |

## Start DB
```bash
source ./start.sh
```

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

## 備註
- 專案仍在開發階段，資料格式、API 結構可能會有變動
