#!/bin/sh
# Download the upstream misc-fixed 6x13 BDF sources at a pinned commit.
set -eu
COMMIT=c4e2af05583764fae3d0b2aa20d5c93b031cbcbf
BASE="https://gitlab.freedesktop.org/xorg/font/misc-misc/-/raw/$COMMIT"
cd "$(dirname "$0")/../upstream"
for f in 6x13.bdf 6x13B.bdf 6x13O.bdf COPYING AUTHORS; do
    curl -fsSL -o "$f" "$BASE/$f"
done
sha256sum 6x13.bdf 6x13B.bdf 6x13O.bdf COPYING AUTHORS
