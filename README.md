# Pike Man Bot
Clicker for [https://t.me/pike_man_bot](https://t.me/pike_man_bot?start=918432365)

My telegram channel: [BOTPROD](https://t.me/botpr0d "BOTPROD") 

## Functionality
| Functional                                | Supported |
|-------------------------------------------|:---------:|
| Multithreading                            |     ✅     |
| Binding a proxy to a session              |     ✅     |
| Random sleep time between accounts; hits  |     ✅     |
| Support pyrogram .session                 |     ✅     |
| Get login links for all accounts          |     ✅     |

## Settings data/config.py
| Setting                  | Description                                                                                    |
|--------------------------|------------------------------------------------------------------------------------------------|
| **API_ID / API_HASH**    | Platform data from which to launch a Telegram session                                          |
| **DELAYS-ACCOUNT**       | Delay between connections to accounts (the more accounts, the longer the delay)                |
| **DELAYS-PIKE**          | Delay between stone strikes                                                                    |
| **PROXY_TYPES-TG**       | Proxy type for telegram session                                                                |
| **PROXY_TYPES-REQUESTS** | Proxy type for requests                                                                        |
| **WORKDIR**              | directory with session                                                                         |
| **TIMEOUT**              | timeout in seconds for checking accounts on valid                                              |

## Requirements
- Python 3.9 (you can install it [here](https://www.python.org/downloads/release/python-390/)) 
- Telegram API_ID and API_HASH (you can get them [here](https://my.telegram.org/auth))

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
## Usage
1. Run the bot:
   ```bash
   python main.py
   ```
