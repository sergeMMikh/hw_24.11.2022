import datetime
import json

from aiohttp import web
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.future import select
from typing import Callable, Awaitable

from config import PG_DSN, TOKEN_TTL
from models import Base, User, Token
from auth import hash_password, check_password

from pprint import pprint

engine = create_async_engine(PG_DSN)

Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


@web.middleware
async def session_middleware(request: web.Request,
                             handler: Callable[[web.Request],
                                               Awaitable[web.Response]]):
    async with Session() as session:
        request['session'] = session
        response = await handler(request)

        return response


async def app_context(app: web.Application):
    async with engine.begin() as conn:
        async with Session() as session:
            await session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            await session.commit()
        await conn.run_sync(Base.metadata.create_all)
    print('START')
    yield
    await engine.dispose()
    print("FINISH")


async def check_auth(request: web.Request):
    token_id = request.headers.get('token')

    if not token_id:
        raise_error(web.HTTPForbidden, message='token is incorrect')

    try:
        token = await get_orm_item(Token, token_id, request['session'])

    except web.HTTPNotFound:
        raise_error(web.HTTPForbidden, message='token is incorrect')
    if token.created + datetime.timedelta(seconds=TOKEN_TTL) <= datetime.datetime.now():
        raise_error(web.HTTPForbidden, message='token is incorrect')
    request['token'] = token


async def check_owner(request: web.Request, owner_id: int):
    if request['token'].user_id != owner_id:
        raise_error(web.HTTPForbidden, message='token is incorrect')


def raise_error(exception_class, message):
    raise exception_class(
        text=json.dumps({'status': 'error',
                         'message': message}),
        content_type='application/json'
    )


async def get_orm_item(orm_class, object_id, session):
    item = await session.get(orm_class, object_id)
    if item is None:
        raise raise_error(web.HTTPNotFound,
                          f'{orm_class.__name__} not found')
    return item


async def login(request: web.Request):
    user_data = await request.json()
    query = select(User).where(User.name == user_data["name"])
    result = await request["session"].execute(query)
    user = result.scalar()
    if not user or not check_password(user_data["password"], user.password):
        raise raise_error(web.HTTPUnauthorized,
                          message='user or password is incorrect')

    token = Token(user=user)
    request["session"].add(token)
    await request["session"].commit()

    return web.json_response({"token": str(token.id)})


class UsersView(web.View):
    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        user = await get_orm_item(User, user_id, self.request['session'])
        return web.json_response({
            'id': user.id,
            'name': user.name
        })

    async def post(self):
        user_data = await self.request.json()
        user_data['password'] = hash_password(user_data['password'])
        new_user = User(**user_data)
        self.request['session'].add(new_user)
        await self.request['session'].commit()
        return web.json_response({
            'id': new_user.id
        })

    async def patch(self):
        user_id = int(self.request.match_info['user_id'])
        user = await get_orm_item(User, user_id, self.request['session'])
        user_data = await self.request.json()

        if 'password' in user_data:
            user_data['password'] = hash_password(user_data['password'])

        for field, value in user_data.items():
            setattr(user, field, value)

        self.request['session'].add(user)
        await self.request['session'].commit()

        return web.json_response({"status": "success"})

    async def delete(self):
        await check_auth(self.request)
        user_id = int(self.request.match_info['user_id'])
        await check_owner(self.request, user_id)
        user = await get_orm_item(User, user_id, self.request['session'])
        await self.request['session'].delete(user)
        await self.request['session'].commit()
        return web.json_response({"status": "success"})


app = web.Application(middlewares=[session_middleware, ])
app._cleanup_ctx.append(app_context)

app.add_routes([
    web.post("/login", login),
    web.post('/users/', UsersView),
    web.get('/users/{user_id:\d+}', UsersView),
    web.patch('/users/{user_id:\d+}', UsersView),
    web.delete('/users/{user_id:\d+}', UsersView),
])

if __name__ == '__main__':
    web.run_app(app, port=8080)
