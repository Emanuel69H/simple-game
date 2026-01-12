"""
Server Configuration Manager
Handles server config file and command-line arguments.
"""

import yaml
import argparse
from pathlib import Path


DEFAULT_SERVER_CONFIG = {
    "host": "0.0.0.0",      # Listen on all interfaces
    "port": 50000,
    "max_players": 8,
    "player_speed": 5,
    "spawn_x": 400,
    "spawn_y": 300
}


class ServerConfig:
    """Manages server configuration."""
    
    CONFIG_FILE = Path("server") / "server_config.yaml"
    
    def __init__(self):
        self.config = {}
        self.load()
    
    def load(self):
        """Load config from file or create default."""
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    loaded = yaml.safe_load(f)
                    if loaded:
                        self.config = {**DEFAULT_SERVER_CONFIG, **loaded}
                    else:
                        self.config = DEFAULT_SERVER_CONFIG.copy()
                        self.save()
            except Exception as e:
                print(f"[WARNING] Error loading config: {e}")
                self.config = DEFAULT_SERVER_CONFIG.copy()
                self.save()
        else:
            print("[INFO] Config file not found, creating default...")
            self.config = DEFAULT_SERVER_CONFIG.copy()
            self.save()
    
    def save(self):
        """Save current config to file."""
        try:
            # Ensure directory exists
            self.CONFIG_FILE.parent.mkdir(exist_ok=True)
            
            with open(self.CONFIG_FILE, 'w') as f:
                yaml.safe_dump(self.config, f, default_flow_style=False)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save config: {e}")
            return False
    
    def parse_args(self):
        """Parse command-line arguments and override config."""
        parser = argparse.ArgumentParser(description="Dash Dash Game Server")
        parser.add_argument(
            '-H', '--host',
            type=str,
            help=f"Host address (default: {self.config['host']})"
        )
        parser.add_argument(
            '-p', '--port',
            type=int,
            help=f"Port number (default: {self.config['port']})"
        )
        parser.add_argument(
            '-m', '--max-players',
            type=int,
            help=f"Maximum players (default: {self.config['max_players']})"
        )
        parser.add_argument(
            '--save',
            action='store_true',
            help="Save command-line arguments to config file"
        )
        
        args = parser.parse_args()
        
        # Override config with command-line args
        if args.host:
            self.config['host'] = args.host
        if args.port:
            self.config['port'] = args.port
        if args.max_players:
            self.config['max_players'] = args.max_players
        
        # Save if requested
        if args.save:
            print("[INFO] Saving configuration...")
            self.save()
            print(f"[INFO] Configuration saved to {self.CONFIG_FILE}")
    
    @property
    def host(self):
        return self.config['host']
    
    @property
    def port(self):
        return self.config['port']
    
    @property
    def max_players(self):
        return self.config['max_players']
    
    @property
    def player_speed(self):
        return self.config['player_speed']
    
    @property
    def spawn_x(self):
        return self.config['spawn_x']
    
    @property
    def spawn_y(self):
        return self.config['spawn_y']
