import datetime
import json

from aiohttp import web
from sqlalchemy.future import select

from auth import hash_password, check_password
from config import TOKEN_TTL
from models import Base, User, Token, AdvModel
from engine_session_middle import engine, Session
from pprint import pprint


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
    print('Token is valid.')
    request['token'] = token


async def check_owner(request: web.Request, owner_id: int):
    if request['token'].user_id != owner_id:
        raise_error(web.HTTPForbidden, message='token is incorrect')


async def get_user(request: web.Request):
    return request['token'].user_id


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

