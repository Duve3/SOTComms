import os
from pathlib import Path
import json


def FindSettingsFile():  # notTODO: change this to write it in this file, or be a one time thing (maybe?)
    dots = "."
    while True:
        try:
            print(f"trying {dots}/settings.json")
            file = open(f"{dots}/settings.json")
        except FileNotFoundError:
            dots += "."
            continue

        file.close()
        return str(Path(f"{dots}/settings.json").absolute())  # converting these dot paths into absolute values.


def FindAssetsDirectory():
    import os
    dots = "."
    while True:
        print(f"trying {dots}/assets")
        if os.path.isdir(f"{dots}/assets/"):
            return str(Path(f"{dots}/assets/").absolute())  # converting these dot paths into absolute values.
        dots += "."

        if len(dots) >= 3:  # this is to prevent finding the incorrect assets' directory.
            return None


SETTINGS_PATH = FindSettingsFile()


class Config:
    template = {}

    def read(self):
        pass

    def write(self):
        pass


class Settings(Config):
    """
    Settings object
    """
    template = {
        "ASSET_DIR": str(),  # The path to the assets folder
        "REFRESH_RATE": int()  # the refresh rate for SOT data
    }

    def __init__(self):
        # bs values, used for type checking
        # ex: self.TOKEN = str() or None
        self.ASSET_DIR = str() or None
        self.REFRESH_RATE = int() or None

        # following set in the main function based on values pulled.
        self.COMFORT = str()

        self.read()

        if not os.path.exists(self.ASSET_DIR):
            self.ASSET_DIR = None

        # find asset dir
        if self.ASSET_DIR is None:
            self.ASSET_DIR = FindAssetsDirectory()
            if self.ASSET_DIR is None:
                raise NotADirectoryError("Unable to find assets directory! (report this to the developers!)")

        if not self.ASSET_DIR.endswith("\\"):
            self.ASSET_DIR += "\\"

        if self.REFRESH_RATE is None:
            self.REFRESH_RATE = 30

        self.write()

    def read(self):
        # read data
        with open(SETTINGS_PATH, "r") as sf:
            data: dict = json.loads(sf.read())

            # by using the get thing, we allow it to default incase values do not exist.
            self.ASSET_DIR = data.get("ASSET_DIR", self.ASSET_DIR)
            self.REFRESH_RATE = data.get("REFRESH_RATE", self.REFRESH_RATE)

    def write(self):
        # write data
        with open(SETTINGS_PATH, "w") as sf:
            data = json.dumps({
                "ASSET_DIR": self.ASSET_DIR,
                "REFRESH_RATE": self.REFRESH_RATE
            })

            sf.write(data)
