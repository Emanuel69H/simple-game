"""
Game Screen - Updated with Play Area Border and Fixed Player List
The actual gameplay screen where players move around.
"""

import pygame
from gui.screens.base_screen import BaseScreen
from game.constants import *


class GameScreen(BaseScreen):
    """Main game screen with multiplayer support."""
    
    def __init__(self, screen, config, client, is_host, back_callback):
        """
        Initialize game screen.
        
        Args:
            screen: pygame display surface
            config: ConfigManager instance
            client: NetworkClient instance
            is_host: bool, True if this player is hosting
            back_callback: Function to call when exiting
        """
        super().__init__(screen, config)
        self.client = client
        self.is_host = is_host
        self.back_callback = back_callback
        
        # Fonts
        self.font_small = pygame.font.SysFont(None, 20)
        self.font_medium = pygame.font.SysFont(None, 24)
        self.font_title = pygame.font.SysFont(None, 36, bold=True)
        
        # Calculate play area
        screen_w, screen_h = self.config.resolution
        self.play_area = pygame.Rect(
            UI_SIDE_MARGIN,
            UI_TOP_HEIGHT,
            screen_w - 2 * UI_SIDE_MARGIN,
            screen_h - UI_TOP_HEIGHT - UI_BOTTOM_HEIGHT
        )
    
    def handle_event(self, event):
        """Handle input events."""
        super().handle_event(event)
        
        # ESC to exit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._exit_game()
    
    def update(self, dt):
        """Update game logic."""
        super().update(dt)
        
        # Check if still connected
        if not self.client.is_connected():
            print("Connection lost during game!")
            self._exit_game()
            return
        
        # Get keyboard input and convert to movement direction (bitwise flags)
        keys = pygame.key.get_pressed()
        movement = MOVE_NONE
        
        # Allow diagonal movement by combining flags
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            movement |= MOVE_UP
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            movement |= MOVE_DOWN
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            movement |= MOVE_LEFT
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            movement |= MOVE_RIGHT
            
        # Send movement to server
        self.client.send_input(movement)
    
    def draw(self):
        """Draw the game."""
        screen_w, screen_h = self.config.resolution
        
        # Fill background
        self.screen.fill(COLOR_BG)
        
        # Draw UI areas
        self._draw_ui_background()
        
        # Draw play area background and border
        self._draw_play_area_background()
        
        # Get all players from server
        players = self.client.get_players()
        
        # Draw all players (server handles wrapping now)
        self._draw_players(players)
        
        # Draw UI overlay
        self._draw_top_ui(players)
        self._draw_bottom_ui()
        
        pygame.display.flip()
    
    def _draw_ui_background(self):
        """Draw background for UI areas."""
        screen_w, screen_h = self.config.resolution
        
        # Top UI area
        top_rect = pygame.Rect(0, 0, screen_w, UI_TOP_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_UI_BG, top_rect)
        
        # Bottom UI area
        bottom_rect = pygame.Rect(0, screen_h - UI_BOTTOM_HEIGHT, screen_w, UI_BOTTOM_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_UI_BG, bottom_rect)
    
    def _draw_play_area_background(self):
        """Draw play area background with visible border."""
        # Play area background (slightly different color)
        pygame.draw.rect(self.screen, (40, 40, 40), self.play_area)
        
        # Draw border around play area
        border_color = (100, 100, 100)
        pygame.draw.rect(self.screen, border_color, self.play_area, 2)  # 2px border
    
    def _draw_players(self, players):
        """Draw all players (server handles wrapping)."""
        for player_id, player_data in players.items():
            x = player_data.get("x", 0)
            y = player_data.get("y", 0)
            name = player_data.get("name", f"Player{player_id}")
            
            # Determine color (own player is blue, others are orange)
            is_self = (name == self.config.username)
            color = COLOR_SELF if is_self else COLOR_OTHER
            
            # Draw player rectangle
            player_rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
            pygame.draw.rect(self.screen, color, player_rect)
            
            # Draw player name above rectangle (only if visible in play area)
            name_y = y - 10
            if name_y > self.play_area.top:
                name_surface = self.font_medium.render(name, True, COLOR_TEXT)
                name_rect = name_surface.get_rect(
                    center=(x + PLAYER_SIZE // 2, name_y)
                )
                self.screen.blit(name_surface, name_rect)
    
    def _draw_top_ui(self, players):
        """Draw top UI elements (title and player grid)."""
        # Draw title
        role_text = "HOST" if self.is_host else "CLIENT"
        title = self.font_title.render(f"DASH DASH - {role_text}", True, COLOR_TEXT)
        self.screen.blit(title, (UI_SIDE_MARGIN, 10))

        # Draw player list header
        y_offset = 50
        player_list_title = self.font_medium.render(f"Players ({len(players)}):", True, COLOR_TEXT)
        self.screen.blit(player_list_title, (UI_SIDE_MARGIN, y_offset))

        # Collect player info
        player_names = []
        for player_id, player_data in sorted(players.items()):
            name = player_data.get("name", f"Player{player_id}")
            is_self = (name == self.config.username)
            player_names.append({'name': name, 'is_self': is_self})

        # Grid layout parameters
        max_rows = 2
        max_cols = 4
        row_height = 18
        col_spacing = 120  # horizontal spacing between columns
        x_start = UI_SIDE_MARGIN + 10
        y_start = y_offset + 25

        for i, player_info in enumerate(player_names):
            row = i % max_rows
            col = i // max_rows
            if col >= max_cols:
                # More players than grid can display
                if i == max_rows * max_cols:
                    more_text = self.font_small.render(
                        f"... and {len(player_names) - max_rows * max_cols} more",
                        True,
                        COLOR_TEXT_DIM
                    )
                    self.screen.blit(more_text, (x_start, y_start + row * row_height))
                break

            x = x_start + col * col_spacing
            y = y_start + row * row_height

            display_name = f"• {player_info['name']}" + (" (You)" if player_info['is_self'] else "")
            color = COLOR_SELF if player_info['is_self'] else COLOR_TEXT_DIM
            name_surface = self.font_small.render(display_name, True, color)
            self.screen.blit(name_surface, (x, y))
    
    def _draw_bottom_ui(self):
        """Draw bottom UI elements (controls hint)."""
        screen_w, screen_h = self.config.resolution
        
        # Controls hint
        controls_text = self.font_small.render(
            "Controls: WASD / Arrow Keys to move  |  ESC to exit",
            True,
            COLOR_TEXT_DIM
        )
        controls_rect = controls_text.get_rect(
            center=(screen_w // 2, screen_h - UI_BOTTOM_HEIGHT // 2)
        )
        self.screen.blit(controls_text, controls_rect)
    
    def _exit_game(self):
        """Exit the game and return to menu."""
        print("Exiting game...")
        
        if self.back_callback:
            self.back_callback()
    
    def on_exit(self):
        """Called when leaving this screen."""
        print("Game screen exited")
