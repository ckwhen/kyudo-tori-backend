from pydantic import BaseModel, UUID4, AwareDatetime, PositiveInt, Field
from typing import Optional, List, Any, Literal

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

class MetaDetail(BaseModel):
    field: str
    message: str

class Meta(BaseModel):
    message: str
    details: Optional[List[MetaDetail]] = []

class APIResponse(BaseModel):
    meta: Optional[Meta] = {}
    data: Any = []

class ShinsaFilterParams(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    search: Optional[str] = None
    limit: int = Field(20, gt=0, le=20)
    offset: int = Field(0, ge=0)
    sort_by: Literal["start_at", "end_at"] = "start_at"
    order: Literal["asc", "desc"] = "asc"

class DanSchema(BaseSchema):
    id: UUID4
    level: PositiveInt

class ShinsaSchema(BaseSchema):
    dans: List[DanSchema] = []

    id: UUID4
    name: str
    location: str
    reg_start_at: Optional[AwareDatetime]
    reg_end_at: Optional[AwareDatetime]
    start_at: AwareDatetime
    end_at: Optional[AwareDatetime]
