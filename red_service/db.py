from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, Float, create_engine
)
import os

meta = MetaData()

redtable = Table(
    'red_count_base', meta,
    Column('image_id', Integer, primary_key=True, autoincrement=True, index=True),
    Column('account_id', Integer, index=True),
    Column('tag', String),
    Column('red', Float, index=True)
)


def db_get_image_handler(engine, num):

    with engine.connect() as conn:
        expression = redtable.select(redtable).where(redtable.c.image_id == num)
        result = conn.execute(expression)
        return result




def create_url():

    url = os.environ.get('DATABASE_URL')
    print(url)

    return url

async def init_db(app):
    url = create_url()

    engine = create_engine(url, echo=True)
    app['db'] = engine


async def close_db(app):
    pass


# +---------------+
# | image_id            |
# +===============+
# | account_id       |
# +---------------+
# | tag     |
# +---------------+
# | red           |
# +---------------+
