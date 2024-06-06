import asyncio
import json
import httpx

from logging import getLogger
from typing import Any
from bot.configuration import bot_configuration as bot_config


logger = getLogger(__name__)


async def do_person_request(name: str) -> dict | None:
    headers = {"user-agent": "Karyna Barkar's telegram bot", "accept": "*/*"}
    url = 'https://opendatabot.com/api/v3'
    endpoint = f'{url}/person'
    params = {"apiKey": bot_config.opendata_api_key, "pib": name.upper()}

    try:
        async with httpx.AsyncClient(timeout=50) as client:
            response = await client.get(url=endpoint, headers=headers, params=params)
        resp_json = response.json()
        if resp_json['status'] == "ok":
            # print(resp_json['data'])
            # print(resp_json['data']['factors'])
            return resp_json
        else:
            logging.debug('Request failed')
            return None
    except:
        return None


async def get_person_info(person: str) -> list | None:
    person_info = await do_person_request(person)
    if person_info is None or len(person_info) == 0:
        logger.debug('No person found')
        return None
    else:
        result = []
        result_text = ''
        for item in person_info['data']['factors']:
            if 'count' in item.keys():
                prefix = f'{item["icon"]} | {item["factorGroup"]} | {item["type"]}'
                for subitem in item['items']:
                    subitem_str = prefix
                    for key, value in subitem.items():
                        if value:
                            if key == 'link':
                                # subitem_desc = ''
                                # subitem_details = self.do_request(endpoint=value)
                                # for k, v in subitem_details.items():
                                #     subitem_desc += f'{k} - {v} | '
                                # subitem_str += subitem_desc
                                value = ''
                            subitem_str = subitem_str + f' | {key} - {value}'
                    result_text += f'{subitem_str} \n'
                    result.append(subitem_str)
            else:
                item_str = ''
                for key, value in item.items():
                    if value:
                        item_str += f'{key} - {value} | '
                result_text += f'{item_str} \n'
                result.append(item_str)
    logger.debug(f'Person info: {result_text}')
    return result


async def get_opendata_info(person: str) -> list[Any] | None:
    person_info = await do_person_request(person)
    if person_info is None or len(person_info) == 0:
        logger.debug('No person found')
        return None
    else:
        # print(person_info['data']['factors'])
        result = []
        for item in person_info['data']['factors']:
            res = {}
            if item["factorGroup"] == 'edr':
                res["Name"] = item.get("text", '') + f' ({item.get("status", '')}) ' + item.get("fullName", '')
                res["Details"] = item.get("activities", '') + ' ' + item.get("location", '')
                res["Location"] = item.get("location", '') + ' ' + item.get("regionName", '')
            elif item["factorGroup"] == 'risk':
                res["Name"] = item.get("fullName", '')
                res["Details"] = item.get("birthDate", '') + ' ' + item.get("text", '')
                res["Location"] = item.get("ovd", '') + ' ' + item.get("lostPlace", '')
            elif item["factorGroup"] == 'publicOfficial':
                res["Name"] = item.get("pib", '')
                res["Details"] = item.get("text", '')
                res["Location"] = item.get("lastWorkPlace", '') + ' ' + item.get("lastWorkPost", '')
            elif item["factorGroup"] == 'selfEmployed':
                res["Name"] = item.get("fullName", '')
                res["Details"] = item.get("text", '')
                res["Location"] = item.get("racalc", '') + ' ' + item.get("regionName", '')
            if len(res):
                result.append(res)
    logger.debug(f'Person info: {result}')
    if result not in [[{}], []]:
        return result
    else:
        return None


async def main():
    person_info = await get_opendata_info('СЛОБОДЯНИК СЕРГІЙ ІВАНОВИЧ')
    print(json.dumps(person_info, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        pass
    finally:
        exit(0)
