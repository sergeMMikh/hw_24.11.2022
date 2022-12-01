from aiohttp import web
from models import AdvModel
from views import get_orm_item, check_auth, check_owner, get_user


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

        user_id = get_user(self.request)

        adv_data = dict(await self.request.json())
        adv_data.update({'user_id': user_id})

        new_adv = AdvModel(**adv_data)
        self.request['session'].add(new_adv)
        await self.request['session'].commit()

        return web.json_response({
            'id': new_adv.id
        })