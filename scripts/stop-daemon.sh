#!/bin/bash
# Stop the JeetLo daemon

LAUNCHD_DIR="$HOME/Library/LaunchAgents"

echo "🛑 Stopping JeetLo Daemon..."

launchctl unload "$LAUNCHD_DIR/com.jeetlo.daemon.plist" 2>/dev/null

echo "✅ JeetLo Daemon stopped!"
