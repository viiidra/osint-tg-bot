import asyncio
from googletrans.client import Translator
from googletrans.constants import LANGUAGES

translator = Translator()


async def translate(text: str, lang_code: str) -> str:
    translated = translator.translate(text=text, dest=lang_code)
    return translated.text


async def detect_language(text: str):
    str_ua = await translate(text=text, lang_code='uk')
    str_en = await translate(text=text, lang_code='en')
    str_ru = await translate(text=text, lang_code='ru')
    if text.lower() == str_ua.lower():
        lang = 'uk'
    elif text.lower() == str_en.lower():
        lang = 'en'
    elif text.lower() == str_ru.lower():
        lang = 'ru'
    else:
        lang = translator.detect(text).lang
        if lang in ['bg', 'be', 'kk', 'ky', 'mk', 'tt']:
            lang = 'ru'
        if lang in ['fi', 'fr', 'de', 'es', 'pt', 'sv', 'hi']:
            lang = 'en'
    return {'lang_code': lang, 'language': LANGUAGES[lang]}


async def main():
    print(await detect_language('Едита Андрощук'))
    print(await detect_language('Христина Макогон'))
    print(await detect_language('Адам Теліженко'))

    lang = await detect_language('Максим Левицький')
    print(lang)
    # for _ in range(100):


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        pass
    finally:
        exit(0)
