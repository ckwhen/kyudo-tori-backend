import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .helper import BaseModel
from .shinsa_dan import shinsa_dan

class DanModel(BaseModel):
    __tablename__ = "dans"
    shinsas = relationship("ShinsaModel", secondary=shinsa_dan, back_populates="dans")

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    level = Column(Integer)

    def __repr__(self):
        return f"<DanModel(name={self.name}, level={self.level})>"