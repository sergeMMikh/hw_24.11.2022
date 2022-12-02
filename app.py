from aiohttp import web

from adv_views import AdvView
from engine_session_middle import session_middleware
from users_views import UsersView
from views import login, app_context

app = web.Application(middlewares=[session_middleware, ])
app._cleanup_ctx.append(app_context)

app.add_routes([
    web.post("/login", login),
    web.post('/users/', UsersView),
    web.get('/users/{user_id:\d+}', UsersView),
    web.patch('/users/{user_id:\d+}', UsersView),
    web.delete('/users/{user_id:\d+}', UsersView),

    web.post('/adv', AdvView),
    web.get('/adv/{adv_id:\d+}', AdvView),
    web.patch('/adv', AdvView),
    web.delete('/adv/{adv_id:\d+}', AdvView),
])
