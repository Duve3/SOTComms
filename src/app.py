import pygame
from libs import ui, config
from connectMenu import ConnectMenu


class Application:
    def __init__(self, screen: ui.CScaleScreen, settings: config.Settings):
        self.screen = screen
        self.settings = settings

        self.menus = [ConnectMenu(self.screen, self.settings)]

    def run(self):
        self.menus[0].run()

