"""Text Input UI Element."""

import pygame

class TextInput:
    def __init__(self, rect, default_text="", max_length=32, placeholder=""):
        self.rect = pygame.Rect(rect)
        self.text = default_text
        self.max_length = max_length
        self.placeholder = placeholder
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.font = pygame.font.SysFont(None, 22)
    
    def draw(self, surface, theme):
        border_color = theme.get('input_active' if self.active else 'input_border', (100, 100, 100))
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=3)
        
        if self.text:
            display, color = self.text, theme.get('text_color', (255, 255, 255))
        elif self.placeholder and not self.active:
            display, color = self.placeholder, (150, 150, 150)
        else:
            display, color = "", theme.get('text_color', (255, 255, 255))
        
        if display:
            text_surf = self.font.render(display, True, color)
            clip_rect = self.rect.inflate(-16, -4)
            surface.set_clip(clip_rect)
            surface.blit(text_surf, text_surf.get_rect(midleft=(self.rect.x + 8, self.rect.centery)))
            surface.set_clip(None)
        
        if self.active and self.cursor_visible and self.text:
            x = min(self.rect.x + 8 + self.font.size(self.text)[0], self.rect.right - 8)
            pygame.draw.line(surface, color, (x, self.rect.y + 6), (x, self.rect.bottom - 6), 2)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.cursor_visible = True
            self.cursor_timer = 0
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_TAB):
                self.active = False
            elif len(self.text) < self.max_length and event.unicode and event.unicode.isprintable():
                self.text += event.unicode
    
    def update(self, dt):
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= 0.5:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
    
    def get_text(self):
        return self.text
