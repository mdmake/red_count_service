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


def db_delete_image_handler(engine, num):

    with engine.connect() as conn:
        expression = redtable.delete(redtable).where(redtable.c.image_id == num)
        result = conn.execute(expression)
        return result

# --> переделать в словарь
def db_post_image_handler(engine, account_id, tag, red_pixel_percent):

    with engine.connect() as conn:
        expression = redtable.insert().returning(redtable.c.image_id)
        result = conn.execute(expression, [{'account_id': account_id, 'tag': tag, 'red': red_pixel_percent}])
        return result

def db_get_image_count_handler(engine, account_id, tag, red__gt):

    with engine.connect() as conn:
        expression = redtable.select(redtable).where((redtable.c.account_id == account_id) & (redtable.c.tag == tag) & (redtable.c.red > red__gt))
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
