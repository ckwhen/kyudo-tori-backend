import csv
from pathlib import Path
from sqlalchemy.orm import Session
from db.database import SessionLocal
from app.models.dan import DanModel

def seed_dans(session: Session):
    with open(
        Path(__file__).parent / "datas" / "dans.csv",
        newline='',
        encoding='utf-8-sig'
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dan = DanModel(
                name=row['name'],
                level=int(row['level'])
            )
            session.add(dan)
    session.commit()

def seed_all():
    session = SessionLocal()

    seed_dans(session)
    print("All seed data has been inserted!")

if __name__ == '__main__':
    seed_all()
