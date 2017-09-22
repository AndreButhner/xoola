from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
planejamento = Table('planejamento', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('titulo', String(length=100)),
    Column('descricao', String(length=255)),
    Column('categoria_id', Integer),
    Column('empresa_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['planejamento'].columns['empresa_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['planejamento'].columns['empresa_id'].drop()
