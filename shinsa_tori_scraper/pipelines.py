import csv
from db.database import init_db, SessionLocal
from app.models.shinsa import ShinsaModel
from app.models.dan import DanModel
from app.repositories.shinsa import ShinsaRepository
from app.repositories.dan import DanRepository
from app.services.shinsa import ShinsaService
from .items import ShinsaItem, DanItem
from .items import DojoItem

class ShinsaToriScraperPipeline:
    def __init__(self):
        init_db()
        self.db = SessionLocal()

        shinsa_repo = ShinsaRepository(self.db)
        dan_repo = DanRepository(self.db)
        self.shinsa_service = ShinsaService(shinsa_repo, dan_repo)

    def process_item(self, item, spider):
        if isinstance(item, ShinsaItem):
            self.shinsa_service.save_shinsa(ShinsaModel(
                id=item.get('id'),
                name=item.get('name'),
                location=item.get('location'),
                reg_start_at=item.get('reg_start_at'),
                reg_end_at=item.get('reg_end_at'),
                start_at=item.get('start_at'),
                end_at=item.get('end_at'),
            ))

        if isinstance(item, DanItem):
            shinsa = self.db.query(ShinsaModel).filter_by(
                location=item.get('shinsa_location'),
                start_at=item.get('shinsa_start_at')
            ).first()
            dan = self.db.query(DanModel).filter_by(
                name=item.get('name')
            ).first()
            print(f'shinsa: {shinsa}')

            if shinsa and dan:
                shinsa.dans.append(dan)
                self.db.commit()

        return item

    def close_spider(self, spider):
        self.db.close()


class KyudojoCsvPipeline:
    def open_spider(self, spider):
        self.file = open('kyudojo.csv', 'w', newline='', encoding='utf-8')
        self.fieldnames = [
            'name',
            'address',
            'phone',
            'province',
            'province_code',
            'latitude',
            'longitude'
        ]
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        if not isinstance(item, DojoItem):
            return None

        self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()
