from aiohttp import web

import routes
import settings
from nats_utils import nats_context
from db_engine import mongo_context


def init_app():
    app = web.Application()
    app.cleanup_ctx.append(mongo_context)
    app.cleanup_ctx.append(nats_context)
    app.add_routes(routes.routes)
    host, port = settings.listen.split(':')
    port = int(port)
    web.run_app(app, host=host, port=port, access_log_format='%a %t "%r" %s %Tfs.')


if __name__ == '__main__':
    init_app()

