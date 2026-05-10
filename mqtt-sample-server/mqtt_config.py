import os
from pathlib import Path

from passlib.apps import custom_app_context as pwd_context

BASE_DIR = Path(__file__).parent
PASSWORD_FILE = BASE_DIR / "passwords.txt"

BROKER_CONFIG = {
    "listeners": {
        "default": {
            "type": "tcp",
            "bind": "0.0.0.0:9883",
            "max_connections": 100,
        },
    },
    "timeout_disconnect_delay": 2,
    "plugins": {
        "amqtt.plugins.authentication.FileAuthPlugin": {
            "password_file": str(PASSWORD_FILE),
        },
    },
}

DEFAULT_USERS = {
    "admin": "admin123",
    "user": "user123",
}


def generate_password_file():
    if PASSWORD_FILE.exists():
        return

    with open(PASSWORD_FILE, "w", encoding="utf-8") as f:
        for username, password in DEFAULT_USERS.items():
            pwd_hash = pwd_context.hash(password)
            f.write(f"{username}:{pwd_hash}\n")

    print(f"密码文件已生成: {PASSWORD_FILE}")
    for username in DEFAULT_USERS:
        print(f"  用户: {username}")


if __name__ == "__main__":
    generate_password_file()
