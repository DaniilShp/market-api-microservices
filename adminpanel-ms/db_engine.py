import datetime
import motor.motor_asyncio

import settings


async def mongo_context(app):
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
    app['mongo_db'] = client.admin_database
    app['mongo_db'].orders.drop()
    yield
    client.close()


async def add_new_order(app, purchases: dict):
    order_id = int(await app['mongo_db'].orders.count_documents({}))
    await app['mongo_db'].orders.insert_one(
        {
            '_id': order_id,
            'purchases': purchases,
            'datetime': str(datetime.datetime.now())
        }
    )
