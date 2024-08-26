from aiohttp import web
from datetime import datetime

routes = web.RouteTableDef()


@routes.get('/get_name')
async def get_microservice_name(request):
    return web.json_response({'ms_name': 'adminpanel'})


@routes.get('/get_all_orders')
async def get_all_orders(request):
    db = request.app['mongo_db']
    results = db.orders.find({})
    if results is None:
        return web.HTTPNotFound()
    answer = [order for order in await results.to_list(length=100)]
    return web.json_response(answer)
