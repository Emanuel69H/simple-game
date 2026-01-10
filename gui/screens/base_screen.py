"""Base Screen Class."""

import pygame


class BaseScreen:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.buttons = []
        self.inputs = []
    
    def add_button(self, button):
        self.buttons.append(button)
    
    def add_input(self, inp):
        self.inputs.append(inp)
    
    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)
        for i in self.inputs:
            i.handle_event(event)
    
    def update(self, dt):
        for i in self.inputs:
            i.update(dt)
    
    def draw(self):
        self.screen.fill(self.config.bg_color)
        theme = {
            'button_color': self.config.button_color,
            'button_hover': self.config.button_hover,
            'text_color': self.config.text_color,
            'input_border': self.config.input_border,
            'input_active': self.config.input_active
        }
        for b in self.buttons:
            b.draw(self.screen, theme)
        for i in self.inputs:
            i.draw(self.screen, theme)
        pygame.display.flip()
    
    def on_enter(self):
        pass
    
    def on_exit(self):
        pass
