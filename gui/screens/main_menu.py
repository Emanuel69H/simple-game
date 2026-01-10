"""Main Menu Screen."""

import pygame
from gui.screens.base_screen import BaseScreen
from gui.elements.button import Button


class MainMenu(BaseScreen):
    def __init__(self, screen, config, callbacks):
        super().__init__(screen, config)
        self.callbacks = callbacks
        self._build_ui()
    
    def _build_ui(self):
        w, h = self.config.resolution
        bw, bh = 250, 50
        cx = w // 2
        
        data = [
            ("Single Player", 0.35, self.callbacks.get('singleplayer')),
            ("Multiplayer", 0.47, self.callbacks.get('multiplayer')),
            ("Settings", 0.59, self.callbacks.get('settings')),
            ("Quit", 0.75, self.callbacks.get('quit'))
        ]
        
        for txt, yr, cb in data:
            y = int(h * yr)
            rect = pygame.Rect(cx - bw // 2, y - bh // 2, bw, bh)
            self.add_button(Button(txt, rect, cb, 28))
    
    def draw(self):
        super().draw()
        font = pygame.font.SysFont(None, 72, bold=True)
        title = font.render("DASH DASH", True, self.config.text_color)
        self.screen.blit(title, title.get_rect(center=(self.config.resolution[0] // 2, 100)))
        
        vfont = pygame.font.SysFont(None, 20)
        ver = vfont.render(f"v{self.config.get('game.version')}", True, (150, 150, 150))
        self.screen.blit(ver, ver.get_rect(bottomright=(self.config.resolution[0] - 10, self.config.resolution[1] - 10)))
        pygame.display.flip()
