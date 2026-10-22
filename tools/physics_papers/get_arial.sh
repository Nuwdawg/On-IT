#!/bin/sh
# Fetch Arial (Microsoft's freely distributable core font package) into
# tools/physics_papers/fonts/ for the build. The font files are not kept in
# the repository: Microsoft allows the package to be passed on only in its
# original form. Needs curl and cabextract (apt-get install cabextract).
set -e
cd "$(dirname "$0")"
mkdir -p fonts
cd fonts
[ -f arial.ttf ] && exit 0
curl -sSL -o arial32.exe https://downloads.sourceforge.net/corefonts/arial32.exe
cabextract -q -L -F '*.ttf' arial32.exe
rm -f arial32.exe
ls *.ttf
