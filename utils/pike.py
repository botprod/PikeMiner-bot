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

    async def stats(self):
        await asyncio.sleep(random.uniform(*config.DELAYS['ACCOUNT']))
        await self.login()
        async with aiohttp.ClientSession() as session:
            async with session.get('https://pikeman-f14904a69fc1.herokuapp.com/users/get',
                                   headers=self.headersLogin, ssl=False) as response:
                if response.status == 200:
                    response_text = await response.text()
                    response_data = json.loads(response_text)
                    user_data = response_data.get('data', {}).get('user', {})
                    coal = user_data.get('coal', None)
                    arkenstone = user_data.get('arkenstone')
                    tourmaline = user_data.get('tourmaline')
                    melange = user_data.get('melange')
                    mana = user_data.get('mana')
                    guild_id = user_data.get('guildId')
                    total_referrals = user_data.get('totalReferrals')
                    await self.logout()
                    await self.client.connect()
                    me = await self.client.get_me()
                    phone_number, name = "'" + me.phone_number, f"{me.first_name} {me.last_name if me.last_name is not None else ''}"
                    await self.client.disconnect()
                    proxy = self.proxy.replace('http://', "") if self.proxy is not None else '-'
                    return [phone_number, name, str(coal), str(arkenstone), str(tourmaline), str(melange), str(mana),
                            str(guild_id),
                            str(total_referrals),
                            proxy]

    async def join_in_guild(self):
        url = f'https://pikeman-f14904a69fc1.herokuapp.com/guilds/leave'
        resp = await self.session.get(url, headers=self.headers_hit, ssl=False)
        response_data = await resp.json()

    async def battery_taps(self, endurance: int = 0):
        logger.info(f"Thread {self.thread} | {self.account} | Hit {endurance} times")
        results = []
        for _ in range(endurance):
            url = 'https://pikeman-f14904a69fc1.herokuapp.com/users/hit'
            resp = await self.session.get(url, headers=self.headers_hit, ssl=False)
            response_data = await resp.json()

            user_data = response_data.get('data', {}).get('user', {})
            drop = response_data.get('data', {}).get('drop', None)
            coal = response_data.get('coal', None)
            hits = response_data.get('hits', None)
            user_id = user_data.get('id')
            created_at = user_data.get('createdAt')
            wallet = user_data.get('wallet')
            invited_by_user = user_data.get('invitedByUser')
            invited_by_partner = user_data.get('invitedByPartner')
            total_referrals = user_data.get('totalReferrals')
            username = user_data.get('username')
            first_name = user_data.get('firstName')
            partner_link = user_data.get('partnerLink')
            last_checkin = user_data.get('lastCheckin')
            language = user_data.get('language')
            next_checkin = user_data.get('nextCheckin')
            hits_count = user_data.get('hits')
            arkenstone = user_data.get('arkenstone')
            tourmaline = user_data.get('tourmaline')
            melange = user_data.get('melange')
            endurance_value = user_data.get('endurance')
            mana = user_data.get('mana')
            last_endurance_update = user_data.get('lastEnduranceUpdate')
            max_endurance = user_data.get('maxEndurance')
            guild_id = user_data.get('guildId')
            endurance_point_restores_in = user_data.get('endurancePointRestoresIn')

            logger.success(f"Thread {self.thread} | {self.account} | HIT! Drop: {drop}")
            await asyncio.sleep(random.uniform(*config.DELAYS['PIKE']))
            results.clear()
            results.append({
                'user_id': user_id,
                'created_at': created_at,
                'wallet': wallet,
                'invited_by_user': invited_by_user,
                'invited_by_partner': invited_by_partner,
                'total_referrals': total_referrals,
                'username': username,
                'first_name': first_name,
                'partner_link': partner_link,
                'last_checkin': last_checkin,
                'language': language,
                'next_checkin': next_checkin,
                'hits_count': hits_count,
                'arkenstone': arkenstone,
                'tourmaline': tourmaline,
                'melange': melange,
                'endurance_value': endurance_value,
                'mana': mana,
                'last_endurance_update': last_endurance_update,
                'max_endurance': max_endurance,
                'guild_id': guild_id,
                'endurance_point_restores_in': endurance_point_restores_in,
                'coal': coal,
                'hits': hits,
                'drop': drop,
            })
        return results

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
                                   headers=self.headersLogin, ssl=False) as response:
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
            async with session.get(url, headers=self.headers_hit, ssl=False) as response:
                if response.status == 200 and b"You have already checked in today" not in await response.read():
                    logger.success(f"Thread {self.thread} | {self.account} | Checkin success")

    async def get_tg_web_data(self):
        try:
            await self.client.connect()
            await self.client.send_message("pike_man_bot", f'/start {config.REF_ID}')
            peer = await self.client.resolve_peer('pike_man_bot')
            await asyncio.sleep(3)
            web_view = await self.client.invoke(RequestWebView(
                peer=peer,
                bot=peer,
                platform='android',
                from_bot_menu=False,
                start_param=f"{config.REF_ID}",
                url='https://pikeman-twa-c69da4fa6518.herokuapp.com/'
            ))
            auth_url = web_view.url
            await self.client.disconnect()
            return urllib.parse.unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        except Exception as e:
            return None
