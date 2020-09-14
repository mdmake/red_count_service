from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, Float, create_engine
)
import os

meta = MetaData()

redtable = Table(
    'red_count_base', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, index=True),
    Column('image_tag', String),
    Column('red', Float, mssql_clustered=True)
)


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
# | id            |
# +===============+
# | user_id       |
# +---------------+
# | image_tag     |
# +---------------+
# | red           |
# +---------------+
