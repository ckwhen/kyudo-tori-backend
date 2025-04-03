from fastapi import Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated
from db.database import get_db
from app.services.shinsa import ShinsaService
from app.repositories.shinsa import ShinsaRepository
from app.repositories.dan import DanRepository
from ..schemas import APIResponse, ShinsaSchema, ShinsaFilterParams

class ShinsaController:
    @classmethod
    async def get_filtered_shinsas(
        cls,
        queries: Annotated[ShinsaFilterParams, Query()],
        db: Session = Depends(get_db),
    ) -> APIResponse:
        shinsa_repo = ShinsaRepository(db)
        dan_repo = DanRepository(db)
        service = ShinsaService(shinsa_repo, dan_repo)

        filters = {"name": queries.name, "location": queries.location}
        shinsas = service.get_filtered_shinsas(
            filters,
            queries.search,
            queries.offset, queries.limit,
            queries.sort_by, queries.order
        )

        return APIResponse(data=[ShinsaSchema.model_validate(shinsa) for shinsa in shinsas])
