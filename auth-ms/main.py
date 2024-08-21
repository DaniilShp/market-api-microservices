import base64
import fernet
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import routes
import settings
from users import mysql_context


def init_app():
    app = web.Application()
    app['db_config'] = settings.get_db_config()
    app.cleanup_ctx.append(mysql_context)
    app.add_routes(routes.auth_routes)
    app.add_routes(routes.redirect_routes)
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    host, port = settings.listen.split(':')
    port = int(port)
    web.run_app(app, host=host, port=port, access_log_format='%a %t "%r" %s %Tfs.')


if __name__ == '__main__':
    init_app()
