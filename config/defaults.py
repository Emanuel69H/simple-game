"""Default configuration values."""

DEFAULT_CONFIG = {
    "game": {"name": "Dash Dash", "version": "1.0.0"},
    "display": {"resolution": [800, 600], "fullscreen": False, "fps_limit": 60},
    "user": {"username": "Player", "language": "en", "client_id": None},
    "theme": {
        "bg_color": [30, 30, 30],
        "button_color": [0, 150, 200],
        "button_hover": [0, 200, 255],
        "button_disabled": [100, 100, 100],
        "label_color": [150, 150, 150],
        "text_color": [255, 255, 255],
        "input_border": [100, 100, 100],
        "input_active": [0, 200, 255]
    },
    "singleplayer": {"speed": 10, "difficulty": "medium"},
    "multiplayer": {"lobby_name": "My Lobby", "lobby_password": "", "max_players": 4, "speed": 10},
    "server": {"ip": "127.0.0.1", "port": 50000, "timeout": 5}
}
# 123.123.123.123
CONSTRAINTS = {
    "username": {"min_length": 1, "max_length": 16, "pattern": r"^[a-zA-Z0-9_-]+$"},
    "ip": {"min_length" :7 ,"max_length":15, "pattern": r"^(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)){3}$"},
    "server_port": {"min": 1024, "max": 65535},
    "speed": {"min": 1, "max": 100},
    "max_players": {"min": 2, "max": 8},
    "resolution": {"width_min": 640, "height_min": 480}
}
