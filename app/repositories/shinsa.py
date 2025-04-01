from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session
from models.shinsa import Shinsa

class ShinsaRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        """ 取得審查 """
        return self.db.query(Shinsa).all()