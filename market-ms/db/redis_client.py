from redis import asyncio as aioredis


class RedisClient:
    def __init__(self, redis_url):
        self.cash_client = aioredis.from_url(redis_url, db=0)
        self.session_client = aioredis.from_url(redis_url, db=1)

    async def get_user_session(self, key: str):
        session = await self.session_client.json().get(key, "$")
        if session is None or session[0] is None or session == []:
            session = [dict()]
        await self.session_client.expire(key, 60*60*24)
        return session[0]

    async def save_user_session(self, key: str, session: dict):
        await self.session_client.json().set(key, "$", session)

    async def clear_session(self, key):
        await self.session_client.json().delete(key)


