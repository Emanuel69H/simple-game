"""Base Screen Class."""

import pygame


class BaseScreen:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.buttons = []
        self.labels = []
        self.inputs = []
        self.all_elements = []
    
    def add_button(self, button):
        self.buttons.append(button)
        self.all_elements.append(button)
    
    def add_input(self, inp):
        self.inputs.append(inp)
        self.all_elements.append(inp)
    
    def add_label(self, label):
        self.labels.append(label)
        self.all_elements.append(label)

    def handle_event(self, event):
        for i in self.all_elements:
            i.handle_event(event)
        # for b in self.buttons:
        #     b.handle_event(event)
        # for i in self.inputs:
        #     i.handle_event(event)
    
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
            'input_active': self.config.input_active,
            'label_color': self.config.label_color
        }
        # for b in self.buttons:
        #     b.draw(self.screen, theme)
        # for i in self.inputs:
        #     i.draw(self.screen, theme)

        for i in self.all_elements:
            i.draw(self.screen, theme)
        # for i in self.
    
    def on_enter(self):
        pass
    
    def on_exit(self):
        pass
