from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, Float, create_engine
)

meta = MetaData()

redtable = Table(
    'red_count_base', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer),
    Column('image_tag', String),
    Column('red', Float)
)


def create_url(cn):
    url = ''
    for k, v in cn.items():
        if not cn[k]:
            cn[k]=''
    url = 'postgresql://{}:{}@{}:{}/{}'.format(cn['user'], \
            cn['password'], cn['host'], cn['port'], cn['database'])

    return url

async def init_db(app):
    conf = app['config']['postgres']
    url = create_url(conf)

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
