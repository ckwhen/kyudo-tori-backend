from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .helper import Base

shinsa_dan = Table(
    'shinsas_dans',
    Base.metadata,
    Column('shinsa_id', UUID(as_uuid=True), ForeignKey('shinsas.id'), primary_key=True),
    Column('dan_id', UUID(as_uuid=True), ForeignKey('dans.id'), primary_key=True)
)