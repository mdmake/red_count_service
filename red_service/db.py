from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, Float, create_engine
)
import os

meta = MetaData()

redtable = Table(
    'red_count_base', meta,
    Column('image_id', Integer, primary_key=True, autoincrement=True),
    Column('account_id', Integer, index=True),
    Column('tag', String),
    Column('red', Float, index=True)
)


def create_dict_from_select_result(prxobject):
    keys = ['image_id', 'account_id', 'tag', 'red']

    try:
        values = list(prxobject.next())
        data = dict(zip(keys, values))
        return data
    except:
        return None


# поменять на get_image_handler
def db_get_image_handler(engine, num):

    with engine.connect() as conn:
        expression = redtable.select(redtable).where(redtable.c.image_id == num)
        result = conn.execute(expression)

        data = create_dict_from_select_result(result)

        return data


def db_delete_image_handler(engine, num):

    with engine.connect() as conn:
        expression = redtable.delete(redtable).where(redtable.c.image_id == num)
        result = conn.execute(expression)

        return result.rowcount


def db_post_image_handler(engine, account_id, tag, red_pixel_percent):

    with engine.connect() as conn:
        expression = redtable.insert().returning(redtable.c.image_id)
        result = conn.execute(expression, [{'account_id': account_id, 'tag': tag, 'red': red_pixel_percent}])

        data_set = {"image_id": result.next()[0], "red": red_pixel_percent}

        return data_set


def db_get_image_count_handler(engine, account_id, tag, red__gt):

    with engine.connect() as conn:
        expression = redtable.select(redtable).where((redtable.c.account_id == account_id) & (redtable.c.tag == tag) & (redtable.c.red > red__gt))
        result = conn.execute(expression)

        return result.rowcount


async def init_db(app):
    url = os.environ.get('DATABASE_URL')
    engine = create_engine(url, echo=True)
    app['db'] = engine


# +---------------+
# | image_id      |
# +===============+
# | account_id    |
# +---------------+
# | tag           |
# +---------------+
# | red           |
# +---------------+
