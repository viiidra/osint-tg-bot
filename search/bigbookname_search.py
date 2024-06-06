import asyncio
import json
import httpx


from logging import getLogger
from bs4 import BeautifulSoup

logger = getLogger(__name__)

GATHER_ADDITIONAL_INFO: bool = False

cookies = {
    'PHPSESSID': 'dj6ikcb10gp7dc68li7svcq5l8',
    '_ga_5EWXP61WWQ': 'GS1.1.1709690129.1.0.1709690129.0.0.0',
    '_ga': 'GA1.1.1763778263.1709690129',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://bigbookname.com',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://bigbookname.com/search_post.php',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}


async def get_people_by_name(name: str) -> dict | None:
    data = {
        'fio': f'{name}',
        'combo': '',
        'combo_new_value': 'true',
        'combo2': '',
        'combo2_new_value': 'true',
        'gender1': '0',
        'sort': '0',
        'get_cityid': '',
        'get_countryid': '',
        'type_search': '1',
        'local_call_ban': '1',
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post('https://bigbookname.com/search_post.php', headers=headers, data=data)
        if len(response.text):
            return response.json()
        else:
            return None


async def parse_user_page(url: str) -> dict:
    result = {}
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        response = await client.get(url=url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features="html.parser")  # html5lib # lxml
            profile_info_short = soup.find('div',
                                           class_='profile_info_short').find_all('div', class_='line_data')
            for item in profile_info_short:
                item_name = item.find('div', class_='field').text.strip().replace(':', '')
                item_value = item.find('div', class_='field_data').text.strip()
                result[item_name] = item_value
            profile_info_full = soup.find('div',
                                          class_='profile_info_full').find_all('div', class_='line_data')
            for item in profile_info_full:
                item_name = item.find('div', class_='field').text.strip().replace(':', '')
                item_value = item.find('div', class_='field_data').text.strip()
                result[item_name] = item_value
    return result


async def find_persons(name: str) -> list | None:
    try:
        people_list = await get_people_by_name(name)
        persons = []
        for person in people_list['persons']:
            person_dict = {'Name': f'{person["ln"]} {person["fn"]}',
                           'Age': person["ag"],
                           'Home': f'{person["ci"] + ", " if person["ci"] else ""}{person["co"] if person["co"] else ""}',
                           'Picture': f'{person["av"]}',
                           'Profile Link': f'https://bigbookname.com/en/user/{person["ur"]}-{person["id"]}'}
            if GATHER_ADDITIONAL_INFO:
                additional_info = await parse_user_page(person_dict['Profile Link'])
                person_dict.update(additional_info)
            persons.append(person_dict)
        return persons
    except:
        return None


async def main():
    results = await find_persons('Буданов Максим')
    print(json.dumps(results, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        pass
    finally:
        exit(0)
