from .__init__ import init_db
from sqlalchemy.ext.asyncio import create_async_engine


def create_alchemy_engine(db_config: dict):
    DSN = "mysql+aiomysql://{user}:{password}@{host}/{database}".format(**db_config)
    engine = create_async_engine(url=DSN)
    return engine


async def mysql_context(app):
    app['alchemy_engine'] = create_alchemy_engine(app['db_config'])
    app['products_table'], app['product_info'] = await init_db(app['alchemy_engine'])
    yield
    await app['alchemy_engine'].dispose()
