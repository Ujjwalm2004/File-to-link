import logging 
import aiohttp 
import os
from os import environ 
from pyrogram.types import *
from pyrogram.errors import *
from pyrogram import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SHORT_URL = environ.get('SHORT_URL', 'tnlinks.in')
SHORT_API = environ.get('SHORT_API', '')

async def get_shortlink(link, u_id):
          u_api = await db.get_api(u_id)
    if u_api:
        API = u_api
    else:
        API = SHORT_API
    https = link.split(":")[0]
    if "http" == https:
        https = "https"
        link = link.replace("http", https)
    url = f'https://{SHORT_URL}/api'
    params = {'api': API,
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
                    return f'https://{SHORT_URL}/api?api={API}&link={link}'

    except Exception as e:
        logger.error(e)
        return f'{SHORT_URL}/api?api={API}&link={link}'
