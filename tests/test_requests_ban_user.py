import asyncio
import pytest
import allure
from time import sleep

from database.requests import ban_tg_user, is_user_banned, unban_tg_user


@allure.suite("PostgreSQL Requests Tests")
class TestDatabaseBanRequests:

    @pytest.mark.asyncio
    @allure.title("Test Requests To ban and unban a user")
    @pytest.mark.parametrize("tg_id", (111,))
    async def test_ban_user(self, tg_id):
        with allure.step("Ban a user"):
            await ban_tg_user(tg_id=tg_id, ban_time=None)
            sleep(1)
        with allure.step("Check if user banned"):
            is_banned = await is_user_banned(tg_id)
            assert is_banned
        with allure.step("Unban a user"):
            await unban_tg_user(tg_id)
            sleep(1)
        with allure.step("Check if user unbanned"):
            is_banned = await is_user_banned(tg_id)
            assert is_banned == False

