import asyncio
import json
import httpx

from logging import getLogger
from bs4 import BeautifulSoup

logger = getLogger(__name__)

cookies = {
    'remixlang': '3',
    'remixstlid': '9119111786008833757_1Ley8lLP1GbaN2Mp3MQcOzYKnYIB2tZkfVYnmOInjZD',
    'remixstid': '2114019338_24RJRZpoXzTWnzRF4NfWWEJYjeou4ZsDInCAvtHx3RL',
    'remixlgck': '8ece74cd0be95ab203',
    'remixscreen_width': '1512',
    'remixscreen_height': '982',
    'remixscreen_dpr': '2',
    'remixscreen_depth': '30',
    'remixscreen_orient': '1',
    'remixscreen_winzoom': '1',
    'remixdark_color_scheme': '1',
    'remixcolor_scheme_mode': 'auto',
    'remixdt': '-3600',
    'remixnp': '0',
    'remixgp': 'fdc1a114e55cc7cc6bfebc8f96cde4c5',
    'tmr_lvid': '7e44a926ca7b7b239ede7f2cae27a138',
    'tmr_lvidTS': '1709679228556',
    'remixrt': '1',
    'tmr_detect': '0%7C1709679239660',
    'remixua': '52%7C-1%7C320%7C1408532450',
    'remixsts': '%7B%22data%22%3A%5B%5B1709721247%2C%22search_attempts%22%2C%22friends_find%22%2Ctrue%2C1%2C%22%u0421%u041E%u041B%u041E%u041C%u041E%u041D%22%2C120%2C%223877424197134904915%22%2C0%2C%22243233%22%2C%22%22%2C%22%22%2C%22%22%2C0%2Cnull%2C0%5D%2C%5B1709721247%2C%22counters_check%22%2C1%5D%5D%2C%22uniqueId%22%3A105960946.88047035%7D',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://vk.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://vk.com/al_search.php?act=search_request',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

params = {
    'act': 'search_request',
}


async def get_people_by_name(name: str) -> str:
    data = {
        'act': 'search_request',
        'al': '1',
        'c[photo]': '0',
        'c[q]': f'{name}',
        'c[section]': 'people',
        'c[sort]': '0',
        'change': '1',
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post('https://vk.com/al_search.php',
                                     params=params, cookies=cookies, headers=headers, data=data)
    return response.text


async def find_persons(name: str) -> list | None:
    try:
        people_page = await get_people_by_name(name)
        people_profiles = []
        soup = BeautifulSoup(json.loads(people_page)['payload'][1][1], features="html.parser")  # html5lib # lxml
        profiles = soup.find_all('div', class_='people_row')
        for profile in profiles:
            result = {'Name': profile.find('div', class_='labeled name').text.strip(),
                      'Profile Link': f'https://vk.com{profile.find("a").attrs["href"].strip()}',
                      'Avatar Link': profile.find('a', class_='AvatarRich').find('img').get('src')}
            result['Possible nickname'] = (
                profile.find("a").attrs["href"].strip().split('/'))[-1] if '/id' not in result['Profile Link'] else ''
            people_profiles.append(result)
        if len(people_profiles):
            return people_profiles
        else:
            return None
    except:
        return None


async def main():
    results = await find_persons('Максим Левицкий')
    print(json.dumps(results, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        pass
    finally:
        exit(0)



