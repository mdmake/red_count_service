from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Float, Date
)

from sqlalchemy import create_engine, MetaData
import aiopg.sa

meta = MetaData()

redtable = Table(
    'red_count_base', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer),
    Column('image_tag', String),
    Column('red', Float)
)

redtable.select()

async def init_pg(app):
    conf = app['config']['postgres']
    engine = create_engine('postgresql://patrick:@localhost:5432/server_test', echo=True)
    app['db'] = engine


async def close_pg(app):
    #app['db'].close()
    #await app['db'].wait_closed()
    pass



# +---------------+
# | id            |
# +===============+
# | user_id       |
# +---------------+
# | image_tag     |
# +---------------+
# | red           |
# +---------------+


