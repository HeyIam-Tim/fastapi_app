from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP


metadata = MetaData()


link = Table(
    'link',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('url', String, nullable=False),
    Column('created', TIMESTAMP, default=datetime.utcnow),
)


counter = Table(
    'counter',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('count', Integer),
    Column('created', TIMESTAMP, default=datetime.utcnow),
)
