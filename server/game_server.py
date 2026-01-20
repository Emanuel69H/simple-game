"""
Game Server - Updated with Diagonal Movement and Client ID Validation
Manages multiplayer game sessions and synchronizes player positions.
"""

import socket
import threading
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from server.server_config import ServerConfig
from game.constants import *


class GameServer:
    def __init__(self):
        self.players = {}  # {player_id: {..., 'conn': conn}}
        self.client_ids = set()
        self.player_id_counter = 1
        self.lock = threading.Lock()
        self.server_config = ServerConfig()
        self.server_config.parse_args()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.server_config.host, self.server_config.port))
        self.server.listen()
        self.state_changed = threading.Event()
        self.running = True

    def start(self):
        print("=" * 70)
        print(f"[STARTED] Dash Dash Game Server")
        print("=" * 70)
        print(f"  Host: {self.server_config.host}")
        print(f"  Port: {self.server_config.port}")
        print(f"  Max Players: {self.server_config.max_players}")
        print(f"  Config: {ServerConfig.CONFIG_FILE}")
        print("=" * 70)
        print("Waiting for connections...")
        print()
        threading.Thread(target=self.connection_handler, daemon=True).start()
        threading.Thread(target=self.broadcaster, daemon=True).start()
        try:
            while self.running:
                threading.Event().wait(1)
        except KeyboardInterrupt:
            print("\n[SHUTDOWN] Server shutting down...")
            self.running = False
            self.server.close()
            print("[STOPPED] Server stopped")

    def connection_handler(self):
        while self.running:
            try:
                conn, addr = self.server.accept()
            except Exception:
                break
            with self.lock:
                if len(self.players) >= self.server_config.max_players:
                    print(f"[REJECTED] Connection from {addr} - Server full ({self.server_config.max_players}/{self.server_config.max_players})")
                    conn.close()
                    continue
                player_id = self.player_id_counter
                self.player_id_counter += 1
                self.players[player_id] = {"conn": conn, "addr": addr}
            threading.Thread(target=self.receiver, args=(conn, addr, player_id), daemon=True).start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1} / {self.server_config.max_players}")

    def receiver(self, conn, addr, player_id):
        print(f"[NEW CONNECTION] Player {player_id} connected from {addr}")
        try:
            data = conn.recv(1024)
            if not data:
                print(f"[ERROR] Player {player_id} disconnected before sending client_id")
                conn.close()
                return
            input_state = json.loads(data.decode())
            client_id = input_state.get("client_id")
            with self.lock:
                if client_id and client_id in self.client_ids:
                    print(f"[REJECTED] Player {player_id} - Client ID already connected: {client_id}")
                    error_response = {"error": "CLIENT_ALREADY_CONNECTED"}
                    conn.sendall(json.dumps(error_response).encode())
                    conn.close()
                    return
                if client_id:
                    self.client_ids.add(client_id)
                self.players[player_id].update({
                    "x": self.server_config.spawn_x,
                    "y": self.server_config.spawn_y,
                    "name": input_state.get("name", f"Player{player_id}"),
                    "client_id": client_id
                })
                # Only send serializable player info
                serializable_players = {
                    pid: {k: v for k, v in pdata.items() if k != "conn" and k != "addr"}
                    for pid, pdata in self.players.items()
                }
                conn.sendall(json.dumps(serializable_players).encode())
                print(f"[REGISTERED] Player {player_id} - Name: {self.players[player_id]['name']}, Client ID: {client_id}")
            while self.running:
                data = conn.recv(1024)
                if not data:
                    break
                input_state = json.loads(data.decode())
                with self.lock:
                    if player_id in self.players:
                        movement = input_state.get("movement", MOVE_NONE)
                        dx = dy = 0
                        if movement & MOVE_UP:
                            dy -= 1
                        if movement & MOVE_DOWN:
                            dy += 1
                        if movement & MOVE_LEFT:
                            dx -= 1
                        if movement & MOVE_RIGHT:
                            dx += 1
                        if dx != 0 and dy != 0:
                            speed = PLAYER_SPEED_DIAGONAL
                        else:
                            speed = self.server_config.player_speed
                        self.players[player_id]["x"] += dx * speed
                        self.players[player_id]["y"] += dy * speed
                        if input_state.get("name"):
                            self.players[player_id]["name"] = input_state["name"]
                        self.state_changed.set()
        except Exception as e:
            print(f"[ERROR] Player {player_id}: {e}")
        finally:
            with self.lock:
                if player_id in self.players:
                    client_id = self.players[player_id].get("client_id")
                    if client_id:
                        self.client_ids.discard(client_id)
                    try:
                        self.players[player_id]["conn"].close()
                    except Exception:
                        pass
                    del self.players[player_id]
            print(f"[DISCONNECTED] Player {player_id} disconnected")
            print(f"[ACTIVE PLAYERS] {len(self.players)} player(s) remaining")

    def broadcaster(self):
        last_state = None
        while self.running:
            self.state_changed.wait()
            with self.lock:
                # Only send serializable player info
                serializable_players = {
                    pid: {k: v for k, v in pdata.items() if k != "conn" and k != "addr"}
                    for pid, pdata in self.players.items()
                }
                state = json.dumps(serializable_players).encode()
                if state != last_state:
                    disconnected_pids = []
                    for pid, pdata in self.players.items():
                        conn_obj = pdata.get("conn")
                        if conn_obj:
                            try:
                                conn_obj.sendall(state)
                            except Exception as e:
                                print(f"[ERROR] Failed to send update to Player {pid}: {e}")
                                disconnected_pids.append(pid)
                    for pid in disconnected_pids:
                        if pid in self.players:
                            try:
                                self.players[pid]["conn"].close()
                            except Exception:
                                pass
                            del self.players[pid]
                    last_state = state
                self.state_changed.clear()


if __name__ == "__main__":
    print()
    print("╔═════════════════════════════════════════╗")
    print("║        DASH DASH - GAME SERVER          ║")
    print("╚═════════════════════════════════════════╝")
    print()
    print("Usage:")
    print("  python game_server.py                    # Use config/defaults")
    print("  python game_server.py -H 0.0.0.0 -p 5000 # Override settings")
    print("  python game_server.py -p 8080 --save     # Save to config")
    print()
    
    GameServer().start()
