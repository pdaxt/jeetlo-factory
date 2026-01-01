#!/bin/bash
# Start the JeetLo daemon as a background service

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_FILE="$SCRIPT_DIR/com.jeetlo.daemon.plist"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"

echo "🚀 Starting JeetLo Daemon..."

# Create LaunchAgents if doesn't exist
mkdir -p "$LAUNCHD_DIR"

# Copy plist
cp "$PLIST_FILE" "$LAUNCHD_DIR/"

# Load the daemon
launchctl load "$LAUNCHD_DIR/com.jeetlo.daemon.plist" 2>/dev/null || {
    # Already loaded, unload and reload
    launchctl unload "$LAUNCHD_DIR/com.jeetlo.daemon.plist" 2>/dev/null
    launchctl load "$LAUNCHD_DIR/com.jeetlo.daemon.plist"
}

echo "✅ JeetLo Daemon started!"
echo ""
echo "📋 Commands:"
echo "   View logs:  tail -f ~/Projects/libraries/jeetlo-factory/logs/daemon.log"
echo "   Stop:       ./scripts/stop-daemon.sh"
echo "   Status:     launchctl list | grep jeetlo"
