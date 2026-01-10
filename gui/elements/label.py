"""Button UI Element."""

import pygame


class Label:
    def __init__(self, text, rect, font_size=24):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.font = pygame.font.SysFont(None, font_size)
        self.enabled = False
    
    def draw(self, surface, theme):
        color = (100, 100, 100)
        # color = theme.get('label_color', (100, 100, 100))
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        text_surf = self.font.render(self.text, True, theme.get('text_color', (255, 255, 255)))
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))
    
    def handle_event(self, event):
        if not self.enabled:
            return
