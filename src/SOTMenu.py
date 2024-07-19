from libs import ui, config
import pygame
from client import Client


class SOTMenu:
    def __init__(self, screen: ui.CScaleScreen, settings: config.Settings, client: Client):
        self.screen = screen
        self.settings = settings

        FONT_title = ui.CUIFont(settings.COMFORT, 100, ui.CUColor.WHITE())
        self.LABEL_title = ui.CUILabel(FONT_title.get_center(self.screen.prescaledSurface,
                                                             f"Connected to {client.server}, CLASS: {client.SOT.SHIP_CLASS}").x,
                                       100, FONT_title, f"Connected to {client.server}, CLASS: {client.SOT.SHIP_CLASS}")

        self.BUTTON_disconnect = ui.CUITextButton(0, 1340, 500, 100, ui.CUColor.GREY(),
                                                  ui.CUIFont(settings.COMFORT, 60, ui.CUColor.WHITE()), "DISCONNECT",
                                                  draw_border_radius=10)
        self.BUTTON_BORDER_disconnect = ui.CUIObject(self.BUTTON_disconnect.x, self.BUTTON_disconnect.y,
                                                     self.BUTTON_disconnect.width, self.BUTTON_disconnect.height,
                                                     ui.CUColor.BLACK(), draw_border_radius=10, draw_width=10)

        self.manager = ui.CUIManager([self.BUTTON_disconnect], scale=True, preres=self.screen.prescaledSurface.size,
                                     postres=self.screen.surface.size)

        self.client = client

        # statuses
        FONT_stats = ui.CUIFont(settings.COMFORT, 80, ui.CUColor.WHITE())

        direct = "RIGHT"
        if client.SOT.STEERING_PERCENT < 0:
            direct = "LEFT"

        self.LABEL_steering = ui.CUILabel(
            FONT_stats.get_center(self.screen.prescaledSurface, f"Steering: {abs(client.SOT.STEERING_PERCENT)}% {direct}").x, 400,
            FONT_stats, f"Steering: {abs(client.SOT.STEERING_PERCENT)}% {direct}")

    def on_refresh(self, client):
        FONT_stats = ui.CUIFont(self.settings.COMFORT, 80, ui.CUColor.WHITE())

        direct = "RIGHT"
        if client.SOT.STEERING_PERCENT < 0:
            direct = "LEFT"

        self.LABEL_steering = ui.CUILabel(
            FONT_stats.get_center(self.screen.prescaledSurface, f"Steering: {abs(client.SOT.STEERING_PERCENT)}% {direct}").x, 400,
            FONT_stats, f"Steering: {abs(client.SOT.STEERING_PERCENT)}% {direct}")

    def run(self):
        frames = 0
        while True:
            self.screen.clock.tick(60)
            frames += 1

            if frames % 30 == 0:
                self.client.refresh()
                self.on_refresh(self.client)

            events = pygame.event.get()
            self.manager.tick(events)

            if self.BUTTON_disconnect.isPressed:
                self.client.disconnect()
                self.screen.close(kill=True)

            for event in events:
                if event.type == pygame.QUIT:
                    return

                elif event.type == pygame.WINDOWRESIZED:
                    self.manager.set_scale(self.screen.prescaledSurface.size, self.screen.surface.size)

            self.screen.fill(ui.CUColor.BLUE())

            self.LABEL_title.draw(self.screen.prescaledSurface)

            self.BUTTON_disconnect.draw(self.screen.prescaledSurface)
            self.BUTTON_BORDER_disconnect.draw(self.screen.prescaledSurface)

            # statuses
            self.LABEL_steering.draw(self.screen.prescaledSurface)

            self.screen.before_flip()
            pygame.display.flip()
