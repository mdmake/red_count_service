from sqlalchemy import create_engine, MetaData
from red_service.db import redtable
import os

db_url = os.environ.get('DATABASE_URL')
#DSN = 'postgresql://patrick:@localhost:5432/server_test'
#DSN = url


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[redtable])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(redtable.insert(), [
        {'account_id': 99,
         'image_tag': 'Mona_Lisa',
         'red': 0.55}
    ])
    conn.close()


if __name__ == '__main__':
    db_url = os.environ.get('DATABASE_URL')
    engine = create_engine(db_url, echo=True)
    create_tables(engine)
    sample_data(engine)
