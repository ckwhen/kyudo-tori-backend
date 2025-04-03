from sqlalchemy import Column, DateTime, orm
from sqlalchemy import cast
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import Dict, Any, Optional

@orm.as_declarative()
class Base:
    id: Any
 
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

class QueryBuilder:
    def __init__(self, model, db: Session):
        self.model = model
        self.db = db
        self.query = db.query(model)

    def filter(self, filters: Dict[str, Any]):
        """根據傳入的參數動態加入過濾條件"""
        for field, value in filters.items():
            if hasattr(self.model, field) and value is not None:
                self.query = self.query.filter(getattr(self.model, field) == value)
        return self

    def search(self, search_fields: list[str], keyword: Optional[str]):
        """根據 `keyword` 在多個欄位做模糊查詢"""
        if keyword:
            conditions = [getattr(self.model, field).ilike(f"%{keyword}%") for field in search_fields]
            self.query = self.query.filter(or_(*conditions))
        return self

    def sort(self, sort_by: str, order: str = "asc"):
        """根據指定欄位排序"""
        if hasattr(self.model, sort_by):
            order_by = getattr(self.model, sort_by)
            if order == "desc":
                order_by = desc(order_by)
            self.query = self.query.order_by(order_by)
        return self

    def paginate(self, offset: int = 0, limit: int = 20):
        """處理分頁"""
        self.query = self.query.offset(offset).limit(limit)
        return self

    def execute(self):
        """執行查詢"""
        return self.query.all()
