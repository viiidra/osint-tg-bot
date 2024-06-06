import asyncio
import json

from duckduckgo_search import AsyncDDGS

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9,zh;q=0.8,pt-BR;q=0.7,pt;q=0.6,zh-CN;q=0.5,uk;q=0.4,ru-UA;q=0.3',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}


async def get_people_by_name(name: str) -> list:
    results = await AsyncDDGS(proxy=None, headers=headers).aimages(keywords=name, max_results=40, safesearch='on')
    return results


async def find_persons(name: str) -> list | None:
    results = await get_people_by_name(name)
    if not results:
        return None
    else:
        try:
            people_profiles = []
            for person in results:
                result = {'Title': person['title'],
                          'Picture': person['thumbnail'],
                          'Link': person['url']}
                people_profiles.append(result)
            if len(people_profiles):
                return people_profiles
            else:
                return None
        except:
            return None


async def main():

    results = await get_people_by_name('Левицкий Максим Алексеевич')
    print(json.dumps(results, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
