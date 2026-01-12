"""
Multiplayer Menu Screen
Connect to server, host or join games.
"""

import pygame
from gui.screens.base_screen import BaseScreen
from gui.elements.button import Button
from gui.elements.label import Label
from game.multiplayer.client import NetworkClient


class MultiplayerMenu(BaseScreen):
    """Multiplayer menu with connection management."""
    
    def __init__(self, screen, config, callbacks):
        super().__init__(screen, config)
        self.callbacks = callbacks
        self.client = NetworkClient()
        
        # UI elements (will be populated in _build_ui)
        self.status_label = None
        self.connect_btn = None
        self.join_btn = None
        self.host_btn = None
        self.back_btn = None
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the UI elements."""
        w, h = self.config.resolution
        bw, bh = 250, 50
        cx = w // 2
        
        # Status label at top
        status_rect = pygame.Rect(cx - bw // 2, int(h * 0.35) - bh // 2, bw, bh)
        self.status_label = Label("Disconnected", status_rect, font_size=28)
        self.add_label(self.status_label)
        
        # Connect button
        connect_rect = pygame.Rect(cx - bw // 2, int(h * 0.47) - bh // 2, bw, bh)
        self.connect_btn = Button(
            "Connect to Server",
            connect_rect,
            lambda: self._connect_to_server(),
            font_size=28,
            enabled=True
        )
        self.add_button(self.connect_btn)
        
        # Join button (disabled initially)
        join_rect = pygame.Rect(cx - bw // 2, int(h * 0.59) - bh // 2, bw, bh)
        self.join_btn = Button(
            "Join Game",
            join_rect,
            lambda: self._join_game(),
            font_size=28,
            enabled=False
        )
        self.add_button(self.join_btn)
        
        # Host button (disabled initially)
        host_rect = pygame.Rect(cx - bw // 2, int(h * 0.71) - bh // 2, bw, bh)
        self.host_btn = Button(
            "Host Game",
            host_rect,
            lambda: self._host_game(),
            font_size=28,
            enabled=False
        )
        self.add_button(self.host_btn)
        
        # Back button
        back_rect = pygame.Rect(cx - bw // 2, int(h * 0.90) - bh // 2, bw, bh)
        self.back_btn = Button(
            "Back",
            back_rect,
            lambda: self._go_back(),
            font_size=28,
            enabled=True
        )
        self.add_button(self.back_btn)
    
    def _connect_to_server(self):
        """Attempt to connect to the server or disconnect."""
        # Check if already connected
        if self.client.is_connected():
            # Disconnect
            self._disconnect_from_server()
            return
        
        print("Attempting to connect to server...")
        
        # Update UI to show connecting state
        self.status_label.text = "Connecting..."
        self.connect_btn.enabled = False
        
        # Force a draw update to show "Connecting..."
        self.draw()
        
        # Get server info from config
        host = self.config.server_ip
        port = self.config.server_port
        username = self.config.username
        client_id = self.config.client_id
        
        print(f"Connecting to {host}:{port} as {username} (ID: {client_id})")
        
        # Try to connect
        success, error = self.client.connect(host, port, username, client_id)
        
        if success:
            # Connection successful
            self.status_label.text = "Connected"
            self.connect_btn.text = "Disconnect"
            self.connect_btn.enabled = True
            
            # Enable join/host buttons
            self.join_btn.enabled = True
            self.host_btn.enabled = True
            
            print("Connected successfully!")
        else:
            # Connection failed
            if "already connected" in error.lower():
                self.status_label.text = "Already Connected"
            else:
                self.status_label.text = "Connection Failed"
            self.connect_btn.enabled = True
            
            print(f"Connection failed: {error}")
    
    def _disconnect_from_server(self):
        """Disconnect from server."""
        print("Disconnecting...")
        
        self.client.disconnect()
        
        # Update UI
        self.status_label.text = "Disconnected"
        self.connect_btn.text = "Connect to Server"
        self.connect_btn.enabled = True
        
        # Disable join/host buttons
        self.join_btn.enabled = False
        self.host_btn.enabled = False
        
        print("Disconnected")
    
    def _join_game(self):
        """Join an existing game."""
        print("Joining game...")
        # TODO: Show lobby browser or join directly
        # For now, just start the game
        if self.callbacks.get('start_game'):
            self.callbacks['start_game'](self.client, is_host=False)
    
    def _host_game(self):
        """Host a new game."""
        print("Hosting game...")
        # TODO: Create lobby with settings
        # For now, just start the game as host
        if self.callbacks.get('start_game'):
            self.callbacks['start_game'](self.client, is_host=True)
    
    def _go_back(self):
        """Return to main menu."""
        # Disconnect if connected
        if self.client.is_connected():
            self.client.disconnect()
        
        # Go back to main menu
        if self.callbacks.get('main_menu'):
            self.callbacks['main_menu']()
    
    def update(self, dt):
        """Update connection status."""
        super().update(dt)
        
        # Check connection status and update UI
        if self.client.is_connected():
            # Connected - make sure UI reflects this
            if self.status_label.text != "Connected":
                self.status_label.text = "Connected"
                self.connect_btn.text = "Disconnect"
                self.connect_btn.enabled = True
                self.join_btn.enabled = True
                self.host_btn.enabled = True
        else:
            # Not connected - check if we were connected before
            if self.connect_btn.text == "Disconnect":
                # Connection was lost
                self.status_label.text = "Disconnected"
                self.connect_btn.text = "Connect to Server"
                self.connect_btn.enabled = True
                self.join_btn.enabled = False
                self.host_btn.enabled = False
                
                # Check for error message
                error = self.client.get_error()
                if error:
                    print(f"Connection error: {error}")
    
    def draw(self):
        """Draw the multiplayer menu."""
        super().draw()
        
        # Draw title
        font = pygame.font.SysFont(None, 72, bold=True)
        title = font.render("MULTIPLAYER", True, self.config.text_color)
        self.screen.blit(title, title.get_rect(center=(self.config.resolution[0] // 2, 100)))
        
        # Draw version
        vfont = pygame.font.SysFont(None, 20)
        ver = vfont.render(f"v{self.config.get('game.version')}", True, (150, 150, 150))
        self.screen.blit(ver, ver.get_rect(bottomright=(self.config.resolution[0] - 10, self.config.resolution[1] - 10)))
        
        # Draw server info
        info_font = pygame.font.SysFont(None, 18)
        server_info = info_font.render(
            f"Server: {self.config.server_ip}:{self.config.server_port} | {self.status_label.text}",
            True,
            (150, 150, 150)
        )
        self.screen.blit(server_info, (10, self.config.resolution[1] - 30))
        
        pygame.display.flip()
    
    def on_exit(self):
        """Called when leaving this screen."""
        # DON'T disconnect - keep connection alive for game!
        # Only disconnect if explicitly requested via Back button or Disconnect button
        pass
