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
        """product_data = {
            'product_id': 2,  # Уникальный идентификатор продукта
            'name': 'Laptop2',  # Название продукта
            'type': 'Electronics',  # Тип продукта
            'price': 888,  # Цена продукта
            'amount_in_stock': 6,  # Количество на складе
            'image_url': 'http://example.com/laptop2.jpg'  # URL изображения продукта
        }
        await conn.execute(products_table.insert().values(**product_data))"""
        res = await conn.execute(products_table.select())
        result = res.fetchall()
        answer = [{
            key: value for key, value in zip(res.keys(), result[i])
        } for i in range(len(result))]
    return web.json_response(answer)
