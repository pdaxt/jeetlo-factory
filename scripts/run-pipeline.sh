#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# JEETLO PROOF CHAIN PIPELINE (LOCAL EXECUTION)
# ═══════════════════════════════════════════════════════════════════════════════
# Runs the complete 6-step pipeline locally using Claude Max (CLI).
# Each step produces a cryptographic hash that chains to the next.
#
# Usage:
#   ./scripts/run-pipeline.sh [reel_id]
#
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
CYAN='\033[0;36m'
NC='\033[0m'

print_box() {
    echo -e "${CYAN}┌─────────────────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│ $1${NC}"
    echo -e "${CYAN}└─────────────────────────────────────────────────────────────────────────────┘${NC}"
}

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🔗 JEETLO PROOF CHAIN PIPELINE${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Get reel_id
if [ -n "$1" ]; then
    REEL_ID="$1"
else
    echo -e "${YELLOW}Fetching latest pending request...${NC}"
    REQUESTS=$(gh api "repos/$REPO/contents/requests" --jq '.[].name' 2>/dev/null | grep -v "template\|README" || true)
    LATEST=$(echo "$REQUESTS" | tail -1)
    REEL_ID="${LATEST%.json}"
fi

echo -e "Reel ID: ${GREEN}$REEL_ID${NC}"

# Work directory
WORK_DIR="/tmp/jeetlo-chain-$REEL_ID"
PROOF_DIR="$WORK_DIR/proofs"
mkdir -p "$WORK_DIR" "$PROOF_DIR"
echo -e "Work Dir: $WORK_DIR"
echo ""

# Initialize proof chain
CHAIN_FILE="$WORK_DIR/chain.json"
echo '{"reel_id": "'$REEL_ID'", "steps": [], "status": "in_progress"}' > "$CHAIN_FILE"

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 0: FETCH REQUEST
# ═══════════════════════════════════════════════════════════════════════════════
print_box "STEP 0: FETCH REQUEST"

gh api "repos/$REPO/contents/requests/${REEL_ID}.json" --jq '.content' | base64 -d > "$WORK_DIR/request.json"
REQUEST_HASH=$(sha256sum "$WORK_DIR/request.json" | cut -d' ' -f1)

SUBJECT=$(jq -r '.subject' "$WORK_DIR/request.json")
TOPIC=$(jq -r '.topic' "$WORK_DIR/request.json")
HOOK=$(jq -r '.hook // "What is this about?"' "$WORK_DIR/request.json")

echo -e "Subject: ${GREEN}$SUBJECT${NC}"
echo -e "Topic: ${GREEN}$TOPIC${NC}"
echo -e "Request Hash: ${YELLOW}${REQUEST_HASH:0:16}...${NC}"
echo ""

# Add to chain
jq --arg hash "$REQUEST_HASH" '.steps += [{"step": "request", "input_hash": null, "output_hash": $hash}]' "$CHAIN_FILE" > "$CHAIN_FILE.tmp" && mv "$CHAIN_FILE.tmp" "$CHAIN_FILE"

PREV_HASH="$REQUEST_HASH"

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: SCRIPT (Claude CLI)
# ═══════════════════════════════════════════════════════════════════════════════
print_box "🤖① STEP 1: WRITE SCRIPT (Claude CLI)"

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

OUTPUT FORMAT (JSON only):
{
  \"segments\": [
    {\"id\": \"01_hook\", \"text\": \"Hook text...\"},
    {\"id\": \"02_setup\", \"text\": \"Setup...\"},
    {\"id\": \"03_explain\", \"text\": \"Explanation...\"},
    {\"id\": \"04_fact\", \"text\": \"Key fact...\"},
    {\"id\": \"05_why\", \"text\": \"Why it matters...\"},
    {\"id\": \"06_exam\", \"text\": \"Exam relevance...\"},
    {\"id\": \"07_cta\", \"text\": \"CTA - jeetlo.ai\"}
  ]
}

Output ONLY JSON."

echo "Running Claude CLI..."
claude --print --dangerously-skip-permissions --output-format json "$SCRIPT_PROMPT" 2>/dev/null | jq -r '.result' > "$WORK_DIR/script_raw.txt"

# Parse JSON
grep -v '```' "$WORK_DIR/script_raw.txt" | jq '.' > "$WORK_DIR/script.json" 2>/dev/null || {
    sed -n '/^{/,/^}/p' "$WORK_DIR/script_raw.txt" | jq '.' > "$WORK_DIR/script.json"
}

SEGMENT_COUNT=$(jq '.segments | length' "$WORK_DIR/script.json")
SCRIPT_HASH=$(sha256sum "$WORK_DIR/script.json" | cut -d' ' -f1)

echo -e "Segments: ${GREEN}$SEGMENT_COUNT${NC}"
echo -e "Input Hash: ${YELLOW}${PREV_HASH:0:16}...${NC}"
echo -e "Output Hash: ${GREEN}${SCRIPT_HASH:0:16}...${NC}"

# Validate chain
jq --arg input "$PREV_HASH" --arg output "$SCRIPT_HASH" '.steps += [{"step": "script", "input_hash": $input, "output_hash": $output}]' "$CHAIN_FILE" > "$CHAIN_FILE.tmp" && mv "$CHAIN_FILE.tmp" "$CHAIN_FILE"

PREV_HASH="$SCRIPT_HASH"
echo -e "${GREEN}✓ Chain linked${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: AUDIO (ElevenLabs or Google TTS)
# ═══════════════════════════════════════════════════════════════════════════════
print_box "🎙️② STEP 2: GENERATE AUDIO"

mkdir -p "$WORK_DIR/audio"

if [ -n "$ELEVENLABS_API_KEY" ]; then
    echo "Using ElevenLabs API..."
    VOICE_ID="WoB1yCV3pS7cFlDlu8ZU"  # Krishna Gupta

    CUMULATIVE=0
    TIMINGS="[]"

    for i in $(seq 0 $((SEGMENT_COUNT - 1))); do
        SEGMENT_ID=$(jq -r ".segments[$i].id" "$WORK_DIR/script.json")
        SEGMENT_TEXT=$(jq -r ".segments[$i].text" "$WORK_DIR/script.json")

        echo "  Generating: $SEGMENT_ID"

        curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID" \
            -H "xi-api-key: $ELEVENLABS_API_KEY" \
            -H "Content-Type: application/json" \
            -d "{
                \"text\": \"$SEGMENT_TEXT\",
                \"model_id\": \"eleven_multilingual_v2\",
                \"voice_settings\": {\"stability\": 0.5, \"similarity_boost\": 0.75}
            }" --output "$WORK_DIR/audio/${SEGMENT_ID}.mp3"

        DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$WORK_DIR/audio/${SEGMENT_ID}.mp3" 2>/dev/null || echo "3.0")
        TIMINGS=$(echo "$TIMINGS" | jq --arg id "$SEGMENT_ID" --arg text "$SEGMENT_TEXT" \
            --argjson dur "$DURATION" --argjson start "$CUMULATIVE" \
            '. += [{"id": $id, "text": $text, "duration": $dur, "startTime": $start}]')
        CUMULATIVE=$(echo "$CUMULATIVE + $DURATION" | bc)
    done

    echo "$TIMINGS" > "$WORK_DIR/audio/timings.json"

    # Combine audio
    cd "$WORK_DIR/audio"
    for f in *.mp3; do [ -f "$f" ] && echo "file '$f'"; done | grep -v timings > concat.txt
    ffmpeg -y -f concat -safe 0 -i concat.txt -c copy "$WORK_DIR/audio/combined.mp3" 2>/dev/null
    cd - > /dev/null

    AUDIO_HASH=$(sha256sum "$WORK_DIR/audio/combined.mp3" | cut -d' ' -f1)
    AUDIO_READY=true
else
    echo -e "${YELLOW}⚠ ELEVENLABS_API_KEY not set${NC}"
    echo -e "${YELLOW}  Skipping audio generation. Set: export ELEVENLABS_API_KEY=your_key${NC}"
    AUDIO_HASH=$(echo "placeholder_audio_$PREV_HASH" | sha256sum | cut -d' ' -f1)
    AUDIO_READY=false
fi

echo -e "Input Hash: ${YELLOW}${PREV_HASH:0:16}...${NC}"
echo -e "Output Hash: ${GREEN}${AUDIO_HASH:0:16}...${NC}"

jq --arg input "$PREV_HASH" --arg output "$AUDIO_HASH" '.steps += [{"step": "audio", "input_hash": $input, "output_hash": $output}]' "$CHAIN_FILE" > "$CHAIN_FILE.tmp" && mv "$CHAIN_FILE.tmp" "$CHAIN_FILE"

PREV_HASH="$AUDIO_HASH"
echo -e "${GREEN}✓ Chain linked${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: VIDEO (Manim)
# ═══════════════════════════════════════════════════════════════════════════════
print_box "🎬③ STEP 3: RENDER VIDEO (Manim)"

echo "Generating Manim code with Claude..."

VIDEO_PROMPT="Generate a complete Manim reel.py for this JeetLo reel.

SUBJECT: $SUBJECT
TOPIC: $TOPIC
SEGMENTS:
$(cat "$WORK_DIR/script.json")

REQUIREMENTS:
- 9:16 vertical (1080x1920)
- JeetLo brand colors (#1a3329 bg, #4CAF50 accent)
- Each segment should have text animations
- Total ~45-60 seconds
- Class name should be 'JeetLoReel'

Output ONLY Python code starting with 'from manim import *'
No markdown, no explanation."

claude --print --dangerously-skip-permissions --output-format json "$VIDEO_PROMPT" 2>/dev/null | jq -r '.result' > "$WORK_DIR/reel_raw.py"

# Clean up the code
grep -v '```' "$WORK_DIR/reel_raw.py" | grep -v '^python' > "$WORK_DIR/reel.py"

echo "Rendering with Manim..."
cd "$WORK_DIR"
if PATH=$PATH:/opt/homebrew/bin:/Library/TeX/texbin manim render -qh reel.py JeetLoReel --format mp4 2>/dev/null; then
    VIDEO_PATH=$(find media -name "*.mp4" | head -1)
    if [ -n "$VIDEO_PATH" ]; then
        cp "$VIDEO_PATH" "$WORK_DIR/video.mp4"
        VIDEO_HASH=$(sha256sum "$WORK_DIR/video.mp4" | cut -d' ' -f1)
        VIDEO_READY=true
        echo -e "${GREEN}✓ Video rendered${NC}"
    else
        echo -e "${YELLOW}⚠ No video output found${NC}"
        VIDEO_HASH=$(echo "placeholder_video_$PREV_HASH" | sha256sum | cut -d' ' -f1)
        VIDEO_READY=false
    fi
else
    echo -e "${YELLOW}⚠ Manim render failed - check $WORK_DIR/reel.py${NC}"
    VIDEO_HASH=$(echo "placeholder_video_$PREV_HASH" | sha256sum | cut -d' ' -f1)
    VIDEO_READY=false
fi
cd - > /dev/null

echo -e "Input Hash: ${YELLOW}${PREV_HASH:0:16}...${NC}"
echo -e "Output Hash: ${GREEN}${VIDEO_HASH:0:16}...${NC}"

jq --arg input "$PREV_HASH" --arg output "$VIDEO_HASH" '.steps += [{"step": "video", "input_hash": $input, "output_hash": $output}]' "$CHAIN_FILE" > "$CHAIN_FILE.tmp" && mv "$CHAIN_FILE.tmp" "$CHAIN_FILE"

PREV_HASH="$VIDEO_HASH"
echo -e "${GREEN}✓ Chain linked${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: COMBINE
# ═══════════════════════════════════════════════════════════════════════════════
print_box "🎞️④ STEP 4: COMBINE AUDIO + VIDEO"

if [ "$AUDIO_READY" = true ] && [ "$VIDEO_READY" = true ]; then
    ffmpeg -y \
        -i "$WORK_DIR/video.mp4" \
        -i "$WORK_DIR/audio/combined.mp3" \
        -c:v libx264 -preset fast -crf 18 \
        -c:a aac -b:a 192k \
        -shortest \
        "$WORK_DIR/final.mp4" 2>/dev/null

    FINAL_HASH=$(sha256sum "$WORK_DIR/final.mp4" | cut -d' ' -f1)
    COMBINE_READY=true
    echo -e "${GREEN}✓ Combined successfully${NC}"
else
    echo -e "${YELLOW}⚠ Skipping combine (audio or video not ready)${NC}"
    FINAL_HASH=$(echo "placeholder_final_$PREV_HASH" | sha256sum | cut -d' ' -f1)
    COMBINE_READY=false
fi

echo -e "Input Hash: ${YELLOW}${PREV_HASH:0:16}...${NC}"
echo -e "Output Hash: ${GREEN}${FINAL_HASH:0:16}...${NC}"

jq --arg input "$PREV_HASH" --arg output "$FINAL_HASH" '.steps += [{"step": "combine", "input_hash": $input, "output_hash": $output}]' "$CHAIN_FILE" > "$CHAIN_FILE.tmp" && mv "$CHAIN_FILE.tmp" "$CHAIN_FILE"

PREV_HASH="$FINAL_HASH"
echo -e "${GREEN}✓ Chain linked${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5: VALIDATE (Claude CLI)
# ═══════════════════════════════════════════════════════════════════════════════
print_box "✅⑤ STEP 5: VALIDATE CHAIN (Claude CLI)"

VALIDATE_PROMPT="You are a chain validator. Verify this proof chain is intact.

CHAIN:
$(cat "$CHAIN_FILE")

RULES:
1. First step (request) should have input_hash = null
2. Each subsequent step's input_hash MUST equal previous step's output_hash
3. All steps must exist: request, script, audio, video, combine

Output JSON only:
{
  \"valid\": true/false,
  \"chain_links\": [
    {\"from\": \"request\", \"to\": \"script\", \"linked\": true/false},
    ...
  ],
  \"errors\": []
}"

claude --print --dangerously-skip-permissions --output-format json "$VALIDATE_PROMPT" 2>/dev/null | jq -r '.result' > "$WORK_DIR/validation_raw.json"
grep -v '```' "$WORK_DIR/validation_raw.json" | jq '.' > "$WORK_DIR/validation.json" 2>/dev/null || echo '{"valid": false}' > "$WORK_DIR/validation.json"

IS_VALID=$(jq -r '.valid' "$WORK_DIR/validation.json")

if [ "$IS_VALID" = "true" ]; then
    echo -e "${GREEN}✓ Chain validation PASSED${NC}"
    VALIDATION_HASH=$(sha256sum "$WORK_DIR/validation.json" | cut -d' ' -f1)
else
    echo -e "${RED}✗ Chain validation FAILED${NC}"
    jq '.errors' "$WORK_DIR/validation.json"
    VALIDATION_HASH=$(echo "failed_validation_$PREV_HASH" | sha256sum | cut -d' ' -f1)
fi

jq --arg input "$PREV_HASH" --arg output "$VALIDATION_HASH" '.steps += [{"step": "validate", "input_hash": $input, "output_hash": $output}]' "$CHAIN_FILE" > "$CHAIN_FILE.tmp" && mv "$CHAIN_FILE.tmp" "$CHAIN_FILE"

PREV_HASH="$VALIDATION_HASH"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6: APPROVE FOR POST
# ═══════════════════════════════════════════════════════════════════════════════
print_box "🚀⑥ STEP 6: FINAL APPROVAL"

if [ "$IS_VALID" = "true" ] && [ "$COMBINE_READY" = true ]; then
    echo -e "${GREEN}✓ APPROVED FOR POSTING${NC}"

    # Update chain status
    jq '.status = "completed" | .approved = true | .can_post = ["instagram", "youtube"]' "$CHAIN_FILE" > "$CHAIN_FILE.tmp" && mv "$CHAIN_FILE.tmp" "$CHAIN_FILE"

    # Save final proof
    cp "$CHAIN_FILE" "$PROOF_DIR/chain_${REEL_ID}.json"
    cp "$WORK_DIR/final.mp4" "$PROOF_DIR/final_${REEL_ID}.mp4" 2>/dev/null || true
else
    echo -e "${RED}✗ NOT APPROVED - Chain incomplete or invalid${NC}"
    jq '.status = "failed" | .approved = false' "$CHAIN_FILE" > "$CHAIN_FILE.tmp" && mv "$CHAIN_FILE.tmp" "$CHAIN_FILE"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}📊 PIPELINE SUMMARY${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Chain visualization:"
jq -r '.steps[] | "  \(.step): \(.input_hash // "null" | .[0:12])... → \(.output_hash[0:12])..."' "$CHAIN_FILE"
echo ""

echo "Files:"
echo "  Chain proof: $CHAIN_FILE"
echo "  Script:      $WORK_DIR/script.json"
[ "$AUDIO_READY" = true ] && echo "  Audio:       $WORK_DIR/audio/combined.mp3"
[ "$VIDEO_READY" = true ] && echo "  Video:       $WORK_DIR/video.mp4"
[ "$COMBINE_READY" = true ] && echo "  Final:       $WORK_DIR/final.mp4"
echo ""

if [ "$(jq -r '.approved' "$CHAIN_FILE")" = "true" ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║           ✅ READY TO POST TO INSTAGRAM + YOUTUBE             ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "To post, run:"
    echo "  node /Users/pran/Projects/tools/social-automation/cli/bin/social.js schedule jeetlo instagram \"$WORK_DIR/final.mp4\""
else
    echo -e "${YELLOW}⚠ Pipeline incomplete. Check the steps above.${NC}"
fi
echo ""
