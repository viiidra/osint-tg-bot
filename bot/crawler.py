from logging import getLogger
from search.opendata_search import get_opendata_info
from search.bigbookname_search import find_persons as bigbook_persons
from search.vk_search import find_persons as vk_search_persons
from search.blackbird_search import find_user_by_username
from search.duckduckgo import find_persons as ddg_find_persons

logger = getLogger(__name__)


async def uni_search(search_type: str, name: str):
    match search_type:
        case 'flp_name' | 'fl_name' | 'last_name':
            results = {
                "BigBook Results": await bigbook_persons(name=name),
                "OpenData Results": await get_opendata_info(person=name),
                "VK Results": await vk_search_persons(name=name),
                "DDG": await ddg_find_persons(name=name),
                "Facebook": await ddg_find_persons(name=f'site:facebook.com {name}')
            }
            return results
        case 'nickname':
            results = {
                "BlackBird Results": await find_user_by_username(username=name),
                "BigBook Results": await bigbook_persons(name=name),
                "OpenData Results": await get_opendata_info(person=name)
            }
            return results
        case _:
            return None
