"""Dash Dash - Main Entry Point"""

import pygame
import sys
from library.config_manager import ConfigManager
from gui.screens.main_menu import MainMenu
from gui.screens.settings_menu import SettingsMenu


class Game:
    """Main game application."""
    
    def __init__(self):
        pygame.init()
        self.config = ConfigManager()
        self.screen = pygame.display.set_mode(self.config.resolution)
        pygame.display.set_caption(f"{self.config.get('game.name')} v{self.config.get('game.version')}")
        self.running = True
        self.clock = pygame.time.Clock()
        self.current_screen = None
        self.screens = {}
        self._init_screens()
        self._change_screen('main_menu')
    
    def _init_screens(self):
        main_callbacks = {
            'singleplayer': self._start_singleplayer,
            'multiplayer': self._show_multiplayer,
            'settings': lambda: self._change_screen('settings'),
            'quit': self._quit_game
        }
        
        self.screens['main_menu'] = MainMenu(self.screen, self.config, main_callbacks)
        self.screens['settings'] = SettingsMenu(self.screen, self.config, lambda: self._change_screen('main_menu'))
    
    def _change_screen(self, screen_name):
        if screen_name not in self.screens:
            print(f"Warning: Screen '{screen_name}' not found!")
            return
        if self.current_screen:
            self.current_screen.on_exit()
        self.current_screen = self.screens[screen_name]
        self.current_screen.on_enter()
    
    def _start_singleplayer(self):
        print("Starting Singleplayer...")
        print(f"Speed: {self.config.singleplayer_speed}, Username: {self.config.username}")
    
    def _show_multiplayer(self):
        print("Multiplayer not implemented yet")
    
    def _quit_game(self):
        self.running = False
    
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.current_screen:
                    self.current_screen.handle_event(event)
            if self.current_screen:
                self.current_screen.update(dt)
                self.current_screen.draw()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
