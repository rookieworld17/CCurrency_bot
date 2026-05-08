from dotenv import load_dotenv
from utils.services.formatting import format_price, escape_md
from utils.translations import STRINGS
import os, requests

load_dotenv()

url = os.getenv('COINMARKETCAP_URL_API')
headers = {'X-CMC_PRO_API_KEY': os.getenv('COINMARKETCAP_USER_API')}

def get_token_info(symbol, lang='EN'):
    s = STRINGS[lang]
    params = {'symbol': symbol.upper(), 'convert': 'USD'}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "status" in data and data["status"]["error_code"] != 0:
        return f"{s['cmc_error']}{data['status']['error_message']}"

    if symbol.upper() not in data['data']:
        return s['token_not_found_short']

    token_data = data['data'][symbol.upper()]
    quote = token_data.get('quote', {}).get('USD')

    if not quote:
        return f"{s['no_price']}{escape_md(symbol)}\\."

    price = format_price(quote.get('price', 0))
    market_cap = format_price(quote.get('market_cap', 0))
    fdv = format_price(quote.get('fully_diluted_market_cap', 0))
    name = token_data.get('name', symbol)

    return (
        f"*📊 {escape_md(name)} \\(${escape_md(symbol.upper())}\\)*\n\n"
        f"{s['price_label']} `${escape_md(price)}`\n"
        f"{s['mcap_label']} `${escape_md(market_cap)}`\n"
        f"{s['fdv_label']} `${escape_md(fdv)}`\n\n"
        f"{s['footer']}"
    )

def convert_currency(amount: float, symbol: str, intent: str = "forward", lang: str = 'EN') -> str:
    s = STRINGS[lang]
    symbol = symbol.upper()

    def get_price(symbol: str, convert_to: str):
        params = {'symbol': symbol, 'convert': convert_to}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get('data', {})
        return data[symbol]['quote'][convert_to]['price'] if symbol in data else None

    try:
        price_usdt = get_price(symbol, 'USDT')
        price_usdc = get_price(symbol, 'USDC')

        if price_usdt is None or price_usdc is None:
            return s['token_not_found_short']

        if intent == "forward":
            result_usdt = float(amount) * price_usdt
            result_usdc = float(amount) * price_usdc
            return (
                f"`{amount}` *${escape_md(symbol)}* *≈* `{escape_md(format_price(result_usdt))}` *$USDT*\n"
                f"`{amount}` *${escape_md(symbol)}* *≈* `{escape_md(format_price(result_usdc))}` *$USDC*\n\n"
                f"{s['footer']}"
            )
        elif intent == "reverse":
            result_token_usdt = float(amount) / price_usdt
            result_token_usdc = float(amount) / price_usdc
            return (
                f"`{amount}` *$USDT* *≈* `{escape_md(format_price(result_token_usdt))}` *${escape_md(symbol)}*\n"
                f"`{amount}` *$USDC* *≈* `{escape_md(format_price(result_token_usdc))}` *${escape_md(symbol)}*\n\n"
                f"{s['footer']}"
            )
        else:
            return s['wrong_direction']
    except Exception:
        return s['price_error']
