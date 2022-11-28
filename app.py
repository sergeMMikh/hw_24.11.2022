from aiohttp import web

from engine_session_middle import session_middleware
from views import login, UsersView, app_context

app = web.Application(middlewares=[session_middleware, ])
app._cleanup_ctx.append(app_context)

app.add_routes([
    web.post("/login", login),
    web.post('/users/', UsersView),
    web.get('/users/{user_id:\d+}', UsersView),
    web.patch('/users/{user_id:\d+}', UsersView),
    web.delete('/users/{user_id:\d+}', UsersView),
])

