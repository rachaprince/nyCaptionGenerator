from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine('sqlite:///database.db')

metadata = MetaData()

user = Table('contest', metadata,
    Column('id', Integer, primary_key=True),
    Column('image', String(120)),
    Column('men', String(5)),
    Column('women', String(5)),
    Column('animals', String(120)),
    Column('glasses', String(120)),
    Column('other', String(120)),
    Column('scenery', String(120)),
    Column('incongruity', String(120)),
    Column('description_0', String(120)),
    Column('description_1', String(120)),
    Column('description_2', String(120)),
    Column('implied', String(120)),
    Column('keyword_0', String(120)),
    Column('keyword_1', String(120)),
)

metadata.create_all(engine)
