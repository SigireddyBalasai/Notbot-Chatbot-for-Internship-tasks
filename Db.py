import aiosqlite
import sqlalchemy as sa
import aiohttp_sqlalchemy as ahsa
from sqlalchemy import orm
class User(Base):
    phone_number = sa.Column(sa.String(20), primary_key=True)
    address = sa.Column(sa.Integer,nullable=False)
    block_number = sa.Column(sa.String(10),nullable=False)
    BrandName = sa.Column(sa.String(20), nullable=False)
    Color = sa.Column(sa.String(20), nullable=False)
    Vehicle_Number = sa.Column(sa.String(20), nullable=False)



