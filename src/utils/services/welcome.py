def get_welcome_message(lang: str = 'EN') -> str:
    if lang == 'RU':
        return (
            "👋 *Добро пожаловать в CCurrency\\!*\n"
            "_Актуальные курсы криптовалют прямо в Telegram_\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "📖 *Как пользоваться ботом*\n\n"

            "💱 *Токен → USDT / USDC*\n"
            "Укажите количество и тикер — бот покажет стоимость в стейблкоинах\\.\n"
            "Примеры: `0.01 BTC` \\| `0.5 ETH` \\| `BTC 0.001`\n\n"

            "🔄 *USDT / USDC → Токен*\n"
            "Укажите сумму и тикер через дефис — бот рассчитает, сколько монет вы получите\\.\n"
            "Примеры: `100-BTC` \\| `500-ETH` \\| `1000-SOL`\n\n"

            "📊 *Информация о токене*\n"
            "Отправьте только тикер — бот выведет цену, Market Cap и FDV\\.\n"
            "Примеры: `BTC` \\| `ETH` \\| `SOL` \\| `TON`\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "ℹ️ *Полезно знать*\n"
            "• Поддерживаются все токены с [CoinMarketCap](https://coinmarketcap\\.com)\n"
            "• Цены обновляются в реальном времени\n"
            "• Запятая и точка работают оба: `0,5` и `0.5`\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "👾 [CCurrency\\_bot](https://t\\.me/RookiesCurrency\\_bot) \\| "
            "🌐 [Канал](https://t\\.me/rookie\\_storie)"
        )

    return (
        "👋 *Welcome to CCurrency\\!*\n"
        "_Live crypto rates right in Telegram_\n\n"

        "━━━━━━━━━━━━━━━━━━━━━━\n\n"

        "📖 *How to use the bot*\n\n"

        "💱 *Token → USDT / USDC*\n"
        "Send an amount with a ticker — the bot shows the value in stablecoins\\.\n"
        "Examples: `0.01 BTC` \\| `0.5 ETH` \\| `BTC 0.001`\n\n"

        "🔄 *USDT / USDC → Token*\n"
        "Send an amount and ticker with a dash — the bot calculates how many coins you get\\.\n"
        "Examples: `100-BTC` \\| `500-ETH` \\| `1000-SOL`\n\n"

        "📊 *Token info*\n"
        "Send just a ticker — the bot shows the price, Market Cap and FDV\\.\n"
        "Examples: `BTC` \\| `ETH` \\| `SOL` \\| `TON`\n\n"

        "━━━━━━━━━━━━━━━━━━━━━━\n\n"

        "ℹ️ *Good to know*\n"
        "• All tokens from [CoinMarketCap](https://coinmarketcap\\.com) are supported\n"
        "• Prices update in real time\n"
        "• Both comma and dot work: `0,5` and `0.5`\n\n"

        "━━━━━━━━━━━━━━━━━━━━━━\n\n"

        "👾 [CCurrency\\_bot](https://t\\.me/RookiesCurrency\\_bot) \\| "
        "🌐 [Channel](https://t\\.me/rookie\\_storie)"
    )
