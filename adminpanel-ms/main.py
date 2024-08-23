from aiohttp import web
import nats
import settings
from nats.aio.msg import Msg


async def nats_context(app):
    app['nats'] = await nats.connect(settings.nats_url)
    await app['nats'].subscribe('confirmed_purchases', cb=on_message)
    yield
    await app['nats'].flush()
    await app['nats'].close()


async def on_message(data: dict):
    print(data)


async def handler(request):
    return web.Response(text="admin panel")


app = web.Application()
app.router.add_get('/get_name', handler)
app.cleanup_ctx.append(nats_context)


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8083)
