from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from ..models.dan import DanModel

class DanRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self):
        try:
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_by_name(self, dan_name):
        try:
          return (
                self.db.query(DanModel)
                .filter(DanModel.name == dan_name)
                .first()
          )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
