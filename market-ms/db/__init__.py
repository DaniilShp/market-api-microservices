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

        """product_data = {
                'product_id': 1,
                'name': 'Laptop',
                'type': 'Electronics',
                'price': 999,
                'amount_in_stock': 8,
                'image_url': 'http://example.com/laptop.jpg'
        }
        await conn.execute(products.insert().values(**product_data))
        product_data = {
                'product_id': 2,
                'name': 'Laptop2',
                'type': 'Electronics',
                'price': 888,
                'amount_in_stock': 6,
                'image_url': 'http://example.com/laptop2.jpg'
        }
        await conn.execute(products.insert().values(**product_data))"""
    return products, product_info
