"""
Network Client
Handles connection to game server and data synchronization.
"""

import socket
import threading
import json
import time


class NetworkClient:
    """Manages client-server communication."""
    
    def __init__(self):
        self.socket = None
        self.connected = False
        self.running = False
        self.players = {}
        self.player_name = "Player"
        self.client_id = None  # Store client ID
        self.lock = threading.Lock()
        self.receive_thread = None
        self.connection_error = None
    
    def connect(self, host, port, username, client_id):
        """
        Connect to game server.
        
        Args:
            host: Server IP address
            port: Server port
            username: Player name
            client_id: Unique client identifier
            
        Returns:
            tuple: (success: bool, error_message: str or None)
        """
        try:
            # Close existing connection if any
            if self.socket:
                self.disconnect()
            
            # Create new socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)  # 5 second timeout for connection
            
            # Try to connect
            print(f"Connecting to {host}:{port}...")
            self.socket.connect((host, port))
            self.socket.settimeout(None)  # Remove timeout after connection
            
            self.connected = True
            self.running = True
            self.player_name = username
            self.client_id = client_id
            self.connection_error = None
            
            # Send initial handshake with client_id
            initial_state = {
                "movement": 0,
                "name": username,
                "client_id": client_id
            }
            self.socket.sendall(json.dumps(initial_state).encode())
            
            # Wait for response
            data = self.socket.recv(4096)
            if data:
                response = json.loads(data.decode())
                # Check for error (duplicate client_id)
                if isinstance(response, dict) and "error" in response:
                    if response["error"] == "CLIENT_ALREADY_CONNECTED":
                        self.socket.close()
                        self.connected = False
                        error_msg = "This client is already connected to the server"
                        print(f"Connection failed: {error_msg}")
                        return (False, error_msg)
                
                # Success - store initial player data
                with self.lock:
                    self.players = response
            
            # Start receive thread
            self.receive_thread = threading.Thread(target=self._receive_data, daemon=True)
            self.receive_thread.start()
            
            print(f"Connected to server at {host}:{port}")
            return (True, None)
            
        except socket.timeout:
            self.connected = False
            error_msg = "Connection timeout - server not responding"
            print(f"Connection failed: {error_msg}")
            return (False, error_msg)
            
        except ConnectionRefusedError:
            self.connected = False
            error_msg = "Connection refused - server not running"
            print(f"Connection failed: {error_msg}")
            return (False, error_msg)
            
        except Exception as e:
            self.connected = False
            error_msg = f"Connection error: {str(e)}"
            print(f"Connection failed: {error_msg}")
            return (False, error_msg)
    
    def disconnect(self):
        """Disconnect from server."""
        print("Disconnecting from server...")
        self.running = False
        self.connected = False
        
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        
        # Wait for receive thread to finish
        if self.receive_thread and self.receive_thread.is_alive():
            self.receive_thread.join(timeout=1)
        
        with self.lock:
            self.players = {}
        
        print("Disconnected")
    
    def _receive_data(self):
        """Background thread to receive game state from server."""
        while self.running and self.connected:
            try:
                data = self.socket.recv(4096)
                if not data:
                    print("Server closed connection")
                    self.connected = False
                    self.connection_error = "Server closed connection"
                    break
                
                # Deserialize player data
                with self.lock:
                    self.players = json.loads(data.decode())
                    
            except ConnectionResetError:
                print("Connection reset by server")
                self.connected = False
                self.connection_error = "Connection lost"
                break
                
            except Exception as e:
                if self.running:  # Only log if not intentionally disconnecting
                    print(f"Receive error: {e}")
                    self.connected = False
                    self.connection_error = f"Network error: {str(e)}"
                break
        
        print("Receive thread stopped")
    
    def send_input(self, movement_direction):
        """
        Send player input to server.
        
        Args:
            movement_direction: int (bitwise flags) representing movement direction
                0 = no movement
                1 = up
                2 = down
                4 = left
                8 = right
                5 = up-left (1 | 4)
                9 = up-right (1 | 8)
                6 = down-left (2 | 4)
                10 = down-right (2 | 8)
            
        Returns:
            bool: True if sent successfully
        """
        if not self.connected or not self.socket:
            return False
        
        try:
            # Create input state with movement, name, and client_id
            input_state = {
                "movement": movement_direction,
                "name": self.player_name,
                "client_id": self.client_id
            }
            
            # Serialize and send

            data = json.dumps(input_state).encode()
            self.socket.sendall(data)
            return True
            
        except Exception as e:
            print(f"Send error: {e}")
            self.connected = False
            self.connection_error = "Failed to send data"
            return False
    
    def get_players(self):
        """
        Get current player positions.
        
        Returns:
            dict: {player_id: {"x": x, "y": y, "name": name}}
        """
        with self.lock:
            return self.players.copy()
    
    def is_connected(self):
        """Check if connected to server."""
        return self.connected
    
    def get_error(self):
        """Get last connection error message."""
        return self.connection_error
