import json
import random
import urllib

from utils.core import logger
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestWebView
import asyncio
from urllib.parse import unquote, quote, parse_qs
from data import config
import aiohttp
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector


class Pike:
    def __init__(self, thread: int, session_name: str, phone_number: str, proxy: [str, None]):
        self.headersLogin = None
        self.headers_hit = None
        self.useragent = UserAgent().random
        self.account = session_name + '.session'
        self.thread = thread
        self.tg_init_data = None
        self.proxy = f"{config.PROXY_TYPES['REQUESTS']}://{proxy}" if proxy is not None else None
        connector = ProxyConnector.from_url(self.proxy) if proxy else aiohttp.TCPConnector(verify_ssl=False)
        if proxy:
            proxy = {
                "scheme": config.PROXY_TYPES['TG'],
                "hostname": proxy.split(":")[1].split("@")[1],
                "port": int(proxy.split(":")[2]),
                "username": proxy.split(":")[0],
                "password": proxy.split(":")[1].split("@")[0]
            }

        self.client = Client(
            name=session_name,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            workdir=config.WORKDIR,
            proxy=proxy,
            lang_code='ru'
        )
        self.session = aiohttp.ClientSession(trust_env=True, connector=connector)

    # maybe useless
    async def get_links(self):
        await asyncio.sleep(random.uniform(*config.DELAYS['ACCOUNT']))
        await self.login
        await self.logout()
        await self.client.connect()
        return 'ok'

    async def battery_taps(self, endurance: int = 0):
        logger.info(f"Thread {self.thread} | {self.account} | Hit {endurance} times")
        for _ in range(endurance):
            url = 'https://pikeman-f14904a69fc1.herokuapp.com/users/hit'
            resp = await self.session.get(url, headers=self.headers_hit)
            response_data = await resp.json()
            user_data = response_data.get('data', {}).get('user', {})
            data = user_data.get('coal') if user_data else None
            logger.success(f"Thread {self.thread} | {self.account} | Hit! Coal: {data}")
            await asyncio.sleep(random.uniform(*config.DELAYS['PIKE']))

    async def logout(self):
        await self.session.close()

    async def login(self):
        await asyncio.sleep(random.uniform(*config.DELAYS['ACCOUNT']))
        query = await self.get_tg_web_data()
        if query is None:
            logger.error(f"Thread {self.thread} | {self.account} | Session {self.account} invalid")
            await self.logout()
            return None

        self.tg_init_data = query
        self.headersLogin = {
            'Accept': '*/*',
            'Accept-Language': 'en-RU,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': 'https://pikeman-twa-c69da4fa6518.herokuapp.com',
            'Referer': 'https://pikeman-twa-c69da4fa6518.herokuapp.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': self.useragent,
            'content-type': 'application/json',
            'initial-data': query,
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-bot-id': 'prod-bot',
        }
        self.headers_hit = {
            'Accept': '*/*',
            'Accept-Language': 'en-RU,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'DNT': '1',
            'Initial-Data': query,
            'Origin': 'https://pikeman-twa-c69da4fa6518.herokuapp.com',
            'Referer': 'https://pikeman-twa-c69da4fa6518.herokuapp.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': self.useragent,
            'X-Bot-Id': 'prod-bot',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('https://pikeman-f14904a69fc1.herokuapp.com/users/get',
                                   headers=self.headersLogin) as response:
                if response.status == 200:
                    response_text = await response.text()
                    response_json = json.loads(response_text)

                    if "data" in response_json:
                        user_data = response_json["data"]
                        if "user" in user_data:
                            user = user_data["user"]
                            if "endurance" in user:
                                return True, user["endurance"]
                            else:
                                logger.error("Key 'endurance' not found in user data")
                                return False, 0
                        else:
                            logger.error("Key 'user' not found in data")
                            return False, 0
                    else:
                        logger.error("Key 'data' not found in response")
                        return False, 0
                else:
                    print(f"Error: HTTP status {response.status}")
                    print(await response.text())
                    return False, 0

    async def check_in(self):
        async with aiohttp.ClientSession() as session:
            url = 'https://pikeman-f14904a69fc1.herokuapp.com/users/checkin'
            async with session.get(url, headers=self.headers_hit) as response:
                if response.status == 200 and b"You have already checked in today" not in await response.read():
                    logger.success(f"Thread {self.thread} | {self.account} | Checkin success")

    async def get_tg_web_data(self):
        try:
            await self.client.connect()
            await self.client.send_message("pike_man_bot", '/start 918432365')
            peer = await self.client.resolve_peer('pike_man_bot')
            await asyncio.sleep(3)
            web_view = await self.client.invoke(RequestWebView(
                peer=peer,
                bot=peer,
                platform='android',
                from_bot_menu=False,
                start_param='918432365',
                url='https://pikeman-twa-c69da4fa6518.herokuapp.com/'
            ))
            await self.client.disconnect()
            auth_url = web_view.url
            await self.session.get(auth_url)
            logger.success(f"Thread {self.thread} | {self.account} | Auth url: {auth_url}")
            return urllib.parse.unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        except Exception as e:
            return None
