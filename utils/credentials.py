from typing import Tuple
from fake_env import USERS

def get_credentials(user_key: str) -> Tuple[str, str]:
    key = user_key.upper()

    if key not in USERS:
        print('User is missing')

    user_cfg = USERS[key]

    username = user_cfg.get("username")
    password = user_cfg.get("password")

    return username, password
