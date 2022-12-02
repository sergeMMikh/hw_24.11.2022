from aiohttp import web
from models import AdvModel
from views import get_orm_item, check_auth, check_owner, get_user, raise_error
from sqlalchemy.future import select


class AdvView(web.View):

    async def get(self):
        adv_id = int(self.request.match_info['adv_id'])

        adv = await get_orm_item(AdvModel, adv_id, self.request['session'])

        return web.json_response({
            'Title': adv.title,
            'Description': adv.description
        })

    async def post(self):
        await check_auth(self.request)

        user_id = await get_user(self.request)
        adv_data = dict(await self.request.json())
        adv_data.update({'user_id': user_id})
        new_adv = AdvModel(**adv_data)
        self.request['session'].add(new_adv)
        await self.request['session'].commit()

        return web.json_response({
            'id': new_adv.id
        })

    async def patch(self):

        await check_auth(self.request)

        adv_data = await self.request.json()

        query = select(AdvModel).where(AdvModel.title == adv_data["title"])
        result = await self.request["session"].execute(query)
        adv = result.scalar()

        if not adv:
            raise raise_error(web.HTTPUnauthorized,
                              message="The title is incorrect.")

        await check_owner(self.request, adv.user_id)

        for field, value in adv_data.items():
            setattr(adv, field, value)

        self.request['session'].add(adv)
        await self.request['session'].commit()

        return web.json_response({"status": "success"})

    async def delete(self):
        await check_auth(self.request)

        adv_id = int(self.request.match_info['adv_id'])
        adv = await get_orm_item(AdvModel, adv_id, self.request['session'])

        await check_owner(self.request, adv.user_id)
        await self.request['session'].delete(adv)
        await self.request['session'].commit()

        return web.json_response({"status": "success"})
