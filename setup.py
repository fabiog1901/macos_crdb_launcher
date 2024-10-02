from setuptools import setup

APP = ["CRDB_Launcher.py"]
DATA_FILES = ["cockroachdb_logo.png"]
OPTIONS = {
    "argv_emulation": True,
    "iconfile": "icon.icns",
    "plist": {
        "LSUIElement": True,
    },
    "packages": ["rumps", "subprocess"],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
