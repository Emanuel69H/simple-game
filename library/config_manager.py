"""Configuration Manager."""

import yaml
import uuid
from pathlib import Path
from config.defaults import DEFAULT_CONFIG, CONSTRAINTS
from library.validators import validate_username, validate_ip, validate_port


class ConfigManager:
    CONFIG_DIR = Path("config")
    CONFIG_FILE = CONFIG_DIR / "settings.yaml"
    
    def __init__(self):
        self._config = {}
        self.CONFIG_DIR.mkdir(exist_ok=True)
        self.load()
    
    def load(self):
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    loaded = yaml.safe_load(f) or {}
                    self._config = self._merge(loaded)
            except:
                self._config = DEFAULT_CONFIG.copy()
                self.save()
        else:
            self._config = DEFAULT_CONFIG.copy()
            self.save()
        if not self.get("user.client_id"):
            self.set("user.client_id", str(uuid.uuid4()))
            self.save()
    
    def _merge(self, loaded):
        import copy
        merged = copy.deepcopy(DEFAULT_CONFIG)
        def deep_merge(base, update):
            for k, v in update.items():
                if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                    deep_merge(base[k], v)
                else:
                    base[k] = v
        deep_merge(merged, loaded)
        return merged
    
    def save(self):
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                yaml.safe_dump(self._config, f)
            return True
        except:
            return False
    
    def get(self, key, default=None):
        keys = key.split('.')
        val = self._config
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val
    
    def set(self, key, value):
        keys = key.split('.')
        cfg = self._config
        for k in keys[:-1]:
            if k not in cfg:
                cfg[k] = {}
            cfg = cfg[k]
        cfg[keys[-1]] = value
    
    @property
    def username(self):
        return self.get('user.username')
    
    @username.setter
    def username(self, v):
        if validate_username(v):
            self.set('user.username', v)
        else:
            raise ValueError("Invalid username")
    
    @property
    def server_ip(self):
        return self.get('server.ip')
    
    @server_ip.setter
    def server_ip(self, v):
        if validate_ip(v):
            self.set('server.ip', v)
        else:
            raise ValueError("Invalid IP")
    
    @property
    def server_port(self):
        return self.get('server.port')
    
    @server_port.setter
    def server_port(self, v):
        if validate_port(v):
            self.set('server.port', int(v))
        else:
            raise ValueError("Invalid port")
    
    @property
    def resolution(self):
        return tuple(self.get('display.resolution'))
    
    @property
    def client_id(self):
        return self.get('user.client_id')
    
    @property
    def bg_color(self):
        return tuple(self.get('theme.bg_color'))
    
    @property
    def button_color(self):
        return tuple(self.get('theme.button_color'))
    
    @property
    def button_hover(self):
        return tuple(self.get('theme.button_hover'))
    
    @property
    def text_color(self):
        return tuple(self.get('theme.text_color'))
    
    @property
    def input_border(self):
        return tuple(self.get('theme.input_border'))
    
    @property
    def input_active(self):
        return tuple(self.get('theme.input_active'))
    
    @property
    def singleplayer_speed(self):
        return self.get('singleplayer.speed')
    
    @singleplayer_speed.setter
    def singleplayer_speed(self, v):
        val = int(v)
        c = CONSTRAINTS['speed']
        if c['min'] <= val <= c['max']:
            self.set('singleplayer.speed', val)
        else:
            raise ValueError(f"Speed must be {c['min']}-{c['max']}")
    
    @property
    def multiplayer_speed(self):
        return self.get('multiplayer.speed')
    
    @multiplayer_speed.setter
    def multiplayer_speed(self, v):
        val = int(v)
        c = CONSTRAINTS['speed']
        if c['min'] <= val <= c['max']:
            self.set('multiplayer.speed', val)
        else:
            raise ValueError(f"Speed must be {c['min']}-{c['max']}")
    
    @property
    def lobby_name(self):
        return self.get('multiplayer.lobby_name')
    
    @lobby_name.setter
    def lobby_name(self, v):
        self.set('multiplayer.lobby_name', str(v))
    
    @property
    def max_players(self):
        return self.get('multiplayer.max_players')
    
    @max_players.setter
    def max_players(self, v):
        val = int(v)
        c = CONSTRAINTS['max_players']
        if c['min'] <= val <= c['max']:
            self.set('multiplayer.max_players', val)
        else:
            raise ValueError(f"Max players {c['min']}-{c['max']}")
