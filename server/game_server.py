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

# Game state
players = {}         # {player_id: {"x": x, "y": y, "name": name, "client_id": client_id}}
client_ids = set()   # Set of connected client IDs
player_id_counter = 1
lock = threading.Lock()

# Server config (will be initialized in main)
server_config = None


def handle_client(conn, addr, player_id):
    """
    Handle a single client connection.
    
    Args:
        conn: socket connection
        addr: client address
        player_id: unique player identifier
    """
    global players, client_ids
    
    print(f"[NEW CONNECTION] Player {player_id} connected from {addr}")
    
    # Wait for first message to get client_id
    try:
        data = conn.recv(1024)
        if not data:
            print(f"[ERROR] Player {player_id} disconnected before sending client_id")
            conn.close()
            return
        
        input_state = json.loads(data.decode())
        client_id = input_state.get("client_id")
        
        # Check if client_id already connected
        with lock:
            if client_id and client_id in client_ids:
                print(f"[REJECTED] Player {player_id} - Client ID already connected: {client_id}")
                # Send error message
                error_response = {"error": "CLIENT_ALREADY_CONNECTED"}
                conn.sendall(json.dumps(error_response).encode())
                conn.close()
                return
            
            # Register client_id
            if client_id:
                client_ids.add(client_id)
            
            # Initialize player at spawn point
            players[player_id] = {
                "x": server_config.spawn_x,
                "y": server_config.spawn_y,
                "name": input_state.get("name", f"Player{player_id}"),
                "client_id": client_id
            }
        
        # Send initial game state
        with lock:
            conn.sendall(json.dumps(players).encode())
        
        print(f"[REGISTERED] Player {player_id} - Name: {players[player_id]['name']}, Client ID: {client_id}")
        
    except Exception as e:
        print(f"[ERROR] Player {player_id} handshake failed: {e}")
        conn.close()
        return
    
    try:
        while True:
            # Receive input from client
            data = conn.recv(1024)
            if not data:
                break
            
            # Deserialize input state
            input_state = json.loads(data.decode())
            # Update player based on movement direction (bitwise flags)
            with lock:
                if player_id in players:
                    movement = input_state.get("movement", MOVE_NONE)
                    
                    # Calculate movement based on bitwise flags
                    dx = 0
                    dy = 0
                    
                    # Check vertical movement
                    if movement & MOVE_UP:
                        dy -= 1
                    if movement & MOVE_DOWN:
                        dy += 1
                    if movement & MOVE_LEFT:
                        dx -= 1
                    if movement & MOVE_RIGHT:
                        dx += 1
                    
                    # Apply speed (use diagonal speed if moving diagonally)
                    if dx != 0 and dy != 0:
                        # Diagonal movement
                        speed = PLAYER_SPEED_DIAGONAL
                    else:
                        # Straight movement
                        speed = server_config.player_speed
                    
                    players[player_id]["x"] += dx * speed
                    players[player_id]["y"] += dy * speed
                    
                    # Update player name if provided
                    if input_state.get("name"):
                        players[player_id]["name"] = input_state["name"]
            
            # Send all player positions back to client
            with lock:
                conn.sendall(json.dumps(players).encode())
    
    except ConnectionResetError:
        print(f"[CONNECTION RESET] Player {player_id} connection reset")
    except Exception as e:
        print(f"[ERROR] Player {player_id}: {e}")
    finally:
        # Remove player and client_id
        with lock:
            if player_id in players:
                client_id = players[player_id].get("client_id")
                if client_id:
                    client_ids.discard(client_id)
                del players[player_id]
        
        conn.close()
        print(f"[DISCONNECTED] Player {player_id} disconnected")
        print(f"[ACTIVE PLAYERS] {len(players)} player(s) remaining")


def start_server():
    """Start the game server."""
    global player_id_counter, server_config
    
    # Load configuration
    server_config = ServerConfig()
    server_config.parse_args()
    
    # Create socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind and listen
    try:
        server.bind((server_config.host, server_config.port))
        server.listen()
    except OSError as e:
        print(f"[ERROR] Failed to bind to {server_config.host}:{server_config.port}")
        print(f"[ERROR] {e}")
        print("[TIP] Port might be in use. Try a different port with: python game_server.py -p <port>")
        return
    
    print("=" * 70)
    print(f"[STARTED] Dash Dash Game Server")
    print("=" * 70)
    print(f"  Host: {server_config.host}")
    print(f"  Port: {server_config.port}")
    print(f"  Max Players: {server_config.max_players}")
    print(f"  Config: {ServerConfig.CONFIG_FILE}")
    print("=" * 70)
    print("Waiting for connections...")
    print()
    
    try:
        while True:
            # Accept new connection
            conn, addr = server.accept()
            
            # Check max players
            with lock:
                if len(players) >= server_config.max_players:
                    print(f"[REJECTED] Connection from {addr} - Server full ({server_config.max_players}/{server_config.max_players})")
                    conn.close()
                    continue
                
                # Assign player ID
                player_id = player_id_counter
                player_id_counter += 1
            
            # Start thread to handle this client
            thread = threading.Thread(
                target=handle_client,
                args=(conn, addr, player_id),
                daemon=True
            )
            thread.start()
            
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1} / {server_config.max_players}")
    
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server shutting down...")
    finally:
        server.close()
        print("[STOPPED] Server stopped")


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
    
    start_server()
