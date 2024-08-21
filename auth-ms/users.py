import bcrypt
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, select

metadata = MetaData()
User = Table(
    'users', metadata,
    Column('login', String(30), primary_key=True, index=True),
    Column('password', String(100)),
    Column('privileges', Integer)
)


def create_alchemy_engine(db_config: dict):
    DSN = "mysql+aiomysql://{user}:{password}@{host}/{database}".format(**db_config)
    engine = create_async_engine(url=DSN)
    return engine


async def create_user_table(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


async def mysql_context(app):
    app['alchemy_engine'] = create_alchemy_engine(app['db_config'])
    await create_user_table(app['alchemy_engine'])
    yield
    await app['alchemy_engine'].dispose()


async def register_user(engine: AsyncEngine, new_user_data: dict):
    async with engine.begin() as conn:
        new_user_data['password'] = bcrypt.hashpw(new_user_data['password'].encode('utf-8'), bcrypt.gensalt())
        await conn.execute(User.insert().values(**new_user_data))


async def check_password(engine, login, password):
    async with engine.begin() as conn:
        result = await conn.execute(
            select(User.c.login, User.c.password, User.c.privileges).where(
                User.c.login == str(login)
            )
        )
        row = result.fetchone()
        if row:
            if bcrypt.checkpw(password.encode('utf-8'), row[1].encode('utf-8')):
                return int(row[2])


