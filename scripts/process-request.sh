#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# JEETLO REEL PROCESSOR
# ═══════════════════════════════════════════════════════════════════════════════
# Processes a reel request using your local Claude Max subscription.
#
# Usage:
#   ./scripts/process-request.sh [reel_id]
#
# If no reel_id provided, fetches the latest pending request from GitHub.
# ═══════════════════════════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FACTORY_DIR="$(dirname "$SCRIPT_DIR")"
REPO="pdaxt/jeetlo-factory"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🎬 JEETLO REEL PROCESSOR${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Get reel_id from argument or fetch latest pending
if [ -n "$1" ]; then
    REEL_ID="$1"
    echo -e "${YELLOW}Processing specified reel: $REEL_ID${NC}"
else
    echo -e "${YELLOW}Fetching latest pending request from GitHub...${NC}"

    # List requests and find pending ones
    REQUESTS=$(gh api "repos/$REPO/contents/requests" --jq '.[].name' 2>/dev/null | grep -v "template\|README" || true)

    if [ -z "$REQUESTS" ]; then
        echo -e "${RED}No pending requests found.${NC}"
        exit 1
    fi

    # Get the most recent request
    LATEST=$(echo "$REQUESTS" | tail -1)
    REEL_ID="${LATEST%.json}"
    echo -e "${GREEN}Found: $REEL_ID${NC}"
fi

# Create work directory
WORK_DIR="/tmp/jeetlo-reel-$REEL_ID"
mkdir -p "$WORK_DIR"
echo -e "Work directory: $WORK_DIR"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: FETCH REQUEST
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}┌─────────────────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│ STEP 1: FETCH REQUEST                                                      │${NC}"
echo -e "${BLUE}└─────────────────────────────────────────────────────────────────────────────┘${NC}"

gh api "repos/$REPO/contents/requests/${REEL_ID}.json" --jq '.content' | base64 -d > "$WORK_DIR/request.json"
echo -e "${GREEN}✓ Request fetched${NC}"
cat "$WORK_DIR/request.json" | jq '.'
echo ""

SUBJECT=$(jq -r '.subject' "$WORK_DIR/request.json")
TOPIC=$(jq -r '.topic' "$WORK_DIR/request.json")
HOOK=$(jq -r '.hook' "$WORK_DIR/request.json")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: WRITE SCRIPT (Claude CLI)
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}┌─────────────────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│ STEP 2: WRITE SCRIPT (Claude CLI)                                          │${NC}"
echo -e "${BLUE}└─────────────────────────────────────────────────────────────────────────────┘${NC}"

SCRIPT_PROMPT="You are a JeetLo script writer. Write a 45-second Hinglish reel script.

TOPIC: $TOPIC
HOOK: $HOOK
SUBJECT: $SUBJECT

RULES:
- Use Devanagari for Hindi words (भाई not bhai)
- Use English for technical terms
- Numbers in English (forty two, not बयालीस)
- Greek letters in Devanagari (थीटा for theta)
- Add emotion: CAPS for emphasis, ... for pauses, ! for energy

OUTPUT FORMAT (JSON only, no markdown):
{
  \"segments\": [
    {\"id\": \"01_hook\", \"text\": \"Hook text here...\"},
    {\"id\": \"02_setup\", \"text\": \"Setup text...\"},
    {\"id\": \"03_explain\", \"text\": \"Explanation...\"},
    {\"id\": \"04_fact\", \"text\": \"Key fact...\"},
    {\"id\": \"05_why\", \"text\": \"Why it matters...\"},
    {\"id\": \"06_exam\", \"text\": \"Exam relevance...\"},
    {\"id\": \"07_cta\", \"text\": \"Call to action...\"}
  ]
}

Output ONLY the JSON. Nothing else."

echo "Running Claude CLI for script generation..."
claude --print --dangerously-skip-permissions --output-format json "$SCRIPT_PROMPT" 2>/dev/null | jq -r '.result' > "$WORK_DIR/script_raw.txt"

# Parse the JSON from Claude's response
grep -v '```' "$WORK_DIR/script_raw.txt" | jq '.' > "$WORK_DIR/script.json" 2>/dev/null || {
    # Try to extract JSON if wrapped in markdown
    sed -n '/^{/,/^}/p' "$WORK_DIR/script_raw.txt" | jq '.' > "$WORK_DIR/script.json"
}

SEGMENT_COUNT=$(jq '.segments | length' "$WORK_DIR/script.json")
echo -e "${GREEN}✓ Script generated with $SEGMENT_COUNT segments${NC}"
echo ""

# Show preview
echo "Script preview:"
jq -r '.segments[0:2] | .[] | "  \(.id): \(.text[0:60])..."' "$WORK_DIR/script.json"
echo "  ..."
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: GENERATE AUDIO (placeholder - needs ElevenLabs)
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}┌─────────────────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│ STEP 3: GENERATE AUDIO                                                     │${NC}"
echo -e "${BLUE}└─────────────────────────────────────────────────────────────────────────────┘${NC}"

# Check for ElevenLabs API key
if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo -e "${YELLOW}⚠ ELEVENLABS_API_KEY not set. Audio generation skipped.${NC}"
    echo -e "${YELLOW}  Set it with: export ELEVENLABS_API_KEY=your_key${NC}"
    AUDIO_READY=false
else
    echo "Generating audio for each segment..."
    mkdir -p "$WORK_DIR/audio"

    # Generate audio for each segment
    for i in $(seq 0 $((SEGMENT_COUNT - 1))); do
        SEGMENT_ID=$(jq -r ".segments[$i].id" "$WORK_DIR/script.json")
        SEGMENT_TEXT=$(jq -r ".segments[$i].text" "$WORK_DIR/script.json")

        echo "  Generating: $SEGMENT_ID"

        curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/WoB1yCV3pS7cFlDlu8ZU" \
            -H "xi-api-key: $ELEVENLABS_API_KEY" \
            -H "Content-Type: application/json" \
            -d "{
                \"text\": \"$SEGMENT_TEXT\",
                \"model_id\": \"eleven_multilingual_v2\",
                \"voice_settings\": {
                    \"stability\": 0.5,
                    \"similarity_boost\": 0.75
                }
            }" --output "$WORK_DIR/audio/${SEGMENT_ID}.mp3"
    done

    # Combine audio files
    echo "Combining audio segments..."
    cd "$WORK_DIR/audio"
    for f in *.mp3; do echo "file '$f'"; done > concat.txt
    ffmpeg -y -f concat -safe 0 -i concat.txt -c copy "$WORK_DIR/combined_audio.mp3" 2>/dev/null

    echo -e "${GREEN}✓ Audio generated and combined${NC}"
    AUDIO_READY=true
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: RENDER VIDEO (placeholder - needs Manim setup)
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}┌─────────────────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│ STEP 4: RENDER VIDEO                                                       │${NC}"
echo -e "${BLUE}└─────────────────────────────────────────────────────────────────────────────┘${NC}"

echo -e "${YELLOW}⚠ Video rendering requires Manim scene creation.${NC}"
echo -e "${YELLOW}  Script saved to: $WORK_DIR/script.json${NC}"
echo -e "${YELLOW}  Create Manim scene and run: manim render scene.py${NC}"
VIDEO_READY=false
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}📊 PROCESSING SUMMARY${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "  Reel ID:    $REEL_ID"
echo "  Subject:    $SUBJECT"
echo "  Topic:      $TOPIC"
echo ""
echo "  Outputs:"
echo "    - Request:  $WORK_DIR/request.json"
echo "    - Script:   $WORK_DIR/script.json"
if [ "$AUDIO_READY" = true ]; then
    echo "    - Audio:    $WORK_DIR/combined_audio.mp3"
fi
echo ""

if [ "$AUDIO_READY" = true ] && [ "$VIDEO_READY" = true ]; then
    echo -e "${GREEN}✅ Ready to combine and post!${NC}"
else
    echo -e "${YELLOW}⚠ Manual steps remaining:${NC}"
    [ "$AUDIO_READY" = false ] && echo "   - Generate audio (set ELEVENLABS_API_KEY)"
    [ "$VIDEO_READY" = false ] && echo "   - Create and render Manim video"
    echo ""
    echo "After completing, run:"
    echo "  ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -shortest final.mp4"
fi
echo ""
