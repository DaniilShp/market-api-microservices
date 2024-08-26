import nats
import json
import settings
from db_engine import add_new_order


async def create_on_message(app):
    async def on_message(msg):
        await add_new_order(app, json.loads(msg.data))
    return on_message


async def nats_context(app):
    app['nats'] = await nats.connect(settings.nats_url)
    await app['nats'].subscribe('confirmed_purchases', cb=await create_on_message(app))
    yield
    await app['nats'].flush()
    await app['nats'].close()
