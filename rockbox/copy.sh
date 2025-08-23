#!/usr/bin/env bash

set -eux

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

abort() {
    echo "Error: $1" >&2
    exit 1
}

ROCKBOX_TARGET_DIR=/run/media/mike/ROCKBOX/.rockbox

test -d "$ROCKBOX_TARGET_DIR" || abort "Rockbox target dir not found."

cp -r "$SCRIPT_DIR/.rockbox/." "$ROCKBOX_TARGET_DIR/"
