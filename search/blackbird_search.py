import asyncio
import json

from blackbird import findUsername


async def find_user_by_username(username: str) -> list | None:
    data = await findUsername(username=username, interfaceType='None')
    result = []
    for site in data["sites"]:
        if site["response-status"] == '200 OK' and site["status"] == 'FOUND':
            res = {}
            res["Site"] = site.get("app", '')
            res["Profile Link"] = site.get("url", '')
            for item in site["metadata"]:
                type = item.get("type", '')
                if type == 'image':
                    res["Picture"] = item.get("value", '')
            if len(res):
                result.append(res)
    return result if len(result) else None


async def main():
    results = await find_user_by_username('qwerty')
    print(json.dumps(results, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        pass
    finally:
        exit(0)
