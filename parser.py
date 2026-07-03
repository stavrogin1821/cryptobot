import aiohttp
from bs4 import BeautifulSoup

async def fetch_news(limit: int = 5) -> str:
    """Парсинг заголовков новостей с CoinDesk (раздел Bitcoin)."""
    url = "https://www.coindesk.com/livewire/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as resp:
                if resp.status != 200:
                    return "Не удалось загрузить новости."
                html = await resp.text()
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.select("div[class*='card-title'] a, h2 a, h3 a")[:limit]
        if not articles:
            return "Новости не найдены (изменилась структура сайта)."
        lines = []
        for i, a in enumerate(articles, 1):
            title = a.get_text(strip=True)
            link = a.get("href", "")
            if link and not link.startswith("http"):
                link = "https://www.coindesk.com" + link
            lines.append(f"{i}. {title}\n   {link}")
        return "\n\n".join(lines)
    except Exception as e:
        return f"Ошибка парсинга: {e}"