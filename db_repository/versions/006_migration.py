from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('extrato_id', INTEGER),
    Column('descricao', VARCHAR(length=100)),
    Column('empresa_id', INTEGER),
    Column('efetuado', BOOLEAN),
)

upload = Table('upload', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('extrato_id', Integer),
    Column('descricao', String(length=100)),
    Column('efetuado', Boolean),
    Column('empresa_id', Integer),
)

planejamento = Table('planejamento', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('titulo', String(length=100)),
    Column('valor', Float),
    Column('descricao', String(length=255)),
    Column('categoria_id', Integer),
    Column('empresa_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['upload'].create()
    post_meta.tables['planejamento'].columns['valor'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['upload'].drop()
    post_meta.tables['planejamento'].columns['valor'].drop()
