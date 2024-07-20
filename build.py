import shutil
import os
import subprocess


def main():
    print("This script will build Arjun Launcher from source. If you have any issues please report them!")
    print("Building...")

    install = ["pygame-ce", "pyinstaller"]
    for package in install:
        print(f"Installing {package} using python -m pip (--upgrade)")
        subprocess.run(["python", "-m", "pip", "install", package, "--upgrade"])

    print("Executing pyinstaller build")
    subprocess.run(["pyinstaller", "./src/main.py", "--onefile"])  # before? ("python", "-m",)

    print("Building complete directory")
    if not os.path.isdir("./output/"):
        os.mkdir("./output/")

    print("Creating settings.json")
    with open("./output/settings.json", "w") as sf:
        sf.write('{\n"ASSET_DIR":"./assets/"\n, "REFRESH_RATE": 30}')  # hopefully works?
        sf.truncate()

    print("Moving from ./dist/main.exe to ./output/main.exe")
    shutil.move("./dist/main.exe", "./output/main.exe")

    print("Creating assets directory (and checking)")
    if not os.path.isdir("./output/assets/"):
        os.mkdir("./output/assets/")

    print("Moving assets")
    filenames = next(os.walk("./assets/"), (None, None, []))[2]
    for file in filenames:
        print(f"Moving {file}")
        shutil.copy(f"./assets/{file}", f"./output/assets/{file}")

    print("Build complete!")
    print("Run main.exe in the output directory (should be in the same one as this one!")
    input("Close this window now.")


if __name__ == "__main__":
    main()
