import asyncio
import pytest
import allure
import json
from jsonschema import validate
from faker import Faker
from search.opendata_search import do_person_request, get_person_info

with open('./json_schemas/opendata_person.json') as schema_file:
    schema = json.loads(schema_file.read())


def fake_names_generator(count: int) -> list:
    locale = ['uk_UA']
    fake = Faker(locale)
    users_list = []
    for _ in range(count):
        name = fake.name()
        users_list.append(name)
    return users_list


@allure.suite("OpenData Tests")
class TestOpenDataPerson:

    @pytest.mark.asyncio
    @allure.title("Test OpenData Person JSON Schema")
    @allure.feature("Getting personal data from OpenData")
    @pytest.mark.parametrize("pib", fake_names_generator(5))
    async def test_opendata_person(self, pib: str):
        with allure.step("Getting personal data for {}".format(pib)):
            person_info = await do_person_request(pib)
        if person_info is not None:
            with allure.step("Validating JSON Schema of response {}".format(person_info)):
                validate(person_info, schema)
        else:
            with allure.step("Exiting, no personal data found"):
                assert True, 'Person not found'

    @pytest.mark.asyncio
    @allure.title("Test Person Data Formatter")
    @allure.feature("Formatting personal data from OpenData")
    @pytest.mark.parametrize("pib", fake_names_generator(5))
    async def test_person_data_formatter(self, pib: str):
        with allure.step("Getting personal data for {}".format(pib)):
            person_info = await get_person_info(pib)
        if person_info is not None and len(person_info) > 0:
            with allure.step(f'Validating that {person_info} is formatted correctly'):
                assert isinstance(person_info, list)
        else:
            with allure.step("Exiting, no personal data found"):
                assert person_info == [], 'Person not found'
