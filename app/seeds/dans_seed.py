from db.database import SessionLocal
from app.models.dan import DanModel

def seed():
    session = SessionLocal()

    existing_dans = {dan.name for dan in session.query(DanModel).all()}
    print(existing_dans)
    dans = [
        { 'name': 'sho', 'level': 1 },
        { 'name': 'ni', 'level': 2 },
        { 'name': 'san', 'level': 3 },
        { 'name': 'yon', 'level': 4 },
        { 'name': 'go', 'level': 5 },
        { 'name': 'roku', 'level': 6 },
        { 'name': 'nana', 'level': 7 },
        { 'name': 'hachi', 'level': 8 },
    ]

    for dan in dans:
        if dan['name'] not in existing_dans:
            dan = DanModel(name=dan['name'], level=dan['level'])
            session.add(dan)

    session.commit()
