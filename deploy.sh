#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

export AUTO_PUSH=1

# Colors for clear feedback
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

banner() { echo -e "\n${BLUE}${BOLD}════════════════════════════════════════${NC}"; echo -e "${BLUE}${BOLD}  $1${NC}"; echo -e "${BLUE}${BOLD}════════════════════════════════════════${NC}\n"; }
step()   { echo -e "${YELLOW}▶ STEP: $1${NC}"; }
done_msg() { echo -e "${GREEN}✅ DONE: $1${NC}"; }
err_msg() { echo -e "${RED}❌ ERROR: $1${NC}"; }

# Show help if no args and --help
if [ "$#" -eq 0 ]; then
  banner "📦 CATALOG UPDATE & DEPLOY"
  step "Rebuilding catalog (tags, JSON, PDF)..."
  ./update-catalog.sh
  done_msg "Catalog rebuilt and deployed! Website live in ~2 min."
  exit 0
fi

# Help command
if [ "$1" = "--help" ] || [ "$1" = "-h" ] || [ "$1" = "help" ]; then
  echo -e "${BOLD}Semwal Bespoke Fabrics — Deploy Tool${NC}"
  echo ""
  echo -e "${BOLD}USAGE:${NC}"
  echo "  ./deploy.sh                              Rebuild & push everything"
  echo "  ./deploy.sh I-440                        Mark I-440 out of stock & deploy"
  echo "  ./deploy.sh I-440 I-306 PI-531           Mark multiple OOS & deploy"
  echo "  ./deploy.sh oos I-440                    Same as above (explicit)"
  echo "  ./deploy.sh restore I-440                Bring I-440 back to active"
  echo "  ./deploy.sh meters I-217 4               Set 4 metres remaining for I-217"
  echo "  ./deploy.sh help                         Show this help"
  echo ""
  echo -e "${BOLD}WHAT HAPPENS:${NC}"
  echo "  1. Performs the action (archive/restore/set meters)"
  echo "  2. Regenerates fabric-tags.json"
  echo "  3. Regenerates catalog-data.json"
  echo "  4. Regenerates PDF catalog"
  echo "  5. Commits to Git automatically"
  echo "  6. Pushes to GitHub → website goes live in ~2 min"
  exit 0
fi

action="$1"
shift

case "$action" in
  oos|out-of-stock)
    if [ "$#" -lt 1 ]; then
      err_msg "Missing fabric code(s)"
      echo "Usage: ./deploy.sh oos I-440 [I-306 ...]"
      exit 1
    fi
    banner "🔴 MARKING OUT OF STOCK"
    echo -e "Fabrics: ${BOLD}$*${NC}"
    echo ""
    for code in "$@"; do
      step "Archiving $code → archive/out-of-stock/"
      ./mark-out-of-stock.sh "$code"
      done_msg "$code archived"
      echo ""
    done
    banner "🚀 ALL DONE — DEPLOYED"
    echo -e "Website will be live in ${BOLD}~2 minutes${NC}. Refresh with Cmd+Shift+R."
    ;;
  restore)
    if [ "$#" -lt 1 ]; then
      err_msg "Missing fabric code(s)"
      echo "Usage: ./deploy.sh restore I-440 [I-306 ...]"
      exit 1
    fi
    banner "🟢 RESTORING FABRIC(S) TO ACTIVE"
    echo -e "Fabrics: ${BOLD}$*${NC}"
    echo ""
    for code in "$@"; do
      step "Restoring $code → images/"
      ./restore-fabric.sh "$code"
      done_msg "$code restored to active catalog"
      echo ""
    done
    banner "🚀 ALL DONE — DEPLOYED"
    echo -e "Website will be live in ${BOLD}~2 minutes${NC}. Refresh with Cmd+Shift+R."
    ;;
  meters|meter)
    if [ "$#" -ne 2 ]; then
      err_msg "Need exactly 2 arguments: FABRIC_CODE and METERS"
      echo "Usage: ./deploy.sh meters I-217 4"
      exit 1
    fi
    banner "🟡 SETTING LOW STOCK METRES"
    echo -e "Fabric: ${BOLD}$1${NC}  →  ${BOLD}$2 metres remaining${NC}"
    echo ""
    step "Setting metres in fabric-tags.json..."
    ./set-meters.sh "$1" "$2"
    step "Rebuilding catalog..."
    ./update-catalog.sh
    done_msg "$1 now shows '$2 mtrs left' bar on website"
    echo ""
    banner "🚀 ALL DONE — DEPLOYED"
    echo -e "Website will be live in ${BOLD}~2 minutes${NC}. Refresh with Cmd+Shift+R."
    ;;
  update)
    banner "📦 CATALOG UPDATE & DEPLOY"
    step "Rebuilding catalog (tags, JSON, PDF)..."
    ./update-catalog.sh
    done_msg "Catalog rebuilt and deployed!"
    ;;
  *)
    # Treat all arguments as fabric codes to mark OOS directly
    banner "🔴 MARKING OUT OF STOCK"
    all_codes="$action $*"
    echo -e "Fabrics: ${BOLD}${all_codes}${NC}"
    echo ""
    for code in $action "$@"; do
      step "Archiving $code → archive/out-of-stock/"
      ./mark-out-of-stock.sh "$code"
      done_msg "$code archived"
      echo ""
    done
    banner "🚀 ALL DONE — DEPLOYED"
    echo -e "Website will be live in ${BOLD}~2 minutes${NC}. Refresh with Cmd+Shift+R."
    ;;
esac
