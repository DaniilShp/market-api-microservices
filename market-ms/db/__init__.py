from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey


async def init_db(engine):
    metadata = MetaData()

    products = Table(
        'products', metadata,
        Column('product_id', Integer, primary_key=True),
        Column('name', String(30)),
        Column('type', String(30)),
        Column('price', Integer),
        Column('amount_in_stock', Integer),
        Column('image_url', String(30))
    )

    product_info = Table(
        'product_info', metadata,
        Column('product_id', Integer, ForeignKey('products.product_id'), unique=True),
        Column('description', String(512))
    )

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    return products, product_info
