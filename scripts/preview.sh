#!/bin/sh
# Render a Powerlevel10k-style test string with the built font on a throw-away
# Xvfb display (never touches your real X session). Usage: scripts/preview.sh [out.png]
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/build/preview.png}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
bdftopcf -o "$TMP/fixednerd6x13.pcf" "$ROOT/build/fixed-nerd-6x13.bdf"
mkfontdir "$TMP"
cat > "$TMP/demo.sh" <<'DEMO'
printf 'Fixed Nerd 6x13 -- the quick brown fox jumps over the lazy dog 0123456789\n\n'
printf '\033[30;44m  ~/src \033[34;42m\356\202\260\033[30;42m \356\202\240 main \033[32;49m\356\202\260\033[0m\n'
printf '\033[97;41m user \033[31;100m\356\202\260\033[97;100m  ~ \033[90;49m\356\202\260\033[0m  \356\202\262 \356\202\263 \356\202\264 \356\202\265 \356\202\266 \356\202\267\n'
printf 'Icons: \357\204\246 \357\200\214 \357\200\225 \357\201\274 \357\204\240 \356\234\245 \356\230\240 \357\220\230 \357\220\200 \356\255\204 \357\202\233 \357\200\207 \357\200\223\n'
printf '\342\235\257 hello  \342\217\272 Bash(ls)  \342\216\277 done  \342\234\273 Thinking\342\200\246  \342\217\265\342\217\265 accept edits  \342\217\270 plan  \342\232\240 warn  \342\247\211 sel  \342\244\267\n'
printf 'Box: \342\224\214\342\224\200\342\224\254\342\224\200\342\224\220  Braille: \342\240\277\342\243\277  Kbd: \357\204\234\n'
sleep 4
DEMO
# Xvfb ignores `xset +fp` for new directories, so pass the font path at server start.
FP="$TMP,/usr/share/fonts/X11/misc,/usr/share/fonts/X11/100dpi/:unscaled,/usr/share/fonts/X11/75dpi/:unscaled,built-ins"
xvfb-run -a -s "-noreset -screen 0 640x180x24 -fp $FP" sh -c "
  xterm -u8 -fn '-jaderfeijo-FixedNerd-medium-r-semicondensed--13-120-75-75-c-60-iso10646-1' \\
        -geometry 80x9+0+0 -e sh '$TMP/demo.sh' &
  sleep 2; import -window root '$OUT'; wait"
echo "wrote $OUT"
