from aiohttp import web

import routes
import settings
from nats_utils import nats_context
from db.db_engine import mysql_context
from db.redis_client import RedisClient


def init_app():
    app = web.Application()
    app['db_config'] = settings.get_db_config()
    app.cleanup_ctx.append(nats_context)
    app.cleanup_ctx.append(mysql_context)
    app['redis_client'] = RedisClient(settings.redis_url)
    app.add_routes(routes.routes)
    host, port = settings.listen.split(':')
    port = int(port)
    web.run_app(app, host=host, port=port, access_log_format='%a %t "%r" %s %Tfs.')


if __name__ == '__main__':
    init_app()
