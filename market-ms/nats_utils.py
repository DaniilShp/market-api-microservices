import nats
import settings


async def nats_context(app):
    app['nats'] = await nats.connect(settings.nats_url)
    yield
    await app['nats'].flush()
    await app['nats'].close()
