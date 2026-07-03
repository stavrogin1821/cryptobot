# CryptoBot — многофункциональный Telegram-бот

Асинхронный бот на aiogram 3.x. Умеет:
- Показывать цены криптовалют (CoinGecko)
- Присылать свежие новости (CoinDesk)
- Сообщать погоду в любом городе (wttr.in)
- Отображать последние землетрясения (USGS)

## Команды
| Команда | Описание | Пример |
|---------|----------|--------|
| `/start` | Справка | |
| `/price <монета>` | Цена криптовалюты | `/price bitcoin` |
| `/news` | 5 последних новостей с CoinDesk | `/news` |
| `/weather <город>` | Текущая погода | `/weather Moscow` |
| `/earthquake [M]` | Землетрясения с магнитудой ≥ M (по умолчанию 4.0) | `/earthquake 5.5` или просто `/eq` |

## Установка и запуск
### 1. Клонировать репозиторий:
```bash
git clone https://github.com/stavrogin1821/cryptobot.git
cd cryptobot
pip install -r requirements.txt
```
### 2. Получить токен у @BotFather и установить переменную окружения:
```bash
export BOT_TOKEN="ваш_токен"
```
### 3. Запустить:
```bash
python main.py
```
## Зависимости
+ aiogram>=3.0
+ aiohttp
+ beautifulsoup4
