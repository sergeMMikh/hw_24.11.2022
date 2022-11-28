import datetime
import json

from aiohttp import web
from sqlalchemy.future import select

from auth import hash_password, check_password
from config import TOKEN_TTL
from models import Base, User, Token
from engine_session_middle import engine, Session


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


class UserView(web.View):

    async def get(self, user_id: int):
        print('UserView.get')

        # with Session() as session:
        #     user = get_by_id(user_id, UserModel, session)
        #
        #     if user is None:
        #         raise HttpError(404, 'user not found')
        #
        #     return jsonify({
        #         'user': user.name,
        #         'email': user.email
        #     })

        return web.json_response({
            'class': 'UserView',
            'method': 'get'
        })

    async def post(self):
        # json_data = request.json
        # with Session() as session:
        #     try:
        #         new_user = UserModel(**validate(json_data, CreateUserSchema))
        #         session.add(new_user)
        #         session.commit()
        #     except IntegrityError:
        #         raise HttpError(409, 'User name already exists')
        #     return jsonify({'status': 'ok', 'id': new_user.id})
        return web.json_response({
            'class': 'UserView',
            'method': 'post'
        })

    async def patch(self, user_id: int):
        # data_to_patch = validate(request.json, PatchUserSchema)
        #
        # with Session() as session:
        #     user = get_by_id(user_id, UserModel, session)
        #
        #     for field, value in data_to_patch.items():
        #         setattr(user, field, value)
        #     session.commit()
        #     return jsonify({'status': 'success', 'id': user.id})
        return web.json_response({
            'class': 'UserView',
            'method': 'patch'
        })

    async def delete(self, user_id: int):
        # with Session() as session:
        #     user = get_by_id(user_id, UserModel, session)
        #     session.delete(user)
        #     session.commit()
        #     return jsonify({'status': 'success', 'id': user.id})
        return web.json_response({
            'class': 'UserView',
            'method': 'delete'
        })

    class AdvView(web.View):

        async def get(self, adv_id: int):
            # with Session() as session:
            #     adv = get_by_id(adv_id, AdvModel, session)
            #
            #     if adv is None:
            #         raise HttpError(404, 'user not found')
            #
            #     return jsonify({
            #         'Title': adv.title,
            #         'Description': adv.description
            #     })
            return web.json_response({
                'class': 'AdvView',
                'method': 'get'
            })

        async def post(self):
            # json_data = request.json
            # with Session() as session:
            #     try:
            #         new_adv = AdvModel(**validate(json_data, CreateAdvSchema))
            #         user_id = get_user_id(json_data, UserModel, session)
            #         setattr(new_adv, 'user_id', user_id)
            #         session.add(new_adv)
            #         session.commit()
            #     except IntegrityError:
            #         raise HttpError(409, 'This title already exists')
            #     return jsonify({'status': 'ok', 'id': new_adv.id})
            return web.json_response({
                'class': 'AdvView',
                'method': 'post'
            })

        async def patch(self, adv_id: int):
            # data_to_patch = validate(request.json, PatchAdvSchema)
            # json_data = request.json
            # with Session() as session:
            #     user_id = get_user_id(json_data, UserModel, session)
            #
            #     if user_id != adv_id:
            #         raise HttpError(403, "You don't have rights to delete this advertisement!")
            #
            # adv = get_by_id(adv_id, AdvModel, session)
            #
            # for field, value in data_to_patch.items():
            #     setattr(adv, field, value)
            # session.commit()
            # return jsonify({'status': 'success', 'id': adv.id})
            return web.json_response({
                'class': 'AdvView',
                'method': 'patch'
            })

        async def delete(self, adv_id: int):
            #         json_data = request.json
            #         with Session() as session:
            #             user_id = get_user_id(json_data, UserModel, session)
            #
            #             if user_id != adv_id:
            #                 raise HttpError(403, "You don't have rights to delete this advertisement!")
            #
            #             adv = get_by_id(adv_id, AdvModel, session)
            #             session.delete(adv)
            #             session.commit()
            #             return jsonify({'status': 'success', 'id': adv.id, 'user_id': user_id})
            return web.json_response({
                'class': 'AdvView',
                'method': 'delete'
            })
