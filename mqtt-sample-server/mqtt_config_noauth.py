import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

BROKER_CONFIG = {
    "listeners": {
        "default": {
            "type": "tcp",
            "bind": "0.0.0.0:9883",
            "max_connections": 100,
        },
    },
    "timeout_disconnect_delay": 2,
    # Allow anonymous connections (no username/password required)
    "plugins": {
        "amqtt.plugins.authentication.AnonymousAuthPlugin": {},
    },
}
