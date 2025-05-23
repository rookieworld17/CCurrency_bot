import re

def clean_text(text: str) -> str:
    text = text.strip().replace('$', '')
    text = re.sub(r'(?<=\d),(?=\d)', '.', text)
    text = re.sub(r'[–—−]', '-', text)
    text = re.sub(r'-{2,}', '-', text)
    return text

def parce_input(text: str):
    text = clean_text(text)

    if '-' in text:
        parts = text.split('-', 1)
        if len(parts) != 2:
            return None, None, 'reverse_invalid'
        amount, symbol = parts[0].strip(), parts[1].strip().upper()
        if not amount.replace('.', '', 1).isdigit():
            return None, None, 'reverse_invalid'
        return amount, symbol, 'reverse'

    compact_match_1 = re.match(r'^([A-Za-z]+)([\d.]+)$', text)
    compact_match_2 = re.match(r'^([\d.]+)([A-Za-z]+)$', text)
    spaced_match = re.match(r'^([A-Za-z]+)\s+([\d.]+)$', text) or \
                   re.match(r'^([\d.]+)\s+([A-Za-z]+)$', text)

    match = compact_match_1 or compact_match_2 or spaced_match

    if match:
        part1, part2 = match.groups()

        if re.fullmatch(r'[\d.]+', part1):
            return part1, part2.upper(), 'forward'
        else:
            return part2, part1.upper(), 'forward'

    return None, text.strip().upper(), 'info'


def format_price(number: float) -> str:
    abs_number = abs(number)

    if abs_number >= 1_000_000_000_000:
        return f"{number / 1_000_000_000_000:.2f}T"
    elif abs_number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.2f}B"
    elif abs_number >= 1_000_000:
        return f"{number / 1_000_000:.2f}M"
    elif abs_number >= 1_000:
        return f"{number:,.2f}"
    elif abs_number >= 1:
        return f"{number:,.2f}"
    elif abs_number >= 0.01:
        return f"{number:,.4f}"
    elif abs_number >= 0.000001:
        return f"{number:,.8f}".rstrip("0").rstrip(".")
    else:
        return f"{number:.10f}".rstrip("0").rstrip(".")


def escape_md(text: str) -> str:
    escape_chars = r'_[]()~>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)