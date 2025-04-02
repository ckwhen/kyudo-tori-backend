from sqlalchemy import Column, DateTime
from sqlalchemy import cast
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import func

Base = declarative_base()
 
class BaseModel(Base):
    __abstract__ = True

    @declared_attr
    def created_at(cls):
        return Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now()
        )

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now()
        )
    
    @staticmethod
    def utc_cast(column):
        """將 timestamp 欄位轉換為 UTC"""
        return cast(column, DateTime).op("AT TIME ZONE")("UTC")
