"""Settings Menu Screen."""

import pygame
from gui.screens.base_screen import BaseScreen
from gui.elements.button import Button
from gui.elements.text_input import TextInput


class SettingsMenu(BaseScreen):
    def __init__(self, screen, config, callbacks):
        super().__init__(screen, config)
        self.callback = callbacks.get('main_menu')
        self.scroll_y = 0
        self.input_map = {}
        self._build_ui()
    
    def _build_ui(self):
        w, h = self.config.resolution
        self.add_button(Button("Cancel", pygame.Rect(20, 20, 100, 35), self.callback, 24))
        self.add_button(Button("Save", pygame.Rect(w - 120, 20, 100, 35), self._save, 24))
        
        sections = [
            {'title': 'General', 'items': [{'key': 'username', 'label': 'Username', 'val': self.config.username, 'max': 16}]},
            {'title': 'Singleplayer', 'items': [{'key': 'sp_speed', 'label': 'Speed (1-100)', 'val': self.config.singleplayer_speed, 'max': 3}]},
            {'title': 'Multiplayer', 'items': [
                {'key': 'lobby_name', 'label': 'Lobby Name', 'val': self.config.lobby_name, 'max': 32},
                {'key': 'max_players', 'label': 'Max Players (2-8)', 'val': self.config.max_players, 'max': 1},
                {'key': 'mp_speed', 'label': 'Speed (1-100)', 'val': self.config.multiplayer_speed, 'max': 3}
            ]},
            {'title': 'Server', 'items': [
                {'key': 'server_ip', 'label': 'IP', 'val': self.config.server_ip, 'max': 15},
                {'key': 'server_port', 'label': 'Port', 'val': self.config.server_port, 'max': 5}
            ]}
        ]
        
        self.sections = []
        y = 100
        iw = 250
        for sec in sections:
            elems = []
            iy = y + 65
            for item in sec['items']:
                inp = TextInput(pygame.Rect(w // 2 - iw // 2, iy, iw, 35), str(item['val']), item['max'])
                self.add_input(inp)
                self.input_map[item['key']] = inp
                elems.append({'label': item['label'], 'input': inp, 'y': iy})
                iy += 45
            self.sections.append({'rect': pygame.Rect(50, y, w - 100, 40 + len(sec['items']) * 45 + 30), 'title': sec['title'], 'elements': elems})
            y += 40 + len(sec['items']) * 45 + 50
    
    def _save(self):
        try:
            self.config.username = self.input_map['username'].get_text()
            self.config.server_ip = self.input_map['server_ip'].get_text()
            self.config.server_port = self.input_map['server_port'].get_text()
            self.config.singleplayer_speed = self.input_map['sp_speed'].get_text()
            self.config.multiplayer_speed = self.input_map['mp_speed'].get_text()
            self.config.lobby_name = self.input_map['lobby_name'].get_text()
            self.config.max_players = self.input_map['max_players'].get_text()
            self.config.save()
            print("Settings saved!")
            if self.callback:
                self.callback()
        except ValueError as e:
            print(f"Error: {e}")
        
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scroll_y = min(0, self.scroll_y + 30)
            elif event.button == 5:
                self.scroll_y -= 30
        for sec in self.sections:
            for el in sec['elements']:
                el['input'].rect.y = el['y'] + self.scroll_y
        super().handle_event(event)
    
    def draw(self):
        super().draw()
        self.screen.fill(self.config.bg_color)
        theme = {'button_color': self.config.button_color, 'button_hover': self.config.button_hover,
                 'text_color': self.config.text_color, 'input_border': self.config.input_border,
                 'input_active': self.config.input_active}
        
        ft = pygame.font.SysFont(None, 28, bold=True)
        fl = pygame.font.SysFont(None, 22)
        
        for sec in self.sections:
            r = sec['rect'].move(0, self.scroll_y)
            if r.bottom < 70 or r.top > self.config.resolution[1]:
                continue
            pygame.draw.rect(self.screen, (50, 50, 50), r, border_radius=8)
            t = ft.render(sec['title'], True, self.config.text_color)
            self.screen.blit(t, t.get_rect(centerx=self.config.resolution[0] // 2, top=r.y + 10))
            for el in sec['elements']:
                if el['input'].rect.bottom < 70 or el['input'].rect.top > self.config.resolution[1]:
                    continue
                lbl = fl.render(el['label'], True, self.config.text_color)
                self.screen.blit(lbl, lbl.get_rect(midright=(el['input'].rect.left - 20, el['input'].rect.centery)))
                el['input'].draw(self.screen, theme)
        
        for b in self.buttons:
            b.draw(self.screen, theme)
        vfont = pygame.font.SysFont(None, 20)
        ver = vfont.render(f"v{self.config.get('game.version')}", True, (150, 150, 150))
        self.screen.blit(ver, ver.get_rect(bottomright=(self.config.resolution[0] - 10, self.config.resolution[1] - 10)))
        pygame.display.flip()
