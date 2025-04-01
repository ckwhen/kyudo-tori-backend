from pydantic import BaseModel, UUID4, AwareDatetime, PositiveInt
from typing import Optional

class DanSchema(BaseModel):
    id: UUID4
    level: PositiveInt

class ShinsaSchema(BaseModel):
    dans: list[DanSchema] = []

    id: UUID4
    name: str
    location: str
    reg_start_at: Optional[AwareDatetime]
    reg_end_at: Optional[AwareDatetime]
    start_at: AwareDatetime
    end_at: Optional[AwareDatetime]

    class Config:
        from_attributes = True