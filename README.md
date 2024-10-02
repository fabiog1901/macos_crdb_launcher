# MacOS_CRDB_Launcher

Simple MacOS menu utility to run CockroachDB locally.

![screenshot](screenshot.png)

## Build

### Requirements

Requires Python3.8 from <https://www.python.org/downloads/>.

```bash
pip3.8 install -U pip
pip3.8 install rumps py2app

brew install create-dmg
```

### Test and Build

Test locally without building

```bash
python3.8 macos_crdb_launcher.py
```

Build App

```bash
python3.8 setup.py py2app
```

Build DMG file

```bash
# https://github.com/create-dmg/create-dmg

create-dmg \
  --volname "CRDB_launcher Installer" \
  --volicon "icon.icns" \
  --window-pos 100 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --app-drop-link 100 100 \
  "CRDB_Launcher.dmg" \
  "dist/"
```
