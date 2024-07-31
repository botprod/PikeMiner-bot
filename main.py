from utils.core.telegram import Accounts
from utils.starter import start, get_links
import asyncio
import os

banner = """
  ___ ___ _  _____ __  __   _   _  _  
 | _ \_ _| |/ / __|  \/  | /_\ | \| | 
 |  _/| || ' <| _|| |\/| |/ _ \| .` | 
 |_| |___|_|\_\___|_|  |_/_/ \_\_|\_|                                     
"""
async def main():
    print(banner)
    print("Soft's author: https://t.me/botpr0d\n")
    action = int(input("Select action:\n1. Start soft\n2. Get auth links\n3. Create sessions\n\n> "))

    if not os.path.exists('sessions'): os.mkdir('sessions')
    if not os.path.exists('sessions/accounts.json'):
        with open("sessions/accounts.json", 'w') as f:
            f.write("[]")

    if action == 3:
        await Accounts().create_sessions()

    if action == 2:
        accounts = await Accounts().get_accounts()
        tasks = []
        for thread, account in enumerate(accounts):
            session_name, phone_number, proxy = account.values()
            tasks.append(asyncio.create_task(
                get_links(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)))


        await asyncio.gather(*tasks)

    if action == 1:
        accounts = await Accounts().get_accounts()
        tasks = []
        for thread, account in enumerate(accounts):
            session_name, phone_number, proxy = account.values()
            tasks.append(asyncio.create_task(
                start(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)))

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
