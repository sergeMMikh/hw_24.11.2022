import json

from aiohttp import web
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.future import select
from typing import Callable, Awaitable

from config import PG_DSN
from models import Base, UserModel, AdvModel
from views import UserView

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
            # await session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            await session.commit()
            print('session.commit()')
        await conn.run_sync(Base.metadata.create_all)
    print('START')
    yield
    await engine.dispose()
    print("FINISH")


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

class TestView(web.View):

    async def get(self):

        print('UserView.get')

        return web.json_response({
            'class': 'TestView',
            'method': 'get'
        })

app = web.Application(middlewares=[session_middleware, ])
app._cleanup_ctx.append(app_context)

app.add_routes([
    # web.get('/user/<int:user_id>', UserView),
    web.get('/users/{user_id:\d+}', TestView),
])

# app.add_url_rule('/user/<int:user_id>', view_func=UserView.as_view('users_get'), methods=['GET', 'PATCH', 'DELETE'])
# app.add_url_rule('/user/', view_func=UserView.as_view('users'), methods=['POST'])
# app.add_url_rule('/adv/<int:adv_id>', view_func=AdvView.as_view('adv_get'), methods=['GET', 'DELETE'])
# app.add_url_rule('/adv/', view_func=AdvView.as_view('adv'), methods=['POST'])
