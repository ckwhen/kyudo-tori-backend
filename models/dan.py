import uuid
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base
from .shinsa_dan import shinsa_dan

class Dan(Base):
    __tablename__ = "dans"
    shinsas = relationship("Shinsa", secondary=shinsa_dan, back_populates="dans")

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    level = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=func.current_timestamp())
    updated_at = Column(DateTime(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f"<Dan(name={self.name}, level={self.level})>"