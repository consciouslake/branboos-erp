#!/bin/bash
# Vendored from frappe_docker's resources/core/main-entrypoint.sh
# https://github.com/frappe/frappe_docker/blob/main/resources/core/main-entrypoint.sh
# Links the image's baked-in assets into the mounted sites volume at
# container start (assets live in the image layer, not the volume, per
# resources/core/07-how-assets-are-handled).
set -e

ASSETS_PATH="/home/frappe/frappe-bench/sites/assets"
BAKED_PATH="/home/frappe/frappe-bench/assets"

echo "Linking fresh assets to volume..."
rm -rf "$ASSETS_PATH"
mkdir -p "$(dirname "$ASSETS_PATH")"
ln -s "$BAKED_PATH" "$ASSETS_PATH"

exec "$@"
