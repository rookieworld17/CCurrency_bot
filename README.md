# 💬 CCurrency

TelegramBot для получения информации о криптовалютах через API CoinMarketCap.

---

## 🚀 Развёртывание (Ubuntu Server)

> Подходит для VPS, облачного сервера или обычного дедика.

### 1. Установить Docker и Docker Compose

```bash
  sudo apt update
  sudo apt install docker.io docker-compose -y
  sudo systemctl enable docker
```

### 2. Клонировать репозиторий

```bash
  git clone <repo-url>
  cd CCurrency_bot
```

### 3. Создать файл `.env` по шаблону

```bash
  cp .env.example .env
  nano .env  # Вставь свои значения
```

### 4. Запустить бота

```bash
  docker-compose up --build -d
```

---

## 🐳 Docker-команды

| Команда                        | Описание                             |
|-------------------------------|--------------------------------------|
| `docker-compose up -d`        | Запуск бота в фоне                   |
| `docker-compose up --build -d`| Сборка и запуск                      |
| `docker-compose down`         | Остановка и удаление контейнеров     |
| `docker-compose restart`      | Перезапуск бота                      |
| `docker-compose logs -f`      | Просмотр логов в реальном времени    |

---

## 🧪 Разработка

> Для разработки рекомендуется виртуальное окружение

### Создать окружение

```bash
  python -m venv .venv
  source .venv/bin/activate
```

### Установка зависимостей

```bash
  pip install -r requirements.txt
```

### Обновить список зависимостей

```bash
  pip freeze > requirements.txt
```

---

## 🔐 Переменные окружения

Создай `.env` на основе `.env-example`.

### .env-example

```env
# -- Telegram --
TELEGRAM_BOT_TOKEN=

# -- CoinMarketCap --
COINMARKETCAP_USER_API=
COINMARKETCAP_URL_API=https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest
```

---