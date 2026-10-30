#!/usr/bin/env bash
# OMNISLATE build launcher.
#   ./build.sh                      pick a campaign and build it
#   ./build.sh errans-inter-astra   build one campaign
#   ./build.sh --install-launcher   put a "Build OMNISLATE" icon on the desktop (run once)
HERE="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
cd "$HERE" || exit 1

if [ "$1" = "--install-launcher" ]; then
  DESK="$(xdg-user-dir DESKTOP 2>/dev/null || echo "$HOME/Desktop")"
  mkdir -p "$DESK" "$HOME/.local/share/applications"
  for DIR in "$DESK" "$HOME/.local/share/applications"; do
    F="$DIR/omnislate-build.desktop"
    cat > "$F" <<DESKTOP
[Desktop Entry]
Type=Application
Name=Build OMNISLATE
Comment=Build session files for the table display
Exec="$HERE/build.sh" --pause
Path=$HERE
Icon=applications-games
Terminal=true
Categories=Game;
DESKTOP
    chmod +x "$F"
    gio set "$F" metadata::trusted true 2>/dev/null || true
  done
  echo "Launcher installed: double-click \"Build OMNISLATE\" on the desktop."
  if ! python3 -c "import PIL" 2>/dev/null; then
    echo
    echo "One more step: Pillow is not installed.  Run this once:"
    echo "    sudo apt install python3-pil"
  fi
  exit 0
fi

PAUSE=0
ARGS=()
for a in "$@"; do
  if [ "$a" = "--pause" ]; then PAUSE=1; else ARGS+=("$a"); fi
done

python3 "$HERE/build.py" "${ARGS[@]}"
STATUS=$?
if [ $STATUS -eq 0 ]; then
  echo
  echo "Open a session file from: $HERE/dist/<campaign>/  (for example session-1.html)"
  echo "app/display.html is the empty engine template.  Skip that one."
  if [ $PAUSE -eq 1 ] && command -v xdg-open >/dev/null; then
    read -r -p "Open the dist folder now? [y/N] " OPEN
    case "$OPEN" in [yY]*) xdg-open "$HERE/dist" >/dev/null 2>&1 & ;; esac
  fi
fi
if [ $PAUSE -eq 1 ]; then
  echo
  read -r -p "Press Enter to close this window..." _
fi
exit $STATUS
