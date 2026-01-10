"""Input validation functions."""

import re
from config.defaults import CONSTRAINTS


def validate_username(username):
    if not username or not isinstance(username, str):
        return False
    username = username.strip()
    c = CONSTRAINTS['username']
    if len(username) < c['min_length'] or len(username) > c['max_length']:
        return False
    return bool(re.match(c['pattern'], username))


def validate_ip(ip):
    if not ip or not isinstance(ip, str):
        return False
    parts = ip.strip().split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not (0 <= int(part) <= 255):
            return False
    return True


def validate_port(port):
    try:
        p = int(port)
        c = CONSTRAINTS['server_port']
        return c['min'] <= p <= c['max']
    except:
        return False
