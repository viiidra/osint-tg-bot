import asyncio
import pytest
import allure

from database.engine import get_pg_version


@allure.suite("PostgreSQL Tests")
class TestPostreSQLDatabaseLink:

    @pytest.mark.asyncio
    @allure.title("Test PostgreSQL Link")
    @allure.feature("Getting version of PostgreSQL")
    async def test_postresql_version(self):
        with allure.step("Getting version of PostgreSQL"):
            version_info = await get_pg_version()
        if version_info is not None:
            with allure.step("Validating response {}".format(version_info)):
                assert "PostgreSQL" in version_info
        else:
            assert False, "PostgreSQL version is not available"
