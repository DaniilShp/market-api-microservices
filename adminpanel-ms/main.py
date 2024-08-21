from aiohttp import web


async def handler(request):
    return web.Response(text="admin panel")


app = web.Application()
app.router.add_get('/get_name', handler)


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8083)
