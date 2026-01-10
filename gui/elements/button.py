"""Button UI Element."""

import pygame


class Button:
    def __init__(self, text, rect, action=None, font_size=24):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.action = action
        self.font = pygame.font.SysFont(None, font_size)
        self.hover = False
        self.enabled = True
    
    def draw(self, surface, theme):
        if not self.enabled:
            color = (100, 100, 100)
        elif self.hover:
            color = theme.get('button_hover', (0, 200, 255))
        else:
            color = theme.get('button_color', (0, 150, 200))
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        text_surf = self.font.render(self.text, True, theme.get('text_color', (255, 255, 255)))
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))
    
    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()
