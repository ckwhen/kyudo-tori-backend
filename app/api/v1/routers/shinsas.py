from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from app.repositories.shinsa import ShinsaRepository
from ..schemas import ShinsaSchema

router = APIRouter(prefix="/shinsas", tags=["Shinsas"])

@router.get("/")
async def get_all_shinsas(db: Session = Depends(get_db)) -> list[ShinsaSchema]:
    repo = ShinsaRepository(db)

    return repo.get_all()

