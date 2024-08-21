from aiohttp import web, ClientSession
from aiohttp_session import get_session

import settings
from users import register_user, check_password

auth_routes = web.RouteTableDef()


@auth_routes.get('/get_name')
async def get_microservice_name(request):
    return web.json_response({'ms_name': 'auth'})


@auth_routes.post('/register')
async def register(request: web.Request):
    engine = request.config_dict['alchemy_engine']
    user_data = await request.json()
    await register_user(engine, user_data)
    return web.json_response({'message': 'registered'})


@auth_routes.post('/login')
async def login(request: web.Request):
    engine = request.config_dict['alchemy_engine']
    session = await get_session(request)
    user_data = await request.json()
    l, p = user_data['login'], user_data['password']
    privileges = await check_password(engine, l, p)
    if privileges is None:
        return web.json_response({"message": "incorrect login or password"})
    payload = {'login': l, 'password': p, 'privileges': privileges}
    session['user_data'] = payload
    return web.json_response({'message': 'success'})


@auth_routes.get('/check_user')
async def check_user(request: web.Request):
    session = await get_session(request)
    if session.empty:
        return web.json_response({'msg': 'not authorized'})
    engine = request.config_dict['alchemy_engine']
    ok = await check_password(engine, session['user_data']['login'], session['user_data']['password'])
    if ok is None:
        session.clear()
        return web.json_response({'msq': 'bad cookie_session'})
    return web.json_response({'msg': 'ok'})


@auth_routes.get('/logout')
async def logout(request: web.Request):
    session = await get_session(request)
    session.clear()
    return web.json_response({'message': 'logout'})


redirect_routes = web.RouteTableDef()


async def redirect_request(method, url):
    print(method, url)
    async with ClientSession() as session:
        async with session.request(method, url) as response:
            data = await response.text()
            status = response.status
            headers = response.headers
            return data, status, headers


@redirect_routes.route('*', '/market/{tail:.*}')
async def market_routes(request: web.Request):
    method = request.method
    ms_base_path = settings.market_url
    rel_path = request.match_info.get('tail', '')
    data, status, headers = await redirect_request(method, ms_base_path+rel_path)
    return web.Response(text=data, status=status, headers=headers)


@redirect_routes.route('*', '/adminpanel/{tail:.*}')
async def adminpanel_routes(request: web.Request):
    method = request.method
    ms_base_path = settings.adminpanel_url
    rel_path = request.match_info.get('tail', '')
    return web.json_response({'method': method, 'url': ms_base_path+rel_path})
    return await redirect_request(method, ms_base_path+rel_path)
