from libs import ui, config
from app import Application


def main():
    ui.init()
    screen = ui.CScaleScreen(size=(720, 405), prescaledSize=(2560, 1440), caption="SOTCommunications", scrap=False, clock=True)
    settings = config.Settings()

    settings.COMFORT = settings.ASSET_DIR + "COMFORT.ttf"

    app = Application(screen, settings)

    app.run()


if __name__ == "__main__":
    main()
