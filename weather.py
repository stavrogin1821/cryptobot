import aiohttp

async def get_weather(city: str) -> str:
    """
    Модуль для получения погоды через wttr.in (без API-ключа).
    Возвращает текстовое описание погоды.
    """
    url = f"https://wttr.in/{city}?format=j1&lang=ru"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    return "Не удалось получить погоду. Проверь название города."
                data = await resp.json()
                current = data.get("current_condition", [{}])[0]
                if not current:
                    return "Город не найден."
                temp_c = current.get("temp_C", "?")
                feels_like = current.get("FeelsLikeC", "?")
                description = current.get("weatherDesc", [{}])[0].get("value", "неизвестно")
                wind = current.get("winddir16Point", "?") + " " + current.get("windspeedKmph", "?") + " км/ч"
                humidity = current.get("humidity", "?") + "%"
                pressure = current.get("pressure", "?") + " мб"
                area = data.get("nearest_area", [{}])[0]
                area_name = area.get("areaName", [{}])[0].get("value", "неизвестно")
                country = area.get("country", [{}])[0].get("value", "")
                return (
                    f"Погода в {city} ({area_name}, {country}):\n"
                    f"🌡 Температура: {temp_c}°C (ощущается как {feels_like}°C)\n"
                    f"☁ {description}\n"
                    f"💨 Ветер: {wind}\n"
                    f"💧 Влажность: {humidity}\n"
                    f"🔽 Давление: {pressure}"
                )
    except Exception as e:
        return f"Ошибка при получении погоды: {e}"