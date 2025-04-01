from db.database import init_db, SessionLocal
from models.shinsa import Shinsa
from models.dan import Dan
from .items import ShinsaItem, DanItem

class ShinsaToriScraperPipeline:
    def __init__(self):
        init_db()
        self.db = SessionLocal()

    def process_item(self, item, spider):
        if isinstance(item, ShinsaItem):
            self.db.add(Shinsa(
                id=item['id'],
                name=item['name'],
                location=item['location'],
                reg_end_at=item['reg_end_at'],
                start_at=item['start_at'],
            ))
            self.db.commit()

        if isinstance(item, DanItem):
            shinsa = (
                self.db.query(Shinsa)
                .filter_by(location=item['shinsa_location'], start_at=item['shinsa_start_at'])
                .first()
            )
            dan = self.db.query(Dan).filter_by(name=item['name']).first()

            if shinsa and dan:
                shinsa.dans.append(dan)
                self.db.commit()

        return item

    def close_spider(self, spider):
        self.db.close()
