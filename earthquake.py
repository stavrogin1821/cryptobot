import aiohttp
from datetime import datetime, timezone

async def get_earthquakes(min_magnitude: float = 4.0, limit: int = 5) -> str:
    """
    Модуль для получения последних землетрясений с USGS (бесплатный API, без ключа).
    """
    url = (
        f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"
        f"{min_magnitude}_day.geojson"
    )
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    return "Ошибка при получении данных о землетрясениях."
                data = await resp.json()
                features = data.get("features", [])
                if not features:
                    return f"Нет землетрясений с магнитудой ≥ {min_magnitude} за последние сутки."
                lines = []
                for eq in features[:limit]:
                    props = eq["properties"]
                    place = props["place"]
                    mag = props["mag"]
                    time_ms = props["time"]
                    t = datetime.fromtimestamp(time_ms / 1000, tz=timezone.utc)
                    time_str = t.strftime("%Y-%m-%d %H:%M UTC")
                    depth = eq["geometry"]["coordinates"][2]
                    lines.append(
                        f"📍 {place}\n"
                        f"   Магнитуда: {mag:.1f} | Глубина: {depth:.1f} км | {time_str}"
                    )
                return "\n\n".join(lines)
    except Exception as e:
        return f"Ошибка при запросе землетрясений: {e}"