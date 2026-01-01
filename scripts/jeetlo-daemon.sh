#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# JEETLO DAEMON - Watches GitHub for new requests and auto-executes locally
# ═══════════════════════════════════════════════════════════════════════════
#
# This script runs continuously on your local machine and:
# 1. Polls GitHub every 30 seconds for new pending requests
# 2. Automatically runs jeetlo.sh for each new request
# 3. Pushes results back to GitHub
#
# Usage:
#   ./scripts/jeetlo-daemon.sh          # Run in foreground
#   ./scripts/jeetlo-daemon.sh &        # Run in background
#   nohup ./scripts/jeetlo-daemon.sh &  # Run persistently
#
# ═══════════════════════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
POLL_INTERVAL=30  # seconds
PROCESSED_FILE="$REPO_DIR/.processed_requests"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log() {
    echo -e "${CYAN}[$(date '+%H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')] ✓${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date '+%H:%M:%S')] ✗${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%H:%M:%S')] ⚠${NC} $1"
}

# Ensure processed file exists
touch "$PROCESSED_FILE"

# Banner
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   JEETLO DAEMON - Watching GitHub for new requests${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  Repo:     ${BLUE}$REPO_DIR${NC}"
echo -e "  Interval: ${BLUE}${POLL_INTERVAL}s${NC}"
echo -e "  Press ${RED}Ctrl+C${NC} to stop"
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Main loop
while true; do
    log "Checking for new requests..."

    # Pull latest from GitHub
    cd "$REPO_DIR"
    git pull origin main --quiet 2>/dev/null || {
        log_warning "Git pull failed, retrying next cycle"
        sleep "$POLL_INTERVAL"
        continue
    }

    # Find pending requests
    NEW_REQUESTS=0
    for request_file in requests/*.json; do
        # Skip template and non-existent
        [[ "$request_file" == "requests/_template.json" ]] && continue
        [[ ! -f "$request_file" ]] && continue

        # Get reel ID
        REEL_ID=$(basename "$request_file" .json)

        # Check if already processed
        if grep -q "^${REEL_ID}$" "$PROCESSED_FILE" 2>/dev/null; then
            continue
        fi

        # Check status
        STATUS=$(jq -r '.status // "pending"' "$request_file" 2>/dev/null)

        if [[ "$STATUS" == "pending" ]]; then
            NEW_REQUESTS=$((NEW_REQUESTS + 1))

            echo ""
            log_success "Found new request: ${BLUE}$REEL_ID${NC}"

            # Extract info
            SUBJECT=$(jq -r '.subject // "unknown"' "$request_file")
            TOPIC=$(jq -r '.topic // "unknown"' "$request_file")

            echo -e "  Subject: ${CYAN}$SUBJECT${NC}"
            echo -e "  Topic:   ${CYAN}$TOPIC${NC}"
            echo ""

            # Run jeetlo.sh
            log "Starting execution..."
            echo ""

            if "$SCRIPT_DIR/jeetlo.sh" "$REEL_ID"; then
                log_success "Completed: $REEL_ID"

                # Mark as processed
                echo "$REEL_ID" >> "$PROCESSED_FILE"

                # Update request status
                jq '.status = "completed"' "$request_file" > "$request_file.tmp" && mv "$request_file.tmp" "$request_file"

                # Push results
                log "Pushing results to GitHub..."
                git add -A
                git commit -m "Complete reel: $REEL_ID" --quiet 2>/dev/null || true
                git push origin main --quiet 2>/dev/null || log_warning "Push failed, will retry"

            else
                log_error "Failed: $REEL_ID"

                # Update request status to failed
                jq '.status = "failed"' "$request_file" > "$request_file.tmp" && mv "$request_file.tmp" "$request_file"

                git add -A
                git commit -m "Failed reel: $REEL_ID" --quiet 2>/dev/null || true
                git push origin main --quiet 2>/dev/null || true
            fi

            echo ""
        fi
    done

    if [[ $NEW_REQUESTS -eq 0 ]]; then
        log "No new requests. Sleeping ${POLL_INTERVAL}s..."
    fi

    sleep "$POLL_INTERVAL"
done
