"""Multiplayer Menu Screen."""

import pygame
from gui.screens.base_screen import BaseScreen
from gui.elements.button import Button
from gui.elements.label import Label
from library.connect import start_connection


class MultiplayerMenu(BaseScreen):
    def __init__(self, screen, config, callbacks):
        super().__init__(screen, config)
        self.callbacks = callbacks
        self._build_ui()
    
    def _build_ui(self):
        w, h = self.config.resolution
        # self.add_button(Button("Cancel", pygame.Rect(20, 20, 100, 35), self.callbacks, 24))
        bw, bh = 250, 50
        cx = w // 2
        
        labels = [
            ("Status", 0.35),
        ]

        data = [
            # ("Status", 0.35, self.callbacks.get('main_menu'),False),
            ("Join Game", 0.47, None,False),
            ("Host Game", 0.59, None,False),
            ("Connect to server", 0.71, start_connection,True),
            ("Back", 0.9, self.callbacks.get('main_menu'),True),
        #     ("Settings", 0.59, self.callbacks.get('settings')),
        #     ("Quit", 0.75, self.callbacks.get('quit'))
        ]
        # self._draw_button(self.connect_btn_rect, "Connect to Server", mouse_pos, active=True)

        for txt, yr in labels:
            y = int(h * yr)
            rect = pygame.Rect(cx - bw // 2, y - bh // 2, bw, bh)
            self.add_label(Label(txt, rect))

        
        for txt, yr, cb, ed in data:
            y = int(h * yr)
            rect = pygame.Rect(cx - bw // 2, y - bh // 2, bw, bh)
            self.add_button(Button(txt, rect, cb, 28, ed))
    
    def draw(self):
        super().draw()
        font = pygame.font.SysFont(None, 72, bold=True)
        title = font.render("DASH DASH", True, self.config.text_color)
        self.screen.blit(title, title.get_rect(center=(self.config.resolution[0] // 2, 100)))
        
        vfont = pygame.font.SysFont(None, 20)
        ver = vfont.render(f"v{self.config.get('game.version')}", True, (150, 150, 150))
        self.screen.blit(ver, ver.get_rect(bottomright=(self.config.resolution[0] - 10, self.config.resolution[1] - 10)))
        pygame.display.flip()
