import os
import random
from utils.pike import Pike
from utils.core import logger
import datetime

from aiohttp.client_exceptions import ContentTypeError
import asyncio
from data import config


async def start(thread: int, session_name: str, phone_number: str, proxy: [str, None]):
    pike = Pike(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
    account = session_name + '.session'
    status, endurance = await pike.login()
    if status:
        logger.success(f"Thread {thread} | {account} | Login")
        await pike.check_in()
        while True:
            try:
                if endurance != 0:
                    acc_stat = await pike.battery_taps(endurance)
                    guild_id = acc_stat[0]['guild_id']
                    if guild_id != config.GUILD_ID:
                        await pike.join_in_guild()
                logger.info(f"Thread {thread} | {account} | Sleep: 4 hours")
                await asyncio.sleep(14400)
                await pike.check_in()
            except ContentTypeError as e:
                logger.error(f"Thread {thread} | {account} | Error: {e}")
                await asyncio.sleep(12)
            except Exception as e:
                logger.error(f"Thread {thread} | {account} | Error: {e}")
                await asyncio.sleep(5)
    await pike.logout()


async def get_links(thread: int, session_name: str, phone_number: str, proxy: [str, None]):
    beer = Pike(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
    await beer.get_tg_web_data()
    await beer.logout()