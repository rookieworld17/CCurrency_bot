import time, os
from dotenv import load_dotenv

load_dotenv()

SUGGESTION_COOLDOWN = int(os.getenv('SUGGESTION_COOLDOWN', 3600))

_pending: set = set()
_last_sent: dict = {}


def is_pending(user_id: int) -> bool:
    return user_id in _pending


def set_pending(user_id: int):
    _pending.add(user_id)


def clear_pending(user_id: int):
    _pending.discard(user_id)


def get_remaining_cooldown(user_id: int) -> float:
    last = _last_sent.get(user_id)
    if last is None:
        return 0
    remaining = SUGGESTION_COOLDOWN - (time.time() - last)
    return remaining if remaining > 0 else 0


def record_submission(user_id: int):
    _last_sent[user_id] = time.time()


def format_remaining(seconds: float) -> str:
    s = int(seconds)
    if s >= 3600:
        h, remainder = divmod(s, 3600)
        m = remainder // 60
        return f"{h}h {m}m" if m else f"{h}h"
    if s >= 60:
        m, sec = divmod(s, 60)
        return f"{m}m {sec}s" if sec else f"{m}m"
    return f"{s}s"
