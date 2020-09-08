from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, Float

engine = create_engine('postgresql://patrick:@localhost:5432/server_test', echo=True)
meta = MetaData()
conn = 0

redtable = Table(
    'red_count_base', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer),
    Column('image_tag', String),
    Column('red', Float)
)


def init_db():
    meta = MetaData()
    meta.create_all(bind=engine, tables=[redtable])
    global conn
    conn = engine.connect()
    pass

def close_db():
    global conn
    conn.close()
    pass



# engine = create_engine('postgresql://patrick:@localhost:5432/server_test', echo=True)
#Base = declarative_base()
# meta = MetaData()

# class RedTable(Base):
#
#     __tablename__ = 'red_count_base'
#     # image_id
#     id = Column(Integer, primary_key=True,  autoincrement=True)
#     user_id = Column(Integer)
#     image_tag = Column(String)
#     red = Column(Float)
#
#     def __repr__(self):
#         return (self.id, self.user_id, self.image_tag, self.red)


# +---------------+
# | id            |
# +===============+
# | user_id       |
# +---------------+
# | image_tag     |
# +---------------+
# | red           |
# +---------------+


