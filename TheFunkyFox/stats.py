import aiohttp
import logging
from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import URL_SHORTNER_API_KEY, URL_SHORTNER_API
from TheFunkyFox.helper_func import get_readable_time

USER_REPLY_TEXT = """<code> ᴀʀᴇ ʙʜᴀɪʏᴀ.. ᴀᴀᴘ ᴋᴏɴ ᴄʜʟᴇ ᴊᴀᴀᴏ ʏʜᴀ sᴇ ᴍᴜᴊʜᴇ ᴀᴀᴘsᴇ ʙᴀᴀᴛ ɴʜɪ ᴋʀɴɪ. </code>"""


@Bot.on_message(filters.private)
async def useless(_,message: Message):
    if USER_REPLY_TEXT:
        await message.reply(USER_REPLY_TEXT)


async def get_shortlink(link):
    https = link.split(":")[0]
    if "http" == https:
        https = "https"
        link = link.replace("http", https)
    url = f'http://urlshortx.com/api'
    params = {'api': URL_SHORTNER_API_KEY,
              'url': link,
              }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                data = await response.json()
                if data["status"] == "success":
                    return data['shortenedUrl']
                else:
                    logger.error(f"Error: {data['message']}")
                    return f'{URL_SHORTNER_API}={URL_SHORTNER_API_KEY}&link={link}'

    except Exception as e:
        logger.error(e)
        return f'{URL_SHORTNER_API}={URL_SHORTNER_API_KEY}&link={link}'
