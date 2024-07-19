from libs import ui, config
import pygame
from client import Client
from SOTMenu import SOTMenu


class ConnectMenu:
    def __init__(self, screen: ui.CScaleScreen, settings: config.Settings):
        self.screen = screen
        self.settings = settings

        FONT_title = ui.CUIFont(settings.COMFORT, 100, ui.CUColor.WHITE())
        self.LABEL_title = ui.CUILabel(FONT_title.get_center(self.screen.prescaledSurface, "Connect (ENTER IP ADDR)").x, 100, FONT_title,
                                       "Connect (ENTER IP ADDR)")

        self.TEXTBOX_addr = ui.CUITextInput(1280 - 500, 300, 1000, 200, ui.CUColor.GRAY(),
                                            ui.CUIFont(settings.COMFORT, 60, ui.CUColor.WHITE()),
                                            "Enter IP (ex: 127.0.0.1)", draw_border_radius=10, onTextUpdate=lambda _: True)
        self.TEXTBOX_BORDER_addr = ui.CUIObject(self.TEXTBOX_addr.x, self.TEXTBOX_addr.y, self.TEXTBOX_addr.width, self.TEXTBOX_addr.height, ui.CUColor.BLACK(), draw_border_radius=10, draw_width=10)

        self.BUTTON_connect = ui.CUITextButton(930, 600, 700, 140, ui.CUColor.GRAY(), ui.CUIFont(settings.COMFORT, 60, ui.CUColor.WHITE()), "CONNECT")
        self.manager = ui.CUIManager([self.TEXTBOX_addr, self.BUTTON_connect], scale=True, preres=self.screen.prescaledSurface.size, postres=self.screen.surface.size)

        self.client = None

    def run(self):
        while True:
            self.screen.clock.tick(60)

            events = pygame.event.get()
            self.manager.tick(events)

            if self.BUTTON_connect.isPressed is True:
                self.client = Client(self.TEXTBOX_addr.text)
                self.BUTTON_connect.isPressed = False
                SOTMenu(self.screen, self.settings, self.client).run()

            for event in events:
                if event.type == pygame.QUIT:
                    return

                elif event.type == pygame.WINDOWRESIZED:
                    print(self.screen.surface.size)
                    self.manager.set_scale(self.screen.prescaledSurface.size, self.screen.surface.size)

            self.screen.fill(ui.CUColor.BLUE())

            self.LABEL_title.draw(self.screen.prescaledSurface)

            self.TEXTBOX_addr.draw(self.screen.prescaledSurface)
            self.TEXTBOX_BORDER_addr.draw(self.screen.prescaledSurface)

            self.BUTTON_connect.draw(self.screen.prescaledSurface)

            self.screen.before_flip()
            pygame.display.flip()
