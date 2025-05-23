from utils.services.formatting import escape_md

def get_welcome_message() -> str:
    body = (
        "*👋 Добро пожаловать в CCurrency - by ROOKIE!*\n\n"
        "*Функционал | Пример запроса*:\n"
        "— Конвертация токена в USDT/USDC. | `0.00013 BTC`\n"
        "— Конвертация USDT/USDC в токен. | `123—ETH`\n"
        "— Информация о токене (Цена, Market Cap, FDV). | `ETH`\n\n"
        "*UPD-23.05*:\n"
        "— Обработка ошибок при неправильном вводе.\n"
        "— Конвертация из `USDT/USDC`, где `123` - сумма в `USDT/USDC`.\n"
        "— Кнопка `Меню` с командой `/start`.\n"
    )

    return escape_md(body)