import json
from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/get_name')
async def get_microservice_name(request):
    return web.json_response({'ms_name': 'market'})


@routes.get('/get_all_products')
async def get_all_products(request):
    engine = request.app['alchemy_engine']
    products_table = request.app['products_table']
    async with engine.begin() as conn:
        res = await conn.execute(products_table.select())
        result = res.fetchall()
        answer = [{
            key: value for key, value in zip(res.keys(), result[i])
        } for i in range(len(result))]
    return web.json_response(answer)


@routes.post('/add_to_cart')
async def add_to_cart(request: web.Request):
    user_uid = request.headers.get('user_uid', None)
    purchase = await request.json()  # {'product_id': int, 'amount': int}
    product_id = purchase['product_id']
    amount = purchase['amount']
    session = await request.app['redis_client'].get_user_session(key=user_uid)
    session[product_id] = amount
    await request.app['redis_client'].save_user_session(user_uid, session)
    return web.json_response(session)


@routes.delete('/clear_cart')
async def clear_cart(request: web.Request):
    redis_client = request.app['redis_client']
    user_uid = request.headers.get('user_uid', None)
    await redis_client.clear_session(key=user_uid)
    return web.Response(status=204)


@routes.post('/confirm_purchases')
async def confirm_purchase(request: web.Request):
    import nats
    redis_client = request.app['redis_client']
    nats_client: nats.NATS = request.app['nats']
    user_uid = request.headers.get('user_uid', None)
    session = await redis_client.get_user_session(key=user_uid)
    payload = json.dumps(session).encode()
    await redis_client.clear_session(key=user_uid)
    await nats_client.publish('confirmed_purchases', payload)
    await nats_client.flush()
    return web.json_response(session)
