import asyncio
from typing import Any

from sqlalchemy import String, text, create_engine
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine, async_sessionmaker
# from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker, Mapped, mapped_column
from bot.configuration import bot_configuration as bot_config
from database.models import Base, UserRequest, Ban


engine = create_async_engine(
    url=bot_config.db_uri_asyncpg,
    echo=True if bot_config.logging_level == 'DEBUG' else False,
    pool_size=20,
    max_overflow=40,
)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_pg_version() -> str:
    async with session_maker.begin() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        pg_version = res.fetchone()[0]
        return pg_version


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def main():
    print(await get_pg_version())
    # await drop_tables()
    # await create_tables()


if __name__ == '__main__':
    asyncio.run(main())
