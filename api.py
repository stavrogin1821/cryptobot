import aiohttp
import asyncio
from datetime import datetime, timedelta

CACHE = {}          # {coin_id: (price, expiry)}
CACHE_DURATION = 30 # секунд

async def get_crypto_price(coin_id: str) -> str:
    """Асинхронно получить цену в USD с CoinGecko API."""
    now = datetime.now()
    if coin_id in CACHE:
        price, expiry = CACHE[coin_id]
        if now < expiry:
            return f"Цена {coin_id.upper()}: ${price:,.2f} (кеш)"

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    return f"Ошибка API: статус {resp.status}"
                data = await resp.json()
                if coin_id not in data or "usd" not in data[coin_id]:
                    return f"Криптовалюта '{coin_id}' не найдена."
                price = data[coin_id]["usd"]
                CACHE[coin_id] = (price, now + timedelta(seconds=CACHE_DURATION))
                return f"Цена {coin_id.upper()}: ${price:,.2f}"
    except asyncio.TimeoutError:
        return "Таймаут запроса к API."
    except Exception as e:
        return f"Ошибка: {e}"