from sqlalchemy import cast, DateTime
from sqlalchemy.exc import SQLAlchemyError
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
            try:
                self.db.add(Shinsa(
                    id=item.get('id'),
                    name=item.get('name'),
                    location=item.get('location'),
                    reg_start_at=item.get('reg_start_at'),
                    reg_end_at=item.get('reg_end_at'),
                    start_at=item.get('start_at'),
                    end_at=item.get('end_at'),
                ))
                self.db.commit()
            except SQLAlchemyError as e:
                print(f"ShinsaItem: {e}")
                self.db.rollback()
            finally:
                self.db.close()

        if isinstance(item, DanItem):
            try:
                shinsa = (
                    self.db.query(Shinsa)
                    .filter(
                        Shinsa.location == item.get('shinsa_location'),
                        cast(Shinsa.start_at, DateTime).op('AT TIME ZONE')('UTC') == item.get('shinsa_start_at')
                    )
                    .first()
                )
                dan = self.db.query(Dan).filter(Dan.name == item.get('name')).first()

                if shinsa and dan:
                    shinsa.dans.append(dan)
                    self.db.commit()
            except SQLAlchemyError as e:
                print(f"DanItem: {e}")
                self.db.rollback()
            finally:
                self.db.close()

        return item

    def close_spider(self, spider):
        self.db.close()
