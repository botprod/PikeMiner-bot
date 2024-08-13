import os
from utils.pike import Pike
from utils.core import logger
import datetime
from utils.core.telegram import Accounts
import pandas as pd

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
                    logger.info(
                        f"Thread {thread} | {account} | Arkenstone: {acc_stat[0]['arkenstone']} Tourmaline: {acc_stat[0]['tourmaline']} Melange: {acc_stat[0]['melange']}")
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


async def stats():
    accounts = await Accounts().get_accounts()
    tasks = []
    for thread, account in enumerate(accounts):
        session_name, phone_number, proxy = account.values()
        tasks.append(asyncio.create_task(
            Pike(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy).stats()))
    data = await asyncio.gather(*tasks)
    path = f"statistics/statistics_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    columns = ['Phone number', 'Name', 'Coal', 'Arkenstone', 'Tourmaline', 'Melange', 'Mana', 'Guild ID',
               'Total referrals',
               'Proxy (login:password@ip:port)']
    if not os.path.exists('statistics'): os.mkdir('statistics')
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(path, index=False, encoding='utf-8-sig')
    logger.success(f"Saved statistics to {path}")
