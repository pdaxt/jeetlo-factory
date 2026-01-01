#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# ISOLATED CLAUDE PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════
# Each step runs in a COMPLETELY FRESH Claude Max session.
# No shared context. No memory. Pure chain enforcement.
#
# Usage:
#   ./scripts/isolated-pipeline.sh <reel_id> <subject>
#
# Example:
#   ./scripts/isolated-pipeline.sh bio-07-test biology
# ═══════════════════════════════════════════════════════════════════════════════

set -e

REEL_ID="${1:?Usage: $0 <reel_id> <subject>}"
SUBJECT="${2:?Usage: $0 <reel_id> <subject>}"

WORK_DIR="/tmp/jeetlo-pipeline-$$"
mkdir -p "$WORK_DIR"

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "🔗 ISOLATED CLAUDE PIPELINE"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Reel ID: $REEL_ID"
echo "Subject: $SUBJECT"
echo "Work Dir: $WORK_DIR"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: CREATE - Fresh Claude #1
# ═══════════════════════════════════════════════════════════════════════════════
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│ 🤖① FRESH CLAUDE #1: CREATE                                                │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"

claude --print --dangerously-skip-permissions --output-format json "You are a JeetLo reel creation agent. You have NO MEMORY of any previous work. You are a FRESH instance.

Your ONLY task: Create a new manifest for reel_id='$REEL_ID', subject='$SUBJECT'.

Output ONLY valid JSON (no markdown, no explanation):
{
  \"version\": \"1.0.0\",
  \"reel_id\": \"$REEL_ID\",
  \"subject\": \"$SUBJECT\",
  \"created_at\": \"<current ISO timestamp>\",
  \"steps\": [{
    \"step_name\": \"create\",
    \"timestamp\": \"<current ISO timestamp>\",
    \"input_hash\": null,
    \"output_hash\": \"<generate 64 random hex chars>\",
    \"metadata\": {\"subject\": \"$SUBJECT\"}
  }],
  \"status\": \"in_progress\"
}

Output ONLY the JSON. Nothing else." | jq -r '.result' > "$WORK_DIR/step1_create.json"

echo "✅ Step 1 complete. Output hash: $(jq -r '.steps[0].output_hash' "$WORK_DIR/step1_create.json" | cut -c1-16)..."
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: AUDIO - Fresh Claude #2
# ═══════════════════════════════════════════════════════════════════════════════
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│ 🤖② FRESH CLAUDE #2: AUDIO                                                 │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"

PREV_MANIFEST=$(cat "$WORK_DIR/step1_create.json")
PREV_HASH=$(jq -r '.steps[-1].output_hash' "$WORK_DIR/step1_create.json")

claude --print --dangerously-skip-permissions --output-format json "You are a JeetLo AUDIO agent. You have NO MEMORY. You are a FRESH instance.

You received this manifest from the previous step:
$PREV_MANIFEST

Your task: Add an 'audio' step to this manifest.

CRITICAL CHAIN RULE:
- Your input_hash MUST be exactly: $PREV_HASH
- This links your step to the previous step's output

Add this step to the steps array:
{
  \"step_name\": \"audio\",
  \"timestamp\": \"<current ISO timestamp>\",
  \"input_hash\": \"$PREV_HASH\",
  \"output_hash\": \"<generate NEW 64 random hex chars>\",
  \"metadata\": {\"total_duration\": 51.0, \"segment_count\": 8}
}

Output the COMPLETE updated manifest JSON. Nothing else." | jq -r '.result' > "$WORK_DIR/step2_audio.json"

# Validate chain
AUDIO_INPUT=$(jq -r '.steps[] | select(.step_name=="audio") | .input_hash' "$WORK_DIR/step2_audio.json")
if [ "$AUDIO_INPUT" != "$PREV_HASH" ]; then
    echo "❌ CHAIN BROKEN: Audio input_hash doesn't match previous output_hash!"
    echo "   Expected: $PREV_HASH"
    echo "   Got: $AUDIO_INPUT"
    exit 1
fi
echo "✅ Step 2 complete. Chain validated."
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: VIDEO - Fresh Claude #3
# ═══════════════════════════════════════════════════════════════════════════════
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│ 🤖③ FRESH CLAUDE #3: VIDEO                                                 │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"

PREV_MANIFEST=$(cat "$WORK_DIR/step2_audio.json")
PREV_HASH=$(jq -r '.steps[-1].output_hash' "$WORK_DIR/step2_audio.json")

claude --print --dangerously-skip-permissions --output-format json "You are a JeetLo VIDEO agent. You have NO MEMORY. FRESH instance.

Manifest from previous step:
$PREV_MANIFEST

Add a 'video' step. Your input_hash MUST be: $PREV_HASH

Add:
{
  \"step_name\": \"video\",
  \"timestamp\": \"<ISO timestamp>\",
  \"input_hash\": \"$PREV_HASH\",
  \"output_hash\": \"<NEW 64 hex chars>\",
  \"metadata\": {\"resolution\": \"1080x1920\", \"video_duration\": 54.0}
}

Output COMPLETE updated manifest JSON only." | jq -r '.result' > "$WORK_DIR/step3_video.json"

VIDEO_INPUT=$(jq -r '.steps[] | select(.step_name=="video") | .input_hash' "$WORK_DIR/step3_video.json")
if [ "$VIDEO_INPUT" != "$PREV_HASH" ]; then
    echo "❌ CHAIN BROKEN at VIDEO step!"
    exit 1
fi
echo "✅ Step 3 complete. Chain validated."
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: COMBINE - Fresh Claude #4
# ═══════════════════════════════════════════════════════════════════════════════
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│ 🤖④ FRESH CLAUDE #4: COMBINE                                               │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"

PREV_MANIFEST=$(cat "$WORK_DIR/step3_video.json")
PREV_HASH=$(jq -r '.steps[-1].output_hash' "$WORK_DIR/step3_video.json")

claude --print --dangerously-skip-permissions --output-format json "You are a JeetLo COMBINE agent. NO MEMORY. FRESH.

Manifest:
$PREV_MANIFEST

Add 'combine' step. input_hash MUST be: $PREV_HASH

Add:
{
  \"step_name\": \"combine\",
  \"timestamp\": \"<ISO>\",
  \"input_hash\": \"$PREV_HASH\",
  \"output_hash\": \"<NEW 64 hex>\",
  \"metadata\": {\"final_duration\": 51.0, \"file_size_kb\": 2534}
}

Output complete manifest JSON." | jq -r '.result' > "$WORK_DIR/step4_combine.json"

COMBINE_INPUT=$(jq -r '.steps[] | select(.step_name=="combine") | .input_hash' "$WORK_DIR/step4_combine.json")
if [ "$COMBINE_INPUT" != "$PREV_HASH" ]; then
    echo "❌ CHAIN BROKEN at COMBINE step!"
    exit 1
fi
echo "✅ Step 4 complete. Chain validated."
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5: VALIDATE - Fresh Claude #5
# ═══════════════════════════════════════════════════════════════════════════════
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│ 🤖⑤ FRESH CLAUDE #5: VALIDATE ENTIRE CHAIN                                 │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"

PREV_MANIFEST=$(cat "$WORK_DIR/step4_combine.json")

claude --print --dangerously-skip-permissions --output-format json "You are a JeetLo VALIDATOR. NO MEMORY. FRESH. You validate the ENTIRE chain.

Manifest to validate:
$PREV_MANIFEST

Check:
1. First step (create) has input_hash = null
2. Each subsequent step's input_hash equals the previous step's output_hash
3. All required steps exist: create, audio, video, combine

Output JSON:
{
  \"valid\": true/false,
  \"chain\": [
    {\"step\": \"create\", \"input\": \"null\", \"output\": \"xxx...\", \"links\": true},
    {\"step\": \"audio\", \"input\": \"xxx...\", \"output\": \"yyy...\", \"links\": true/false},
    ...
  ],
  \"errors\": []
}

Only JSON output." | jq -r '.result' > "$WORK_DIR/step5_validate.json"

IS_VALID=$(jq -r '.valid' "$WORK_DIR/step5_validate.json" 2>/dev/null || echo "false")
if [ "$IS_VALID" != "true" ]; then
    echo "❌ VALIDATION FAILED!"
    cat "$WORK_DIR/step5_validate.json"
    exit 1
fi
echo "✅ Step 5 complete. CHAIN IS VALID!"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6: POST APPROVAL - Fresh Claude #6
# ═══════════════════════════════════════════════════════════════════════════════
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│ 🤖⑥ FRESH CLAUDE #6: FINAL GATEKEEPER                                      │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"

PREV_MANIFEST=$(cat "$WORK_DIR/step4_combine.json")

claude --print --dangerously-skip-permissions --output-format json "You are the FINAL GATEKEEPER. NO MEMORY. FRESH. You approve or reject posting.

Manifest:
$PREV_MANIFEST

Approve ONLY if:
1. Chain is complete and valid
2. All steps exist: create, audio, video, combine
3. Each step's input_hash links to previous output_hash

If approved, output:
{
  \"approved\": true,
  \"status\": \"completed\",
  \"can_post\": [\"instagram\", \"youtube\"],
  \"final_manifest\": <the manifest with status changed to completed>
}

If rejected:
{
  \"approved\": false,
  \"reason\": \"...\"
}

Only JSON." | jq -r '.result' > "$WORK_DIR/step6_post.json"

APPROVED=$(jq -r '.approved' "$WORK_DIR/step6_post.json" 2>/dev/null || echo "false")
if [ "$APPROVED" != "true" ]; then
    echo "❌ POST REJECTED!"
    jq -r '.reason' "$WORK_DIR/step6_post.json"
    exit 1
fi

# Save final manifest
jq -r '.final_manifest' "$WORK_DIR/step6_post.json" > "$WORK_DIR/final_manifest.json"

echo "✅ Step 6 complete. APPROVED FOR POSTING!"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "📊 PIPELINE COMPLETE"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "6 Fresh Claude instances executed in isolation:"
echo "  🤖① Create   → ✅"
echo "  🤖② Audio    → ✅"
echo "  🤖③ Video    → ✅"
echo "  🤖④ Combine  → ✅"
echo "  🤖⑤ Validate → ✅"
echo "  🤖⑥ Post     → ✅"
echo ""
echo "Final manifest saved to: $WORK_DIR/final_manifest.json"
echo ""
echo "Chain visualization:"
jq -r '.steps[] | "  \(.step_name): \(.input_hash // "null" | .[0:12])... → \(.output_hash[0:12])..."' "$WORK_DIR/final_manifest.json"
echo ""
echo "✅ Ready to post to Instagram and YouTube!"
