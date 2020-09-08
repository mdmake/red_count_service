from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Float, Date
)
import aiopg.sa

meta = MetaData()

redtable = Table(
    'red_count_base', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer),
    Column('image_tag', String),
    Column('red', Float)
)


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()



# +---------------+
# | id            |
# +===============+
# | user_id       |
# +---------------+
# | image_tag     |
# +---------------+
# | red           |
# +---------------+


