#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

export AUTO_PUSH=1

if [ "$#" -eq 0 ]; then
  echo "Running catalog update & auto-deploy..."
  ./update-catalog.sh
  exit 0
fi

action="$1"
shift

case "$action" in
  oos|out-of-stock)
    if [ "$#" -lt 1 ]; then
      echo "Usage: ./deploy.sh oos FABRIC_CODE_1 [FABRIC_CODE_2 ...]"
      exit 1
    fi
    for code in "$@"; do
      echo "=== Archiving $code ==="
      # mark-out-of-stock runs update-catalog.sh internally
      ./mark-out-of-stock.sh "$code"
    done
    ;;
  restore)
    if [ "$#" -lt 1 ]; then
      echo "Usage: ./deploy.sh restore FABRIC_CODE_1 [FABRIC_CODE_2 ...]"
      exit 1
    fi
    for code in "$@"; do
      echo "=== Restoring $code ==="
      ./restore-fabric.sh "$code"
    done
    ;;
  meters|meter)
    if [ "$#" -ne 2 ]; then
      echo "Usage: ./deploy.sh meters FABRIC_CODE METERS"
      exit 1
    fi
    ./set-meters.sh "$1" "$2"
    ./update-catalog.sh
    ;;
  update)
    ./update-catalog.sh
    ;;
  *)
    # Treat arguments as fabric codes to mark OOS directly
    for code in "$action" "$@"; do
      echo "=== Archiving $code ==="
      ./mark-out-of-stock.sh "$code"
    done
    ;;
esac
