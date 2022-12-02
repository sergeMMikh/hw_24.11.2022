from pprint import pprint
from aiohttp import web
from auth import hash_password
from models import User
from views import get_orm_item, check_auth, check_owner


class UsersView(web.View):
    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        user = await get_orm_item(User, user_id, self.request['session'])
        return web.json_response({
            'id': user.id,
            'name': user.name,
            'email': user.email
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