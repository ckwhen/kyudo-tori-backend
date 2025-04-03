from db.database import init_db, SessionLocal
from app.models.shinsa import ShinsaModel
from app.models.dan import DanModel
from app.models.helper import BaseModel
from app.repositories.shinsa import ShinsaRepository
from app.repositories.dan import DanRepository
from app.services.shinsa import ShinsaService
from .items import ShinsaItem, DanItem

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
            self.shinsa_service.save_shinsa_dans(
                item.get('name'),
                item.get('shinsa_location'),
                item.get('shinsa_start_at')
            )

        return item

    def close_spider(self, spider):
        self.db.close()
