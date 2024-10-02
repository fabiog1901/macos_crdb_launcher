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
