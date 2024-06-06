import asyncio
import enum

from datetime import datetime, timedelta

from sqlalchemy.sql.functions import count

from database.models import UserRequest, Ban
from database.engine import session_maker
from sqlalchemy import select, update, insert, delete, and_, or_, not_, any_, desc


async def get_banned_users_by_time(last_time: timedelta = timedelta(hours=2)) -> list:
    async with session_maker() as session:
        results = await session.scalars(select(Ban).where(or_(Ban.banned_at >= datetime.now() - last_time,
                                                              Ban.banned_to == None)))
        return results.all()


async def get_banned_users(number_of_users: int = 10) -> list:
    async with session_maker() as session:
        results = await session.execute(select(Ban.telegram_id, Ban.banned_at).
                                        order_by(desc(Ban.banned_at)).
                                        limit(number_of_users))
        return results.fetchall()


async def is_user_banned(tg_id: int) -> bool:
    async with session_maker() as session:
        result = await session.execute(select(Ban.telegram_id).
                                       where(and_(Ban.telegram_id == tg_id,
                                                  or_(Ban.banned_to > datetime.now(), Ban.banned_to == None))))
        return bool(len(result.scalars().all()))


async def ban_tg_user(tg_id: int, ban_time: datetime | None) -> None:
    async with session_maker() as session:
        await session.execute(insert(Ban).values(telegram_id=tg_id,
                                                 banned_at=datetime.now(),
                                                 banned_to=ban_time if ban_time else None))
        await session.commit()


async def unban_tg_user(tg_id: int) -> None:
    async with session_maker() as session:
        await session.execute(delete(Ban).where(tg_id == Ban.telegram_id))
        await session.commit()


async def unban_all() -> None:
    async with session_maker() as session:
        await session.execute(delete(Ban))
        await session.commit()


async def save_user_request(tg_id: int | str, tg_username: str, search_type: enum.Enum, search_str: str,
                            report_url: str) -> None:
    async with session_maker() as session:
        await session.execute(insert(UserRequest).values(telegram_id=int(tg_id),
                                                         tg_username=tg_username,
                                                         search_type=search_type,
                                                         search_str=str(search_str),
                                                         search_time=datetime.now(),
                                                         report_url=str(report_url)))
        await session.commit()


async def get_spam_users(number_of_users: int = 10) -> list:
    async with session_maker() as session:
        results = await session.execute(select(UserRequest.telegram_id, count(UserRequest.telegram_id).
                                               label('spam_users')).order_by(desc("spam_users")).limit(number_of_users).
                                        group_by(UserRequest.telegram_id))
    return results.all()


async def get_user_requests(number_of_requests: int = 5) -> list:
    async with session_maker() as session:
        results = await session.execute(select(UserRequest.telegram_id, UserRequest.tg_username,
                                               UserRequest.search_type, UserRequest.search_str,
                                               UserRequest.search_time, UserRequest.report_url).
                                        order_by(desc(UserRequest.search_time)).
                                        limit(number_of_requests))
    return results.all()


async def main():
    pass
    # print(await get_user_requests())
    # print(await get_spam_users())

    # await save_user_request(tg_id='12345', tg_username='Ivan', search_type='flp_name', search_str='qwe qwe qwe',
    #                         report_url='https://osint-bot.duckdns.org/reports/20240521164914-6090714570-2_3_4.html')


if __name__ == '__main__':
    asyncio.run(main())
