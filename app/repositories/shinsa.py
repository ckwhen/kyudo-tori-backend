from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from ..models.helper import BaseModel
from ..models.shinsa import ShinsaModel
from ..models.dan import DanModel

class ShinsaRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, shinsa: ShinsaModel):
        try:
            self.db.add(ShinsaModel(
                id=shinsa.id,
                name=shinsa.name,
                location=shinsa.location,
                reg_start_at=shinsa.reg_start_at,
                reg_end_at=shinsa.reg_end_at,
                start_at=shinsa.start_at,
                end_at=shinsa.end_at,
            ))
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_by_unique(self, shinsa_location, shinsa_start_at):
        try:
            q = self.db.query(ShinsaModel)
            record = (
                q.filter(
                    ShinsaModel.location == shinsa_location,
                    BaseModel.utc_cast(ShinsaModel.start_at) == shinsa_start_at
                )
                .first()
            )
            return record
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_all(self):
        try:
            return self.db.query(ShinsaModel).all()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
