from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Upl_Docs = Table('Upl_Docs', post_meta,
    Column('upload_id', Integer, primary_key=True, nullable=False),
    Column('docs_id', Integer, primary_key=True, nullable=False),
)

upload = Table('upload', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('extrato_id', Integer),
    Column('descricao', String(length=100)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Upl_Docs'].create()
    post_meta.tables['upload'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Upl_Docs'].drop()
    post_meta.tables['upload'].drop()
