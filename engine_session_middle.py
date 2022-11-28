from typing import Callable, Awaitable

from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import PG_DSN

Base = declarative_base()

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

