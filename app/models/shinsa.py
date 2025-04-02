import uuid
from sqlalchemy import Column, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .helper import BaseModel
from .shinsa_dan import shinsa_dan

class ShinsaModel(BaseModel):
    __tablename__ = "shinsas"
    __table_args__ = (UniqueConstraint('location', 'start_at', name='u_shinsa_locationdate'),)

    dans = relationship('DanModel', secondary=shinsa_dan, back_populates='shinsas')

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True)
    location = Column(String)
    reg_start_at = Column(DateTime(timezone=True), nullable=True)
    reg_end_at = Column(DateTime(timezone=True), nullable=True)
    start_at = Column(DateTime(timezone=True))
    end_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<ShinsaModel(name={self.name}, start_at={self.start_at}, location={self.location})>"