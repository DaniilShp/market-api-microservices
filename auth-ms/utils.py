import re

from aiohttp import web
from aiohttp_session import get_session
from typing import Any, Awaitable, Callable, Optional

import settings
from users import check_password

_Handler = Callable[
    [web.Request, Optional[list], Optional[dict]],
    Awaitable[web.StreamResponse]
]


def login_required(handler_func: _Handler) -> _Handler | web.json_response:
    async def wrapped(
            request: web.Request, *args: Any, **kwargs: Any
    ) -> web.StreamResponse:
        for pattern in settings.not_protected_routes:
            if re.fullmatch(pattern, str(request.rel_url)):
                return await handler_func(request, *args, **kwargs)
        session = await get_session(request)
        if session.empty:
            return web.json_response({'msg': 'not authorized'})
        engine = request.config_dict['alchemy_engine']
        ok = await check_password(engine, session['user_data']['login'], session['user_data']['password'])
        if ok is None:
            raise web.HTTPFound('/log_out')
        return await handler_func(request, *args, **kwargs)

    return wrapped
