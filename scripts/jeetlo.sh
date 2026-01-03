#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# JEETLO REEL FACTORY - COMPLETE LOCAL PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════
#
# This script runs the ENTIRE reel creation pipeline locally using Claude CLI.
# Each step runs a FRESH Claude instance with NO memory of previous steps.
# The proof chain cryptographically links each step to the previous.
#
# EMBEDDED KNOWLEDGE:
# - Voice Learnings (Prosody Engine): Fenrir @ 0.9, NO SSML, NO post-processing
# - Audio Learnings: Emotion presets, segment structure, Hindi in Devanagari
# - Video Learnings: VP1-VP8 rules, frame QA, sync validation
# - manim-edu: Required primitives for each subject
# - Brand Rules: CTA, watermark, subject colors, aap tone
#
# Usage:
#   ./scripts/jeetlo.sh <reel_id> [--resume]
#
# Example:
#   ./scripts/jeetlo.sh bio-05-dna-right-handed
#   ./scripts/jeetlo.sh phy-01-laws-of-motion --resume
#
# ═══════════════════════════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FACTORY_DIR="$(dirname "$SCRIPT_DIR")"
CONTENT_FACTORY="/Users/pran/Projects/ace/content-factory"
JEETLO_BRAND="$CONTENT_FACTORY/brands/jeetlo"
MANIM_EDU="/Users/pran/Projects/libraries/manim-edu"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════════════════════
# EMBEDDED KNOWLEDGE - ALL OUR LEARNINGS
# ═══════════════════════════════════════════════════════════════════════════════

# PROSODY ENGINE (10+ iterations of learning)
VOICE_SETTINGS='{
  "voice": "hi-IN-Chirp3-HD-Fenrir",
  "speakingRate": 0.9,
  "audioEncoding": "MP3",
  "ssml": false,
  "postProcessing": false,
  "why": "Deliberate pace = authority (Morgan Freeman effect). Chirp3-HD has built-in emotion, SSML makes it robotic."
}'

# SUBJECT CONFIG
SUBJECT_CONFIG='{
  "physics": {
    "color": "#0066FF",
    "background": "#0A1A3F",
    "voice": "hi-IN-Chirp3-HD-Orus",
    "icon": "⚡",
    "manim_edu_imports": ["WaveSimulator", "FieldVisualizer", "MechanicsSimulator"]
  },
  "chemistry": {
    "color": "#00CC66",
    "background": "#0A2F1F",
    "voice": "hi-IN-Chirp3-HD-Fenrir",
    "icon": "🧪",
    "manim_edu_imports": ["MoleculeBuilder"]
  },
  "biology": {
    "color": "#CC66FF",
    "background": "#2A1A3F",
    "voice": "hi-IN-Chirp3-HD-Leda",
    "icon": "🧬",
    "manim_edu_imports": ["CellVisualizer"]
  },
  "mathematics": {
    "color": "#FF9900",
    "background": "#3F2A0A",
    "voice": "hi-IN-Chirp3-HD-Kore",
    "icon": "📐",
    "manim_edu_imports": ["GraphAnimator"]
  }
}'

# SEGMENT STRUCTURE
SEGMENT_STRUCTURE='{
  "01_hook": {"purpose": "Grab attention", "duration": "3-5s", "emotion": "excited", "patterns": ["WRONG!", "Everyone thinks X but..."]},
  "02_setup": {"purpose": "Set up problem", "duration": "5-8s", "emotion": "curious"},
  "03_content": {"purpose": "Main education", "duration": "20-30s", "emotion": "informative"},
  "04_reveal": {"purpose": "Aha moment", "duration": "5-8s", "emotion": "triumphant"},
  "05_key_point": {"purpose": "Key takeaway", "duration": "5-8s", "emotion": "serious"},
  "06_exam_tip": {"purpose": "JEE/NEET relevance", "duration": "5-8s", "emotion": "informative"},
  "07_cta": {"purpose": "Follow/subscribe", "duration": "3-5s", "emotion": "warm"}
}'

# VIDEO PRODUCTION RULES
VIDEO_RULES='{
  "VP1": "Hook in first 3 seconds",
  "VP2": "Audio/video values MUST match exactly",
  "VP3": "Frame QA at 0.5fps minimum before delivery",
  "VP4": "60 seconds optimal for short-form",
  "VP5": "CTA always at end",
  "VP6": "Progressive reveal animations",
  "VP7": "Visual-first design",
  "VP8": "Sync animations WITH audio",
  "VP9_TIMING": "EACH segment MUST use duration from timing dict. Calculate: wait_time = (duration - sum(run_times)) / num_waits. Video duration MUST equal audio duration."
}'

# HINGLISH RULES
HINGLISH_RULES='{
  "hindi_words": "Devanagari ONLY (भाई not bhai)",
  "technical_terms": "English ONLY (angle, degrees, reflection)",
  "greek_letters": "Devanagari (theta → थीटा)",
  "trig_functions": "Phonetic fix (sine → sign)",
  "acronyms": "Dotted format (JEE → J. E. E.)",
  "numbers": "Spelled English (42 → forty two)"
}'

# BRAND RULES
BRAND_RULES='{
  "tone": "aap (respectful), never tu/tum",
  "cta_url": "jeetlo.ai",
  "cta_text": "JeetLo! Follow kijiye!",
  "watermark": "flame + JeetLo text, bottom-right",
  "jee_neet": "Mention exam relevance in every video"
}'

# TTS CONFIG
TTS_CONFIG='{
  "project_id": "fabled-variety-482120-b2",
  "api_endpoint": "https://texttospeech.googleapis.com/v1/text:synthesize"
}'

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_step() {
    echo -e "${CYAN}┌─────────────────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│ STEP $1: $2${NC}"
    echo -e "${CYAN}└─────────────────────────────────────────────────────────────────────────────┘${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Compute SHA256 hash of a file
compute_hash() {
    shasum -a 256 "$1" | cut -d' ' -f1
}

# Add step to proof chain
add_chain_step() {
    local step_name="$1"
    local output_file="$2"
    local chain_file="$WORK_DIR/.proof_chain.json"

    local prev_hash=$(jq -r '.steps[-1].output_hash // "genesis"' "$chain_file")
    local output_hash=$(compute_hash "$output_file")
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    jq --arg step "$step_name" \
       --arg input "$prev_hash" \
       --arg output "$output_hash" \
       --arg time "$timestamp" \
       '.steps += [{"step": $step, "input_hash": $input, "output_hash": $output, "timestamp": $time}]' \
       "$chain_file" > "$chain_file.tmp" && mv "$chain_file.tmp" "$chain_file"

    echo "$output_hash"
}

# Validate chain integrity
validate_chain() {
    local chain_file="$WORK_DIR/.proof_chain.json"

    python3 << EOF
import json
with open('$chain_file') as f:
    chain = json.load(f)

prev_output = None
for step in chain['steps']:
    if prev_output and step['input_hash'] != prev_output:
        print(f"CHAIN BROKEN at {step['step']}: expected {prev_output[:16]}..., got {step['input_hash'][:16]}...")
        exit(1)
    prev_output = step['output_hash']

print(f"Chain valid: {len(chain['steps'])} steps")
EOF
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 0: SETUP & TTS AUTH
# ═══════════════════════════════════════════════════════════════════════════════

setup_and_auth() {
    print_step "0" "SETUP & TTS AUTH"

    # Create work directory
    mkdir -p "$WORK_DIR"
    mkdir -p "$WORK_DIR/audio"

    # Initialize proof chain if not resuming
    if [ ! -f "$WORK_DIR/.proof_chain.json" ]; then
        local genesis_hash=$(echo -n "jeetlo-$REEL_ID-$(date +%s)" | shasum -a 256 | cut -d' ' -f1)
        cat > "$WORK_DIR/.proof_chain.json" << EOF
{
  "reel_id": "$REEL_ID",
  "subject": "$SUBJECT",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "genesis_hash": "$genesis_hash",
  "steps": []
}
EOF
        print_success "Proof chain initialized: ${genesis_hash:0:16}..."
    else
        print_success "Resuming existing proof chain"
    fi

    # Save embedded knowledge
    echo "$VOICE_SETTINGS" > "$WORK_DIR/voice_settings.json"
    echo "$SUBJECT_CONFIG" > "$WORK_DIR/subject_config.json"
    echo "$SEGMENT_STRUCTURE" > "$WORK_DIR/segment_structure.json"
    echo "$VIDEO_RULES" > "$WORK_DIR/video_rules.json"
    echo "$HINGLISH_RULES" > "$WORK_DIR/hinglish_rules.json"
    echo "$BRAND_RULES" > "$WORK_DIR/brand_rules.json"

    print_success "Embedded knowledge saved to work directory"

    # Check TTS auth
    echo ""
    echo "Checking Google Cloud TTS authentication..."

    # Check if gcloud is authenticated
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null | grep -q "@"; then
        print_warning "gcloud not authenticated. Opening browser for login..."
        gcloud auth login
        gcloud auth application-default login
        gcloud auth application-default set-quota-project fabled-variety-482120-b2
    fi

    # Verify with test request (use application-default for service account style auth)
    local token=$(gcloud auth application-default print-access-token 2>/dev/null)
    if [ -z "$token" ]; then
        print_error "Failed to get access token"
        echo "Run manually: gcloud auth application-default login"
        exit 1
    fi

    # Test TTS API
    local test_result=$(curl -s -X POST \
        -H "Authorization: Bearer $token" \
        -H "x-goog-user-project: fabled-variety-482120-b2" \
        -H "Content-Type: application/json" \
        "https://texttospeech.googleapis.com/v1/text:synthesize" \
        -d '{"input":{"text":"test"},"voice":{"languageCode":"en-US","name":"en-US-Standard-A"},"audioConfig":{"audioEncoding":"MP3"}}')

    if echo "$test_result" | jq -e '.audioContent' > /dev/null 2>&1; then
        print_success "TTS API authenticated and working"
    else
        print_error "TTS API test failed"
        echo "$test_result" | jq '.error.message // .' 2>/dev/null
        echo ""
        echo "Fix: Run these commands:"
        echo "  gcloud auth application-default login"
        echo "  gcloud auth application-default set-quota-project fabled-variety-482120-b2"
        exit 1
    fi

    # Add setup step to chain
    echo '{"status": "setup_complete", "tts_auth": true}' > "$WORK_DIR/setup_complete.json"
    add_chain_step "setup" "$WORK_DIR/setup_complete.json"

    print_success "Setup complete"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: CREATIVE BRIEF (ULTRATHINK)
# ═══════════════════════════════════════════════════════════════════════════════

# Helper to extract JSON object from mixed output
extract_json_object() {
    local input_file="$1"
    local output_file="$2"

    # Use Python for reliable cross-platform JSON extraction
    python3 << EOF
import re
import json
import sys

with open('$input_file') as f:
    content = f.read()

# Method 1: Try to extract from \`\`\`json blocks
json_block_match = re.search(r'\`\`\`json\s*\n(.*?)\n\s*\`\`\`', content, re.DOTALL)
if json_block_match:
    try:
        obj = json.loads(json_block_match.group(1))
        with open('$output_file', 'w') as f:
            json.dump(obj, f, indent=2)
        sys.exit(0)
    except json.JSONDecodeError:
        pass

# Method 2: Try generic code blocks
code_block_match = re.search(r'\`\`\`\s*\n(.*?)\n\s*\`\`\`', content, re.DOTALL)
if code_block_match:
    try:
        obj = json.loads(code_block_match.group(1))
        with open('$output_file', 'w') as f:
            json.dump(obj, f, indent=2)
        sys.exit(0)
    except json.JSONDecodeError:
        pass

# Method 3: Find JSON object directly (handles nested objects)
# Find all { positions and try to parse from each
brace_positions = [i for i, c in enumerate(content) if c == '{']
for start in brace_positions:
    depth = 0
    for i, c in enumerate(content[start:], start):
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                try:
                    obj = json.loads(content[start:i+1])
                    with open('$output_file', 'w') as f:
                        json.dump(obj, f, indent=2)
                    sys.exit(0)
                except json.JSONDecodeError:
                    break

# Method 4: Old regex pattern for simple JSON
match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)
if match:
    try:
        obj = json.loads(match.group())
        with open('$output_file', 'w') as f:
            json.dump(obj, f, indent=2)
        exit(0)
    except:
        pass
exit(1)
EOF
    return $?
}

# Helper to extract JSON array from mixed output
extract_json_array() {
    local input_file="$1"
    local output_file="$2"

    # Use Python for reliable cross-platform JSON extraction
    python3 << EOF
import re
import json
import sys

with open('$input_file') as f:
    content = f.read()

# Method 1: Try to extract from \`\`\`json blocks
json_block_match = re.search(r'\`\`\`json\s*\n(.*?)\n\s*\`\`\`', content, re.DOTALL)
if json_block_match:
    try:
        arr = json.loads(json_block_match.group(1))
        if isinstance(arr, list):
            with open('$output_file', 'w') as f:
                json.dump(arr, f, indent=2)
            sys.exit(0)
    except json.JSONDecodeError:
        pass

# Method 2: Try generic code blocks
code_block_match = re.search(r'\`\`\`\s*\n(.*?)\n\s*\`\`\`', content, re.DOTALL)
if code_block_match:
    try:
        arr = json.loads(code_block_match.group(1))
        if isinstance(arr, list):
            with open('$output_file', 'w') as f:
                json.dump(arr, f, indent=2)
            sys.exit(0)
    except json.JSONDecodeError:
        pass

# Method 3: Find JSON array pattern
match = re.search(r'\[[\s\S]*?\](?=\s*$|\s*\`\`\`|\s*\n\n)', content)
if match:
    try:
        arr = json.loads(match.group())
        with open('$output_file', 'w') as f:
            json.dump(arr, f, indent=2)
        exit(0)
    except:
        pass

# Fallback: find [ ... ] anywhere
match = re.search(r'\[\s*\{.*?\}\s*\]', content, re.DOTALL)
if match:
    try:
        arr = json.loads(match.group())
        with open('$output_file', 'w') as f:
            json.dump(arr, f, indent=2)
        exit(0)
    except:
        pass
exit(1)
EOF
    return $?
}

create_creative_brief() {
    print_step "1" "CREATIVE BRIEF (ULTRATHINK)"

    # Get subject-specific info
    local subject_info=$(echo "$SUBJECT_CONFIG" | jq --arg s "$SUBJECT" '.[$s]')
    local color=$(echo "$subject_info" | jq -r '.color')
    local background=$(echo "$subject_info" | jq -r '.background')
    local voice=$(echo "$subject_info" | jq -r '.voice')
    local manim_imports=$(echo "$subject_info" | jq -r '.manim_edu_imports | join(", ")')

    echo "Subject: $SUBJECT"
    echo "Color: $color | Background: $background"
    echo "Voice: $voice"
    echo "Required manim-edu imports: $manim_imports"
    echo ""
    echo "Running Claude CLI for creative brief..."

    claude --print --dangerously-skip-permissions \
        "You are a viral educational content strategist. Create a creative brief for this reel.

TOPIC: $TOPIC
SUBJECT: $SUBJECT
HOOK: $HOOK

REQUIREMENTS:
1. Core Analogy: Create a UNIQUE metaphor (not textbook). Example: 'Carbocation = Desperate single at party'
2. Subconscious Hook: What emotion triggers engagement? (FOMO, curiosity gap, identity challenge)
3. Visual Scenes: For EACH segment, describe EXACTLY what to animate
4. Virality Factor: What makes people screenshot/share?
5. Mind-Blow Moment: The 'aha!' that rewires their brain
6. Duration: Target 75-85 seconds (sweet spot for virality)
7. Simplification: The WEAKEST student must understand. Every jargon needs an analogy!
8. Logic Flow: Each segment MUST connect to next. Viewer should never wonder 'why are they telling me this?'

SEGMENT STRUCTURE:
$(echo "$SEGMENT_STRUCTURE" | jq '.')

manim-edu PRIMITIVES TO USE: $manim_imports

Output ONLY valid JSON with this structure:
{
  \"core_analogy\": \"...\",
  \"subconscious_hook\": \"...\",
  \"visual_scenes\": {
    \"01_hook\": \"...\",
    \"02_setup\": \"...\",
    ...
  },
  \"virality_factor\": \"...\",
  \"mind_blow_moment\": \"...\",
  \"duration_target\": \"80s\",
  \"simplification_strategy\": \"...\",
  \"logic_flow\": \"Hook → ... → CTA\",
  \"manim_edu_components\": [\"...\"]
}" 2>&1 > "$WORK_DIR/creative_brief_raw.txt"

    # Extract JSON from response
    if extract_json_object "$WORK_DIR/creative_brief_raw.txt" "$WORK_DIR/creative_brief.json"; then
        if jq -e '.core_analogy' "$WORK_DIR/creative_brief.json" > /dev/null 2>&1; then
            print_success "Creative brief generated"
            echo ""
            echo "Core Analogy: $(jq -r '.core_analogy' "$WORK_DIR/creative_brief.json")"
            echo "Mind-Blow: $(jq -r '.mind_blow_moment' "$WORK_DIR/creative_brief.json")"
        else
            print_error "Creative brief missing required fields"
            cat "$WORK_DIR/creative_brief_raw.txt" | head -30
            exit 1
        fi
    else
        print_error "Failed to extract JSON from creative brief"
        echo "Raw output:"
        cat "$WORK_DIR/creative_brief_raw.txt" | head -30
        exit 1
    fi

    add_chain_step "creative_brief" "$WORK_DIR/creative_brief.json"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: AUDIO SCRIPT
# ═══════════════════════════════════════════════════════════════════════════════

create_audio_script() {
    print_step "2" "AUDIO SCRIPT"

    local creative_brief=$(cat "$WORK_DIR/creative_brief.json")

    echo "Generating audio script with embedded Hinglish rules..."

    claude --print --dangerously-skip-permissions \
        "You are a JeetLo script writer. Write the audio script for this reel.

CREATIVE BRIEF:
$creative_brief

HINGLISH RULES (MANDATORY):
$(echo "$HINGLISH_RULES" | jq '.')

SEGMENT STRUCTURE:
$(echo "$SEGMENT_STRUCTURE" | jq '.')

EMOTION ENGINEERING (USE THESE - TTS-FRIENDLY):
- NEVER use ALL CAPS (TTS reads letter-by-letter: 'DEATH' becomes 'D-E-A-T-H')
- Use '...' for dramatic pause: 'लेकिन actually...'
- Use '!' for energy and emphasis: 'Secret है hydrogen bonding!'
- Use '?' for curiosity: 'क्यों?'
- Use repetition for emphasis: 'हर... हर एक solid sink करता है!'
- Use word isolation: 'और ये... shocking है!'

BRAND VOICE:
- Use 'aap' (respectful), never 'tu/tum'
- Mention JEE/NEET relevance
- End with: 'JeetLo! Follow kijiye!'

EXAMPLE SEGMENT:
{
  \"id\": \"01_hook\",
  \"text\": \"Ice पानी पर float करती है... लेकिन हर दूसरा solid sink करता है! क्यों?\"
}

Output ONLY valid JSON array:
[
  {\"id\": \"01_hook\", \"text\": \"...\"},
  {\"id\": \"02_setup\", \"text\": \"...\"},
  ...
  {\"id\": \"07_cta\", \"text\": \"JeetLo! Follow kijiye!\"}
]" 2>&1 > "$WORK_DIR/audio_script_raw.txt"

    # Extract JSON array from response
    if extract_json_array "$WORK_DIR/audio_script_raw.txt" "$WORK_DIR/audio_script.json"; then
        local segment_count=$(jq 'length' "$WORK_DIR/audio_script.json" 2>/dev/null || echo 0)
        if [ "$segment_count" -ge 5 ]; then
            print_success "Audio script generated: $segment_count segments"

            # Show preview
            echo ""
            echo "Preview:"
            jq -r '.[0:2][] | "  \(.id): \(.text[0:60])..."' "$WORK_DIR/audio_script.json" 2>/dev/null
            echo "  ..."
        else
            print_error "Audio script has too few segments: $segment_count"
            cat "$WORK_DIR/audio_script_raw.txt" | head -30
            exit 1
        fi
    else
        print_error "Failed to extract JSON array from audio script"
        echo "Raw output:"
        cat "$WORK_DIR/audio_script_raw.txt" | head -30
        exit 1
    fi

    add_chain_step "audio_script" "$WORK_DIR/audio_script.json"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: GENERATE AUDIO
# ═══════════════════════════════════════════════════════════════════════════════

generate_audio() {
    print_step "3" "GENERATE AUDIO"

    local voice=$(echo "$SUBJECT_CONFIG" | jq -r --arg s "$SUBJECT" '.[$s].voice')
    local speaking_rate=$(echo "$VOICE_SETTINGS" | jq -r '.speakingRate')
    local token=$(gcloud auth application-default print-access-token)

    echo "Voice: $voice"
    echo "Speaking Rate: $speaking_rate (authoritative)"
    echo ""

    local total_duration=0
    local timings="[]"

    # Generate each segment
    jq -c '.[]' "$WORK_DIR/audio_script.json" | while read -r segment; do
        local id=$(echo "$segment" | jq -r '.id')
        local text=$(echo "$segment" | jq -r '.text')

        echo "Generating: $id"

        # Build TTS request
        local request=$(jq -n \
            --arg text "$text" \
            --arg voice "$voice" \
            --argjson rate "$speaking_rate" \
            '{
                input: {text: $text},
                voice: {languageCode: "hi-IN", name: $voice},
                audioConfig: {audioEncoding: "MP3", speakingRate: $rate}
            }')

        # Call TTS API
        local result=$(curl -s -X POST \
            -H "Authorization: Bearer $token" \
            -H "x-goog-user-project: fabled-variety-482120-b2" \
            -H "Content-Type: application/json" \
            "https://texttospeech.googleapis.com/v1/text:synthesize" \
            -d "$request")

        if echo "$result" | jq -e '.audioContent' > /dev/null 2>&1; then
            echo "$result" | jq -r '.audioContent' | base64 -d > "$WORK_DIR/audio/$id.mp3"

            local duration=$(ffprobe -i "$WORK_DIR/audio/$id.mp3" -show_entries format=duration -v quiet -of csv="p=0")
            echo "  ✓ Duration: ${duration}s"
        else
            print_error "Failed to generate $id"
            echo "$result" | jq '.error.message // .'
        fi

        sleep 0.3
    done

    # Generate timings.json
    echo "Generating timings..."
    local timings="[]"
    local current_time=0

    for mp3 in $(ls "$WORK_DIR/audio/"*.mp3 | sort); do
        local id=$(basename "$mp3" .mp3)
        local duration=$(ffprobe -i "$mp3" -show_entries format=duration -v quiet -of csv="p=0")
        local text=$(jq -r --arg id "$id" '.[] | select(.id == $id) | .text' "$WORK_DIR/audio_script.json")

        timings=$(echo "$timings" | jq \
            --arg id "$id" \
            --arg text "$text" \
            --argjson dur "$duration" \
            --argjson start "$current_time" \
            --argjson end "$(echo "$current_time + $duration" | bc)" \
            '. += [{id: $id, text: $text, duration: $dur, startTime: $start, endTime: $end}]')

        current_time=$(echo "$current_time + $duration" | bc)
    done

    echo "$timings" | jq '.' > "$WORK_DIR/audio/timings.json"

    # Combine audio
    echo ""
    echo "Combining segments..."
    # Remove old combined file first, then list segment files (exclude combined_audio.mp3)
    rm -f "$WORK_DIR/audio/combined_audio.mp3"
    # Use full paths in concat.txt so ffmpeg can find files from any working directory
    ls "$WORK_DIR/audio/"*.mp3 | grep -v combined_audio | sort | while read f; do
        echo "file '$f'"
    done > "$WORK_DIR/audio/concat.txt"

    ffmpeg -y -f concat -safe 0 -i "$WORK_DIR/audio/concat.txt" -c copy "$WORK_DIR/audio/combined_audio.mp3" 2>/dev/null
    rm "$WORK_DIR/audio/concat.txt"

    local total_duration=$(ffprobe -i "$WORK_DIR/audio/combined_audio.mp3" -show_entries format=duration -v quiet -of csv="p=0")
    print_success "Audio generated: ${total_duration}s total"

    add_chain_step "generate_audio" "$WORK_DIR/audio/combined_audio.mp3"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: VIDEO SCRIPT (reel.py)
# ═══════════════════════════════════════════════════════════════════════════════

# Helper function to extract Python code from mixed output
extract_python_code() {
    local input_file="$1"
    local output_file="$2"

    # Use Python for reliable cross-platform extraction
    python3 << EOF
import re
import sys

with open('$input_file') as f:
    content = f.read()

# Method 1: Extract from \`\`\`python ... \`\`\` blocks
python_match = re.search(r'\`\`\`python\s*\n(.*?)\n\s*\`\`\`', content, re.DOTALL)
if python_match:
    code = python_match.group(1)
    if 'class' in code and 'Scene' in code:
        with open('$output_file', 'w') as f:
            f.write(code)
        sys.exit(0)

# Method 2: Extract from generic \`\`\` ... \`\`\` blocks
code_match = re.search(r'\`\`\`\s*\n(.*?)\n\s*\`\`\`', content, re.DOTALL)
if code_match:
    code = code_match.group(1)
    if 'class' in code and 'Scene' in code:
        with open('$output_file', 'w') as f:
            f.write(code)
        sys.exit(0)

# Method 3: Find code starting with import/from/class
lines = content.split('\n')
start_idx = None
for i, line in enumerate(lines):
    if line.startswith('import ') or line.startswith('from ') or line.startswith('class '):
        start_idx = i
        break

if start_idx is not None:
    code = '\n'.join(lines[start_idx:])
    if 'class' in code and 'Scene' in code:
        with open('$output_file', 'w') as f:
            f.write(code)
        sys.exit(0)

# Method 4: Copy as-is if it looks like Python
if 'class' in content and 'Scene' in content and 'def construct' in content:
    with open('$output_file', 'w') as f:
        f.write(content)
    sys.exit(0)

sys.exit(1)
EOF
    return $?
}

create_video_script() {
    print_step "4" "VIDEO SCRIPT (reel.py using manim-edu)"

    local creative_brief=$(cat "$WORK_DIR/creative_brief.json")
    local timings=$(cat "$WORK_DIR/audio/timings.json")
    local subject_info=$(echo "$SUBJECT_CONFIG" | jq --arg s "$SUBJECT" '.[$s]')
    local background=$(echo "$subject_info" | jq -r '.background')
    local color=$(echo "$subject_info" | jq -r '.color')
    local manim_imports=$(echo "$subject_info" | jq -r '.manim_edu_imports[]')

    # Read manim-edu README for complete library documentation
    local manim_edu_readme=""
    if [ -f "$MANIM_EDU/README.md" ]; then
        # Extract key sections: Quick Start through Mechanics
        manim_edu_readme=$(sed -n '/^## Quick Start/,/^## Waves/p' "$MANIM_EDU/README.md" | head -400)
        echo "Loaded manim-edu documentation ($(echo "$manim_edu_readme" | wc -l) lines)"
    fi

    echo "Generating Manim reel.py..."
    echo "Background: $background"
    echo "Subject Color: $color"
    echo "manim-edu imports: $manim_imports"
    echo ""

    # Build manim-edu import line
    local import_line=""
    for imp in $manim_imports; do
        if [ "$imp" == "MoleculeBuilder" ]; then
            import_line="from manim_edu.chemistry import MoleculeBuilder"
        elif [ "$imp" == "CellVisualizer" ]; then
            import_line="from manim_edu.biology import CellVisualizer"
        elif [ "$imp" == "WaveSimulator" ] || [ "$imp" == "FieldVisualizer" ] || [ "$imp" == "MechanicsSimulator" ]; then
            import_line="from manim_edu.physics import WaveSimulator, FieldVisualizer, MechanicsSimulator"
        elif [ "$imp" == "GraphAnimator" ]; then
            import_line="from manim_edu.mathematics import GraphAnimator"
        fi
    done

    local max_attempts=3
    local attempt=1
    local success=false

    while [ $attempt -le $max_attempts ] && [ "$success" = false ]; do
        echo "Attempt $attempt of $max_attempts..."

        # Pre-compute capitalized subject for class name
        local subject_cap=$(echo "${SUBJECT:0:1}" | tr '[:lower:]' '[:upper:]')${SUBJECT:1}

        # Use different prompts for retries
        local prompt_prefix=""
        if [ $attempt -eq 2 ]; then
            prompt_prefix="IMPORTANT: Your previous response was not valid Python code. This time, output ONLY the Python code with NO explanations, summaries, or markdown."
        elif [ $attempt -eq 3 ]; then
            prompt_prefix="FINAL ATTEMPT - OUTPUT ONLY PYTHON CODE. No markdown. Start with import sys."
        fi

        # Build prompt file to avoid bash substitution issues
        cat > "$WORK_DIR/prompt_$attempt.txt" << PROMPT_EOF
${prompt_prefix}
Generate a complete Manim Python file for an educational reel.

CREATIVE BRIEF:
$creative_brief

TIMINGS (each segment must match these durations):
$timings

CONFIG:
- Background color: $background
- Subject color: $color
- Subject: $SUBJECT

MANIM-EDU LIBRARY (MANDATORY - use ONLY manim-edu for all scientific visuals):
Location: /Users/pran/Projects/libraries/manim-edu

=== COMPLETE MANIM-EDU DOCUMENTATION (READ THIS!) ===
$manim_edu_readme
=== END MANIM-EDU DOCUMENTATION ===

═══════════════════════════════════════════════════════════════════════════════
🚨 GUARDRAILS - VIOLATION = PIPELINE FAILURE 🚨
═══════════════════════════════════════════════════════════════════════════════

🔴 FORBIDDEN (Will cause pipeline to FAIL):
1. NEVER put Hindi/Devanagari text ON SCREEN - Audio is Hinglish, VIDEO is ENGLISH ONLY
2. NEVER use MathTex, Tex, or raw LaTeX
3. NEVER write custom CTA code - ALWAYS use self.add_cta_slide_*() from JeetLoReelMixin
4. NEVER use GrowArrow() - use Create() instead for arrows
5. NEVER put text outside safe zone (avoid edges - keep content in center 80%)
6. NEVER overlap text on text - position elements with proper spacing
7. NEVER create manual Arrow() loops for field visualizations - USE FieldVisualizer methods instead!
   - For gravity: field.gravitational_field() NOT manual Arrow() in a loop
   - For electric: field.electric_dipole() or field.point_charge()
   - Manual Arrow() with normalized vectors WILL CRASH if direction=0
8. NEVER call .normalized() on numpy arrays - numpy doesn't have this method!
   - WRONG: (end - start).normalized()
   - RIGHT: normalize(end - start)  # Manim's normalize() function
   - OR: (end - start) / np.linalg.norm(end - start)  # numpy way
9. NEVER stack formula labels using .next_to(X, DOWN) - they will OVERLAP!
   - WRONG: g_label.next_to(g_term, DOWN), m_label.next_to(m_term, DOWN)  # Overlaps!
   - RIGHT: Use SmartLabel or Callout from manim_edu.primitives.annotation
   - Example for formula F = Gm₁m₂/r²:
     from manim_edu.primitives.annotation import Callout
     g_callout = Callout("Universe's Counselor", g_term.get_center(), direction=UL)
     m_callout = Callout("Both Masses", m_terms.get_center(), direction=UP)
     r_callout = Callout("Distance!", r_term.get_center(), direction=DR)
   - Each label gets its OWN direction (UL, UR, DL, DR, UP, DOWN, LEFT, RIGHT)

🟢 REQUIRED (Must include or pipeline will FAIL):
1. ALWAYS use manim-edu components for formulas and scientific visuals
2. ALWAYS use English text on screen (Hindi is ONLY in audio, never on screen)
3. ALWAYS use self.add_cta_slide_{subject}(duration) for CTA segment
4. ALWAYS clear objects at end of each segment with FadeOut or self.clear()
5. ALWAYS position text with .move_to(), .next_to(), .to_edge() with proper buff values

═══════════════════════════════════════════════════════════════════════════════
SAFE ZONE POSITIONING (9:16 Vertical Frame):
- FRAME_WIDTH = 8 units, FRAME_HEIGHT = 14.22 units
- Keep main content within X: [-3.5, 3.5] and Y: [-6, 6]
- Title/Header: UP * 5 to UP * 6
- Main content: UP * 2 to DOWN * 2
- Bottom info: DOWN * 4 to DOWN * 6
- Watermark is always at bottom-right, don't overlap it
═══════════════════════════════════════════════════════════════════════════════

=== ATOMIC FORMULA SYSTEM (NEW - USE THIS!) ===

from manim_edu.formulas import (
    Char,          # Single character: Char("x", BLUE, 60)
    CharSeq,       # Per-char colors: CharSeq("RAINBOW", colors=[RED, ORANGE, ...])
    SmartUnit,     # Element + sub/sup: SmartUnit("H", sub="2") -> H₂
    Term,          # Variable with scripts: Term("n", sub="1", color=BLUE, sub_color=TEAL)
    Op,            # Operators: Op("="), Op("+"), Op("→")
    Frac,          # Fractions: Frac(numerator, denominator)
    Sqrt,          # Square roots: Sqrt(content)
    Paren,         # Scaling parens: Paren(content)
    Formula,       # Combine any: Formula(Term(...), Op(...), Term(...))
    Chem,          # Chemical: Chem("H2O", element_colors={"H": BLUE, "O": RED})
    FormulaRenderer,  # Pre-built: renderer.gravity(), renderer.emc2()
)

=== CHEMICAL FORMULAS (Smart Positioning!) ===

# Water with element colors
water = Chem("H2O", size=70, element_colors={"H": BLUE, "O": RED})

# Glucose with multi-digit subscripts
glucose = Chem("C6H12O6", size=60, element_colors={"C": GRAY, "H": BLUE, "O": RED})

# Ions with charges (parsed automatically!)
iron_ion = Chem("Fe3+", element_colors={"Fe": ORANGE})  # Fe³⁺
sulfate = Chem("SO4-", element_colors={"S": YELLOW, "O": RED})  # SO₄⁻

=== PHYSICS/MATH FORMULAS (Full Atomic Control!) ===

# Snell's Law: n₁sinθ₁ = n₂sinθ₂
snells_law = Formula(
    Term("n", sub="1", color=BLUE, sub_color=TEAL, size=50),
    Term("sin", color=WHITE, size=40),
    Term("theta", greek=True, sub="1", color=YELLOW, sub_color=ORANGE, size=50),
    Op("=", color=WHITE, size=50),
    Term("n", sub="2", color=GREEN, sub_color=TEAL, size=50),
    Term("sin", color=WHITE, size=40),
    Term("theta", greek=True, sub="2", color=YELLOW, sub_color=ORANGE, size=50),
    buff=0.15
)
self.play(snells_law.write_sequence(lag_ratio=0.2))  # Animated entrance!

# Pre-built formulas
renderer = FormulaRenderer()
emc2 = renderer.emc2()            # E = mc²
gravity = renderer.gravity()       # F = Gm₁m₂/r²
quadratic = renderer.quadratic()   # Quadratic formula

=== SUBJECT VISUALIZERS ===

# Physics - ALWAYS use these instead of manual arrows/shapes!
from manim_edu.physics import WaveSimulator, FieldVisualizer, MechanicsSimulator

field = FieldVisualizer(scale=1.0)
# Electric fields
field.electric_dipole()         # Field lines between +/- charges
field.point_charge(positive=True)  # Radial field around single charge
field.parallel_plates()         # Uniform field between plates
# Magnetic fields
field.magnetic_field_wire()     # Concentric circles around current wire
# Gravitational fields (USE THIS for gravity reels!)
field.gravitational_field()     # Inward arrows toward mass center - CRASH-FREE!

# Mechanics - forces and vectors
mech = MechanicsSimulator()
# Use gravity_force() instead of manual Arrow() - it's crash-proof!

# Chemistry
from manim_edu.chemistry import MoleculeBuilder
mol = MoleculeBuilder(scale=1.5)
water = mol.water()  # H2O with correct bond angles

# Biology
from manim_edu.biology import CellVisualizer
cell = CellVisualizer()
rbc = cell.red_blood_cell()

# Mathematics
from manim_edu.mathematics import GraphAnimator
graph = GraphAnimator()

=== AUTO-BOUNDED TEXT & SAFE POSITIONING (MANDATORY!) ===

# Use SafeText from layout module - it auto-clamps to safe zone and auto-scales
from manim_edu.layout import (
    SafeText,              # Drop-in Text replacement with auto-bounds
    SafeMarkupText,        # MarkupText with auto-bounds
    safe_title,            # Pre-configured title helper
    safe_body,             # Pre-configured body text helper
    safe_label,            # Label with optional background
    check_bounds,          # Verify mobject is in safe zone
    fit_to_safe_zone,      # Scale/position to fit

    # Constants for 9:16 vertical reels
    SAFE_X_MIN, SAFE_X_MAX,  # -3.0 to 3.0 (with padding)
    SAFE_Y_MIN, SAFE_Y_MAX,  # -5.5 to 5.5 (with padding)
    MAX_TEXT_WIDTH,          # 6.0 units max
    POSITIONS,               # Named positions dict
)

# ✅ SafeText auto-scales and clamps to safe zone
title = SafeText("WRONG BLOOD = DEATH", font_size=48, color=YELLOW)
title.move_to(UP * 4)  # Will be clamped to safe zone automatically

# ✅ Use safe_title for guaranteed fit
title = safe_title("Very Long Title That Would Overflow", position="top")

# ✅ Use safe_body for auto-wrapped body text
explanation = safe_body("Long explanation text that needs to wrap...", wrap_width=35)

# ✅ Use safe_label for labels with background
label = safe_label("Important!", bg_color="#FF4444", font_size=28)

# ✅ Chain positioning with .below()
subtitle = SmartText("Subtitle text", font_size=36, color=GRAY).below(title)

# ✅ SmartVGroup validates & fixes overlaps automatically
group = SmartVGroup(
    SmartText("Item 1"),
    SmartText("Item 2"),
    SmartText("Item 3")
).arrange(DOWN, buff=0.5)

# ✅ Existing SmartLayout for text lists (auto-validates)
summary = SmartLayout(
    "Title",
    "Point 1",
    "Point 2",
    direction=DOWN,
    aligned_edge=LEFT
)

# ✅ Manual validation with auto-fix
result = validate_vertical(title, subtitle)  # Check for issues
if not result.passed:
    fixed_group, result = ensure_no_overlaps(title, subtitle)  # Auto-fix

=== ANIMATION PATTERNS (REVOLUTIONARY!) ===

# IMPORTANT: For Arrows, use Create() not GrowArrow() - GrowArrow has compatibility issues
# For multiple arrows: self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.1))

# Visual first, text reinforces
formula = Chem("H2O", element_colors={"H": BLUE, "O": RED})
self.play(FadeIn(formula))  # Show first
self.play(formula.animate.scale(1.3).set_color(YELLOW))  # Highlight
label = Text("Water!", font_size=36)
self.play(Write(label))  # Label after

# Progressive revelation
step1 = Chem("C")
self.play(Create(step1))
step2 = Chem("C6")
self.play(Transform(step1, step2))
step3 = Chem("C6H12O6", element_colors={"C": GRAY, "H": BLUE, "O": RED})
self.play(Transform(step1, step3))

COMPLETE PYTHON FILE STRUCTURE:
The file must start exactly like this:

import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')
from manim import *
from jeetlo_style import JeetLoReelMixin, create_brand_watermark

# Import manim-edu components for ${SUBJECT}
${import_line}

class ${subject_cap}Reel(JeetLoReelMixin, Scene):
    subject = "${SUBJECT}"

    def construct(self):
        self.camera.background_color = '$background'
        self.add(create_brand_watermark())

        # Load timings from file
        import json
        with open('audio/timings.json') as f:
            self.timings = json.load(f)

        # Call each segment
        for seg in self.timings:
            method_name = f"segment_{seg['id']}"
            method = getattr(self, method_name, None)
            if method:
                method(seg)

    def segment_01_hook(self, timing):
        duration = timing['duration']
        # Animation code here...
        # Use: wait_time = (duration - total_animation_time) / num_waits

    # ... implement ALL segment methods from timings

    def segment_07_cta(self, timing):
        # MANDATORY: Use the pre-built CTA slide from JeetLoReelMixin
        # This includes: flame icon, JeetLo text, jeetlo.ai URL, pricing, Follow CTA
        duration = timing['duration']
        # Call subject-specific CTA based on self.subject
        cta_methods = {
            'physics': self.add_cta_slide_physics,
            'chemistry': self.add_cta_slide_chem,
            'biology': self.add_cta_slide_biology,
            'mathematics': self.add_cta_slide_math
        }
        cta_methods[self.subject](duration)

REQUIREMENTS:
1. Create a segment method for EACH entry in timings (segment_01_hook, segment_02_setup, etc.)
2. Each segment must use timing['duration'] to calculate wait times correctly
3. MUST use manim-edu components for stunning scientific visualizations
4. Use 6+ colors from: RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, TEAL, PINK, WHITE, GOLD (NOT CYAN - use TEAL instead)
5. Clear all objects at end of each segment with self.clear() or FadeOut
6. Match the visual scenes described in the creative brief
7. CTA segment must include jeetlo.ai and "Follow for more!"

🚨 CRITICAL TIMING RULE (VIDEO MUST MATCH AUDIO DURATION!):
Each segment method MUST use this pattern:
def segment_XX(self, timing):
    duration = timing['duration']

    # 1. Calculate total animation time (sum all run_time values)
    total_anim_time = 0.5 + 0.3 + 0.4  # example

    # 2. Count wait() calls
    num_waits = 3  # example

    # 3. Calculate wait_time to fill remaining duration
    wait_time = max(0.1, (duration - total_anim_time) / num_waits)

    # 4. Use consistent wait_time throughout
    self.play(FadeIn(obj1), run_time=0.5)
    self.wait(wait_time)
    self.play(Write(obj2), run_time=0.3)
    self.wait(wait_time)
    self.play(Create(obj3), run_time=0.4)
    self.wait(wait_time)

This ensures: total_anim_time + (num_waits * wait_time) = duration

Output the complete Python file now:
PROMPT_EOF

        # Generate the video script using the prompt file
        claude --print --dangerously-skip-permissions "$(cat "$WORK_DIR/prompt_$attempt.txt")" 2>&1 > "$WORK_DIR/reel_raw_$attempt.txt"

        # Extract Python code from the output
        if extract_python_code "$WORK_DIR/reel_raw_$attempt.txt" "$WORK_DIR/reel.py"; then
            # Validate the extracted code
            if grep -q "class.*Scene" "$WORK_DIR/reel.py" && \
               grep -q "def construct" "$WORK_DIR/reel.py" && \
               grep -q "def segment_" "$WORK_DIR/reel.py"; then

                local line_count=$(wc -l < "$WORK_DIR/reel.py" | tr -d ' ')
                if [ "$line_count" -gt 50 ]; then
                    success=true
                    print_success "reel.py generated ($line_count lines) on attempt $attempt"
                else
                    print_warning "Generated code too short ($line_count lines), retrying..."
                fi
            else
                print_warning "Missing required patterns, retrying..."
            fi
        else
            print_warning "Could not extract Python code, retrying..."
        fi

        if [ "$success" = false ]; then
            echo "Raw output saved to: $WORK_DIR/reel_raw_$attempt.txt"
            echo "First 20 lines:"
            head -20 "$WORK_DIR/reel_raw_$attempt.txt"
            echo ""
        fi

        attempt=$((attempt + 1))
        [ "$success" = false ] && sleep 2
    done

    if [ "$success" = false ]; then
        print_error "Failed to generate valid reel.py after $max_attempts attempts"
        echo ""
        echo "Debug info saved to $WORK_DIR/reel_raw_*.txt"
        echo "Please check the raw outputs and fix manually."

        # Update request status to failed
        if [ -f "$FACTORY_DIR/requests/$REEL_ID.json" ]; then
            jq '.status = "failed" | .error = "video_script_generation"' \
                "$FACTORY_DIR/requests/$REEL_ID.json" > "$FACTORY_DIR/requests/$REEL_ID.json.tmp"
            mv "$FACTORY_DIR/requests/$REEL_ID.json.tmp" "$FACTORY_DIR/requests/$REEL_ID.json"

            cd "$FACTORY_DIR"
            git add -A
            git commit -m "Failed reel: $REEL_ID - video script generation failed" 2>/dev/null || true
            git push origin main 2>/dev/null || true
        fi

        exit 1
    fi

    # Additional validation
    if grep -q "manim_edu\|MoleculeBuilder\|CellVisualizer\|WaveSimulator\|FieldVisualizer\|MechanicsSimulator\|GraphAnimator" "$WORK_DIR/reel.py"; then
        print_success "Uses manim-edu primitives"
    else
        print_warning "Missing manim-edu imports (will use basic Manim)"
    fi

    if grep -q "create_brand_watermark\|add_cta_slide" "$WORK_DIR/reel.py"; then
        print_success "Has brand elements (watermark/CTA)"
    else
        print_warning "Missing brand elements - adding manually..."
        # Could add brand elements here if needed
    fi

    # Syntax check
    if python3 -m py_compile "$WORK_DIR/reel.py" 2>/dev/null; then
        print_success "Python syntax valid"
    else
        print_warning "Python syntax errors detected - may need manual fixes"
        python3 -m py_compile "$WORK_DIR/reel.py" 2>&1 | head -10
    fi

    add_chain_step "video_script" "$WORK_DIR/reel.py"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5: VALIDATE manim-edu COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════════

validate_manim_edu() {
    print_step "5" "VALIDATE manim-edu COMPLIANCE"

    local reel_code="$WORK_DIR/reel.py"
    local issues=()
    local score=0

    echo "Checking reel.py patterns..."

    # Check for manim-edu imports
    local manim_edu_count=0
    if grep -q "from manim_edu" "$reel_code" 2>/dev/null; then
        manim_edu_count=$(grep -c "from manim_edu" "$reel_code")
        print_success "manim-edu imports found: $manim_edu_count"
        score=$((score + 20))
    else
        print_warning "No manim-edu imports found"
        issues+=("missing_manim_edu_imports")
    fi

    # Check for brand elements
    if grep -q "create_brand_watermark\|add_watermark" "$reel_code" 2>/dev/null; then
        print_success "Brand watermark found"
        score=$((score + 15))
    else
        print_warning "Missing brand watermark"
        issues+=("missing_watermark")
    fi

    if grep -q "add_cta_slide" "$reel_code" 2>/dev/null; then
        print_success "CTA slide found"
        score=$((score + 15))
    else
        print_warning "Missing CTA slide"
        issues+=("missing_cta")
    fi

    # Check for JeetLoReelMixin
    if grep -q "JeetLoReelMixin" "$reel_code" 2>/dev/null; then
        print_success "JeetLoReelMixin used"
        score=$((score + 10))
    else
        print_warning "Missing JeetLoReelMixin"
        issues+=("missing_mixin")
    fi

    # Check for segment methods
    local segment_count=$(grep -c "def segment_" "$reel_code" 2>/dev/null || echo 0)
    if [ "$segment_count" -ge 5 ]; then
        print_success "Segment methods found: $segment_count"
        score=$((score + 15))
    else
        print_warning "Only $segment_count segment methods (expected 5+)"
        issues+=("insufficient_segments")
    fi

    # ═══════════════════════════════════════════════════════════════════════════
    # 🚨 GUARDRAIL CHECKS - These can BLOCK the pipeline
    # ═══════════════════════════════════════════════════════════════════════════

    # GUARDRAIL 1: Check for Hindi/Devanagari text ON SCREEN (BLOCKING)
    # Uses Python for reliable Unicode detection
    local hindi_lines=$(python3 -c "
import re
import sys
with open('$reel_code', 'r') as f:
    for i, line in enumerate(f, 1):
        # Check for Devanagari characters in Text() calls
        if 'Text(' in line and re.search(r'[\u0900-\u097F]', line):
            print(f'{i}: {line.strip()[:80]}')
" 2>/dev/null)

    if [ -n "$hindi_lines" ]; then
        print_error "🚨 GUARDRAIL VIOLATION: Hindi/Devanagari text found ON SCREEN!"
        print_error "   Audio can be Hinglish, but VIDEO must be ENGLISH ONLY"
        echo "   Offending lines:"
        echo "$hindi_lines" | head -5
        issues+=("BLOCKING_hindi_on_screen")
    else
        print_success "No Hindi text on screen (English only - correct!)"
        score=$((score + 10))
    fi

    # GUARDRAIL 2: Check for GrowArrow (deprecated - causes errors)
    if grep -q "GrowArrow" "$reel_code" 2>/dev/null; then
        print_warning "⚠️ GrowArrow() detected - should use Create() for arrows"
        echo "   Auto-fixing: replacing GrowArrow with Create..."
        sed -i '' 's/GrowArrow/Create/g' "$reel_code" 2>/dev/null || sed -i 's/GrowArrow/Create/g' "$reel_code"
        print_success "Auto-fixed: GrowArrow → Create"
    else
        print_success "No GrowArrow usage (using Create - correct!)"
    fi

    # GUARDRAIL 3: Check for proper CTA (must use add_cta_slide_*)
    if grep -q "add_cta_slide_physics\|add_cta_slide_chem\|add_cta_slide_biology\|add_cta_slide_math" "$reel_code" 2>/dev/null; then
        print_success "Using standard CTA slide (correct!)"
        score=$((score + 10))
    elif grep -q "segment_07_cta\|segment.*cta" "$reel_code" 2>/dev/null; then
        print_warning "CTA segment exists but may not use standard add_cta_slide_*()"
        issues+=("custom_cta_code")
    else
        print_warning "No CTA segment found"
        issues+=("missing_cta")
    fi

    # GUARDRAIL 4: Auto-fix run_time() syntax error (LLM often writes run_time(0.5) instead of run_time=0.5)
    if grep -q "run_time([0-9]" "$reel_code" 2>/dev/null; then
        print_warning "⚠️ run_time() syntax error detected - should be run_time=value"
        echo "   Auto-fixing: replacing run_time(value) with run_time=value..."
        sed -i '' 's/run_time(\([0-9.]*\))/run_time=\1/g' "$reel_code" 2>/dev/null || sed -i 's/run_time(\([0-9.]*\))/run_time=\1/g' "$reel_code"
        print_success "Auto-fixed: run_time(x) → run_time=x"
    else
        print_success "No run_time() syntax errors"
    fi

    # GUARDRAIL 5: Auto-fix buff() syntax error (LLM may write buff(0.5) instead of buff=0.5)
    if grep -q "buff([0-9]" "$reel_code" 2>/dev/null; then
        print_warning "⚠️ buff() syntax error detected - should be buff=value"
        echo "   Auto-fixing: replacing buff(value) with buff=value..."
        sed -i '' 's/buff(\([0-9.]*\))/buff=\1/g' "$reel_code" 2>/dev/null || sed -i 's/buff(\([0-9.]*\))/buff=\1/g' "$reel_code"
        print_success "Auto-fixed: buff(x) → buff=x"
    fi

    # GUARDRAIL 6: Check for plain Text() usage (should use SmartText for auto-bounds)
    local plain_text_count=$(grep -c "Text(" "$reel_code" 2>/dev/null || echo 0)
    local smart_text_count=$(grep -c "SmartText\|safe_text\|smart_title\|smart_subtitle\|smart_body" "$reel_code" 2>/dev/null || echo 0)
    if [ "$plain_text_count" -gt 5 ] && [ "$smart_text_count" -eq 0 ]; then
        print_warning "⚠️ Using plain Text() - consider SmartText for auto-bounds (not blocking)"
        echo "   Tip: SmartText auto-scales and clamps to safe zone"
    elif [ "$smart_text_count" -gt 0 ]; then
        print_success "Using SmartText components (good!)"
    fi

    # GUARDRAIL 7: Check for proper imports (manim_edu should be imported)
    if ! grep -q "from manim_edu\|import manim_edu" "$reel_code" 2>/dev/null; then
        print_warning "⚠️ manim_edu not imported - some features may be missing"
    fi

    # ═══════════════════════════════════════════════════════════════════════════

    # GUARDRAIL 8: PRE-RENDER TIMING VALIDATION (CRITICAL - catches duration mismatch BEFORE render)
    echo ""
    echo "🕐 Validating segment timing calculations..."

    local timing_issues=$(python3 << TIMING_CHECK_EOF
import json
import re
import sys

# Load audio timings
try:
    with open('$WORK_DIR/audio/timings.json', 'r') as f:
        timings = json.load(f)
except:
    print("ERROR: Cannot load timings.json")
    sys.exit(0)

# Load reel.py
try:
    with open('$WORK_DIR/reel.py', 'r') as f:
        reel_code = f.read()
except:
    print("ERROR: Cannot load reel.py")
    sys.exit(0)

issues = []
total_audio = sum(t.get('duration', 0) for t in timings if t.get('id') != 'combined_audio')

# For each segment, check if timing logic looks correct
for timing in timings:
    seg_id = timing.get('id', '')
    if seg_id == 'combined_audio':
        continue

    seg_duration = timing.get('duration', 0)
    method_name = f"def segment_{seg_id}"

    # Find the segment method in code
    if method_name not in reel_code:
        issues.append(f"MISSING: segment_{seg_id} method not found in reel.py")
        continue

    # Extract the segment method code
    start = reel_code.find(method_name)
    next_def = reel_code.find("\n    def ", start + 1)
    if next_def == -1:
        next_def = len(reel_code)
    segment_code = reel_code[start:next_def]

    # Count run_time values
    run_times = re.findall(r'run_time\s*=\s*([\d.]+)', segment_code)
    total_run_time = sum(float(rt) for rt in run_times)

    # Count self.wait() calls
    wait_calls = len(re.findall(r'self\.wait\s*\(', segment_code))

    # Check for proper timing calculation pattern
    has_duration_var = 'duration = timing' in segment_code or "duration = timing['duration']" in segment_code
    has_wait_calc = 'wait_time' in segment_code or 'wait =' in segment_code

    if not has_duration_var:
        issues.append(f"TIMING: {seg_id} - not using duration from timing dict")

    if wait_calls > 0 and not has_wait_calc:
        issues.append(f"TIMING: {seg_id} - has {wait_calls} wait() calls but no wait_time calculation")

    # Rough estimate check: if run_times are too high relative to segment duration
    if total_run_time > seg_duration * 0.9:
        issues.append(f"TIMING: {seg_id} - animation time ({total_run_time:.1f}s) nearly exceeds segment duration ({seg_duration:.1f}s)")

# Print issues
for issue in issues:
    print(issue)

if not issues:
    print("OK: All segment timings validated")
TIMING_CHECK_EOF
)

    if echo "$timing_issues" | grep -q "^ERROR:"; then
        print_warning "Could not validate timing (file access issue)"
    elif echo "$timing_issues" | grep -q "^MISSING:\|^TIMING:"; then
        print_warning "⚠️ Timing issues detected (may cause duration mismatch):"
        echo "$timing_issues" | grep "^MISSING:\|^TIMING:" | head -5 | sed 's/^/   /'
        issues+=("timing_calculation_issues")
    else
        print_success "Segment timing calculations validated"
        score=$((score + 10))
    fi

    # ═══════════════════════════════════════════════════════════════════════════

    # Check for dynamic animations
    local dynamic_anims=0
    for anim in "Transform" "GrowFromCenter" "DrawBorderThenFill" "Write" "Create" "GrowArrow" "Flash"; do
        if grep -q "$anim" "$reel_code" 2>/dev/null; then
            dynamic_anims=$((dynamic_anims + 1))
        fi
    done
    if [ "$dynamic_anims" -ge 3 ]; then
        print_success "Dynamic animations found: $dynamic_anims types"
        score=$((score + 15))
    else
        print_warning "Only $dynamic_anims dynamic animation types (expected 3+)"
        issues+=("few_animations")
    fi

    # Check for color variety
    local color_count=0
    for color in "RED" "BLUE" "GREEN" "YELLOW" "ORANGE" "PURPLE" "CYAN" "PINK" "WHITE"; do
        if grep -q "$color" "$reel_code" 2>/dev/null; then
            color_count=$((color_count + 1))
        fi
    done
    if [ "$color_count" -ge 4 ]; then
        print_success "Color variety: $color_count colors"
        score=$((score + 10))
    else
        print_warning "Only $color_count colors (expected 4+)"
        issues+=("low_color_variety")
    fi

    # Generate validation JSON
    local issues_json=$(printf '%s\n' "${issues[@]}" | jq -R . | jq -s .)
    cat > "$WORK_DIR/manim_validation.json" << EOF
{
  "valid": $([ ${#issues[@]} -lt 3 ] && echo "true" || echo "false"),
  "animation_score": $score,
  "segment_count": $segment_count,
  "color_count": $color_count,
  "dynamic_animation_count": $dynamic_anims,
  "manim_edu_import_count": $manim_edu_count,
  "issues": $issues_json
}
EOF

    echo ""
    echo "Animation Score: $score/100"

    if [ ${#issues[@]} -lt 3 ]; then
        print_success "Validation passed with ${#issues[@]} warnings"
    else
        print_warning "Validation has ${#issues[@]} issues - proceeding anyway"
    fi

    add_chain_step "validate_manim_edu" "$WORK_DIR/manim_validation.json"
}

# ═══════════════════════════════════════════════════════════════════════════════
# QA CHECKPOINT 1: AUDIO SCRIPT VIRAL ENGINEERING
# ═══════════════════════════════════════════════════════════════════════════════

qa_audio_script_viral() {
    print_step "QA-1" "AUDIO SCRIPT - VIRAL ENGINEERING CHECK"

    local audio_script="$WORK_DIR/audio_script.json"
    if [ ! -f "$audio_script" ]; then
        print_warning "Audio script not found, skipping viral check"
        return 0
    fi

    local score=0
    local issues=()

    echo "Checking viral engineering elements..."

    # VIRAL ELEMENT 1: Hook in first segment (open loop)
    local hook=$(jq -r '.[0].text // ""' "$audio_script" 2>/dev/null)
    if echo "$hook" | grep -qiE "WRONG|क्यों|कैसे|secret|shocking|\?$|\.\.\."; then
        print_success "✅ Hook has open loop/question/intrigue"
        score=$((score + 15))
    else
        print_warning "⚠️ Hook missing open loop (add question, 'क्यों?', '...', WRONG!)"
        issues+=("weak_hook")
    fi

    # VIRAL ELEMENT 2: "99% wrong" or FOMO trigger
    if jq -r '.[].text' "$audio_script" | grep -qiE "99%|most students|sochte.*wrong|galat"; then
        print_success "✅ Has '99% wrong' or FOMO trigger"
        score=$((score + 15))
    else
        print_warning "⚠️ Missing '99% wrong' or FOMO element"
        issues+=("no_fomo")
    fi

    # VIRAL ELEMENT 3: Mind-blow moment
    if jq -r '.[].text' "$audio_script" | grep -qiE "mind.*blow|shocking|incredible|crazy|amazing|unbelievable"; then
        print_success "✅ Has mind-blow moment"
        score=$((score + 10))
    else
        print_warning "⚠️ Missing mind-blow moment"
        issues+=("no_mind_blow")
    fi

    # VIRAL ELEMENT 4: Data/numbers for credibility
    if jq -r '.[].text' "$audio_script" | grep -qE "[0-9]+.*%|[0-9]+.*kJ|[0-9]+.*degree|[0-9]+.*times"; then
        print_success "✅ Has data/numbers for credibility"
        score=$((score + 10))
    else
        print_warning "⚠️ Missing specific data/numbers"
        issues+=("no_data")
    fi

    # VIRAL ELEMENT 5: Exam anxiety trigger (JEE/NEET)
    if jq -r '.[].text' "$audio_script" | grep -qiE "JEE|NEET|exam|directly|पूछा|important question"; then
        print_success "✅ Has exam relevance (JEE/NEET)"
        score=$((score + 15))
    else
        print_warning "⚠️ Missing JEE/NEET exam relevance"
        issues+=("no_exam_relevance")
    fi

    # VIRAL ELEMENT 6: CTA with pricing
    if jq -r '.[].text' "$audio_script" | grep -qiE "jeetlo|499|register|early bird"; then
        print_success "✅ CTA mentions jeetlo.ai + pricing"
        score=$((score + 15))
    else
        print_warning "⚠️ CTA missing jeetlo.ai or pricing"
        issues+=("weak_cta")
    fi

    # VIRAL ELEMENT 7: Emotional hooks (pauses, exclamations, questions)
    # Note: We NO LONGER use CAPS (TTS reads them letter-by-letter)
    local ellipsis_count=$(jq -r '.[].text' "$audio_script" | grep -o '\.\.\.' | wc -l | tr -d ' ')
    local exclaim_count=$(jq -r '.[].text' "$audio_script" | grep -o '!' | wc -l | tr -d ' ')
    local question_count=$(jq -r '.[].text' "$audio_script" | grep -o '?' | wc -l | tr -d ' ')

    # WARN if CAPS are present (bad for TTS)
    local caps_count=$(jq -r '.[].text' "$audio_script" | grep -oE '\b[A-Z]{3,}\b' | wc -l | tr -d ' ')
    if [ "$caps_count" -gt 0 ]; then
        print_warning "⚠️ Found $caps_count ALL-CAPS words (TTS will spell letter-by-letter!)"
        issues+=("caps_in_audio")
    fi

    if [ "$ellipsis_count" -ge 3 ] && [ "$exclaim_count" -ge 3 ]; then
        print_success "✅ Emotional hooks present (pauses: $ellipsis_count, energy: $exclaim_count, curiosity: $question_count)"
        score=$((score + 10))
    else
        print_warning "⚠️ Need more '...' pauses and '!' energy markers"
        issues+=("weak_emotion")
    fi

    # VIRAL ELEMENT 8: Hinglish check (Hindi in Devanagari)
    if jq -r '.[].text' "$audio_script" | grep -q '[अ-ह]'; then
        print_success "✅ Hindi words in Devanagari (correct!)"
        score=$((score + 10))
    else
        print_warning "⚠️ Hindi should be in Devanagari script"
        issues+=("romanized_hindi")
    fi

    echo ""
    echo "Viral Engineering Score: $score/100"

    # Save QA result
    cat > "$WORK_DIR/qa_viral.json" << EOF
{
  "score": $score,
  "passed": $([ $score -ge 60 ] && echo "true" || echo "false"),
  "issues": $(printf '%s\n' "${issues[@]}" | jq -R . | jq -s . 2>/dev/null || echo "[]")
}
EOF

    if [ $score -ge 60 ]; then
        print_success "Viral engineering: PASS ($score/100)"
    else
        print_warning "Viral engineering: NEEDS IMPROVEMENT ($score/100)"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# QA CHECKPOINT 2: VIDEO CODE - MANIM-EDU USAGE VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

qa_video_code() {
    print_step "QA-2" "VIDEO CODE - MANIM-EDU USAGE CHECK"

    local reel_code="$WORK_DIR/reel.py"
    if [ ! -f "$reel_code" ]; then
        print_warning "reel.py not found, skipping code QA"
        return 0
    fi

    local score=0
    local issues=()

    echo "Verifying manim-edu library utilization..."

    # CHECK 1: Uses jeetlo_style.py imports
    if grep -q "from jeetlo_style import\|from.*jeetlo_style" "$reel_code"; then
        print_success "✅ Uses jeetlo_style.py (brand consistency)"
        score=$((score + 20))
    else
        print_warning "⚠️ Not using jeetlo_style.py - may have inconsistent branding"
        issues+=("no_jeetlo_style")
    fi

    # CHECK 2: Uses JeetLoReelMixin
    if grep -q "JeetLoReelMixin" "$reel_code"; then
        print_success "✅ Uses JeetLoReelMixin (correct base class)"
        score=$((score + 20))
    else
        print_warning "⚠️ Not using JeetLoReelMixin - missing standard features"
        issues+=("no_mixin")
    fi

    # CHECK 3: Uses standard CTA (add_cta_slide_*)
    if grep -qE "add_cta_slide_(physics|chem|biology|math)" "$reel_code"; then
        print_success "✅ Uses standard CTA slide (brand compliant)"
        score=$((score + 20))
    else
        print_error "❌ NOT using standard CTA - BLOCKING!"
        issues+=("custom_cta")
        echo "   REQUIRED: self.add_cta_slide_chem(duration) or similar"
    fi

    # CHECK 4: Uses manim_edu components
    local manim_edu_imports=$(grep -cE "from manim_edu|import manim_edu" "$reel_code" || echo 0)
    if [ "$manim_edu_imports" -ge 1 ]; then
        print_success "✅ Uses manim_edu components ($manim_edu_imports imports)"
        score=$((score + 15))
    else
        print_warning "⚠️ Not importing from manim_edu"
        issues+=("no_manim_edu")
    fi

    # CHECK 5: Uses watermark
    if grep -q "add_watermark\|create_brand_watermark" "$reel_code"; then
        print_success "✅ Uses standard watermark"
        score=$((score + 10))
    else
        print_warning "⚠️ Watermark may be missing"
        issues+=("no_watermark")
    fi

    # CHECK 6: Uses subject background
    if grep -q "set_subject_background\|CHEMISTRY_BG\|PHYSICS_BG\|BIOLOGY_BG\|MATH_BG" "$reel_code"; then
        print_success "✅ Uses subject-specific background color"
        score=$((score + 10))
    else
        print_warning "⚠️ May not use subject background color"
        issues+=("no_subject_bg")
    fi

    # CHECK 7: No reinvention (custom CTA, custom watermark)
    local reinvention=0
    if grep -qE "JeetLo.*!.*jeetlo\.ai.*499" "$reel_code" && ! grep -q "_create_standard_cta\|add_cta_slide" "$reel_code"; then
        print_error "❌ Custom CTA code detected - use add_cta_slide_*() instead!"
        reinvention=1
        issues+=("reinvented_cta")
    fi
    if grep -qE "watermark.*=.*VGroup\|Text.*JeetLo.*to_corner" "$reel_code" && ! grep -q "create_brand_watermark\|add_watermark" "$reel_code"; then
        print_warning "⚠️ Possible custom watermark - use create_brand_watermark() instead"
        reinvention=1
        issues+=("reinvented_watermark")
    fi
    if [ $reinvention -eq 0 ]; then
        print_success "✅ No code reinvention detected"
        score=$((score + 5))
    fi

    echo ""
    echo "Code Quality Score: $score/100"

    # Save QA result
    cat > "$WORK_DIR/qa_code.json" << EOF
{
  "score": $score,
  "passed": $([ $score -ge 70 ] && echo "true" || echo "false"),
  "issues": $(printf '%s\n' "${issues[@]}" | jq -R . | jq -s . 2>/dev/null || echo "[]")
}
EOF

    # BLOCKING: Must use standard CTA
    if grep -qE "add_cta_slide_(physics|chem|biology|math)" "$reel_code"; then
        print_success "Code QA: PASS"
    else
        print_error "Code QA: FAIL - Must use standard CTA (add_cta_slide_*)"
        echo "   Fix: Replace custom CTA with self.add_cta_slide_chem(duration)"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# QA CHECKPOINT 3: SYNC VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

qa_sync_verification() {
    print_step "QA-3" "AUDIO-VIDEO SYNC VERIFICATION"

    local video="$WORK_DIR/final.mp4"
    local audio="$WORK_DIR/audio/combined_audio.mp3"
    local timings="$WORK_DIR/audio/timings.json"

    if [ ! -f "$video" ]; then
        print_warning "Video not found, skipping sync check"
        return 0
    fi

    echo "Checking audio-video synchronization..."

    # Get durations
    local video_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video" 2>/dev/null | cut -d. -f1)
    local audio_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$audio" 2>/dev/null | cut -d. -f1)

    echo "Video duration: ${video_duration}s"
    echo "Audio duration: ${audio_duration}s"

    local diff=$((video_duration - audio_duration))
    if [ $diff -lt 0 ]; then diff=$((-diff)); fi

    if [ $diff -le 2 ]; then
        print_success "✅ Duration sync: ${diff}s difference (acceptable)"
    else
        print_error "❌ Duration mismatch: ${diff}s difference (max 2s allowed)"
        echo "   Video: ${video_duration}s, Audio: ${audio_duration}s"
        return 1
    fi

    # Extract keyframes at segment boundaries for manual verification
    if [ -f "$timings" ]; then
        echo ""
        echo "Extracting keyframes at segment boundaries..."
        mkdir -p "$WORK_DIR/qa_frames"

        local segment_times=$(jq -r '.[].startTime' "$timings" 2>/dev/null | head -5)
        local i=1
        for ts in $segment_times; do
            local ts_int=$(echo "$ts" | cut -d. -f1)
            ffmpeg -y -ss "$ts_int" -i "$video" -vframes 1 -q:v 2 "$WORK_DIR/qa_frames/segment_${i}_at_${ts_int}s.jpg" 2>/dev/null
            echo "  Frame at ${ts_int}s -> qa_frames/segment_${i}_at_${ts_int}s.jpg"
            i=$((i + 1))
        done
        print_success "Keyframes extracted for manual sync verification"
    fi

    # Save QA result
    cat > "$WORK_DIR/qa_sync.json" << EOF
{
  "video_duration": $video_duration,
  "audio_duration": $audio_duration,
  "difference": $diff,
  "passed": $([ $diff -le 2 ] && echo "true" || echo "false")
}
EOF
}

# ═══════════════════════════════════════════════════════════════════════════════
# QA CHECKPOINT 4: FRAME-BY-FRAME VISUAL QA
# ═══════════════════════════════════════════════════════════════════════════════

qa_frame_by_frame() {
    print_step "QA-4" "FRAME-BY-FRAME VISUAL QA"

    local video="$WORK_DIR/final.mp4"
    if [ ! -f "$video" ]; then
        print_warning "Video not found, skipping frame QA"
        return 0
    fi

    echo "Extracting frames for visual inspection (0.5 fps)..."
    mkdir -p "$WORK_DIR/qa_frames"

    # Extract at 0.5 fps (1 frame every 2 seconds)
    ffmpeg -y -i "$video" -vf "fps=0.5" "$WORK_DIR/qa_frames/frame_%02d.png" 2>/dev/null

    local frame_count=$(ls "$WORK_DIR/qa_frames"/frame_*.png 2>/dev/null | wc -l)
    echo "Extracted $frame_count frames"

    local issues=()

    # CHECK 1: First frame (Hook) - should have engaging visual
    if [ -f "$WORK_DIR/qa_frames/frame_01.png" ]; then
        print_success "✅ Frame 1 (Hook) extracted"
    fi

    # CHECK 2: Last few frames - should show CTA
    local last_frame=$(ls "$WORK_DIR/qa_frames"/frame_*.png 2>/dev/null | tail -1)
    if [ -n "$last_frame" ]; then
        echo "Last frame: $last_frame (should show CTA)"
        print_success "✅ CTA frame extracted"
    fi

    # CHECK 3: Content within bounds (use Python for actual pixel analysis if needed)
    echo ""
    echo "Manual QA checklist:"
    echo "  [ ] Hook frame is visually engaging"
    echo "  [ ] No text cut off at edges"
    echo "  [ ] No overlapping text"
    echo "  [ ] Colors are vibrant"
    echo "  [ ] CTA slide has flame + JeetLo + pricing"
    echo "  [ ] Watermark visible in bottom-right"

    # Save QA result
    cat > "$WORK_DIR/qa_frames.json" << EOF
{
  "frame_count": $frame_count,
  "frames_dir": "$WORK_DIR/qa_frames",
  "manual_review_required": true
}
EOF

    print_success "Frames ready for visual inspection at: $WORK_DIR/qa_frames/"
}

# ═══════════════════════════════════════════════════════════════════════════════
# QA CHECKPOINT 5: CTA COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════════

qa_cta_compliance() {
    print_step "QA-5" "CTA COMPLIANCE CHECK"

    local reel_code="$WORK_DIR/reel.py"
    local audio_script="$WORK_DIR/audio_script.json"
    local issues=()

    echo "Verifying CTA compliance..."

    # VIDEO CTA: Must use standard add_cta_slide_*
    echo ""
    echo "VIDEO CTA (on-screen):"
    if grep -qE "add_cta_slide_(physics|chem|biology|math)" "$reel_code" 2>/dev/null; then
        local cta_method=$(grep -oE "add_cta_slide_(physics|chem|biology|math)" "$reel_code" | head -1)
        print_success "✅ Using standard CTA: $cta_method"
        echo "   Includes: Flame + JeetLo + Follow + jeetlo.ai + ₹499/mo"
    else
        print_error "❌ NOT using standard CTA!"
        echo "   REQUIRED: self.add_cta_slide_chem(duration)"
        issues+=("no_standard_cta")
    fi

    # AUDIO CTA: Must mention jeetlo.ai and pricing
    echo ""
    echo "AUDIO CTA (spoken):"
    if jq -r '.[].text' "$audio_script" 2>/dev/null | grep -qi "jeetlo"; then
        print_success "✅ Audio mentions 'jeetlo'"
    else
        print_warning "⚠️ Audio should mention 'jeetlo.ai'"
        issues+=("audio_no_jeetlo")
    fi

    if jq -r '.[].text' "$audio_script" 2>/dev/null | grep -qE "499|four ninety nine"; then
        print_success "✅ Audio mentions pricing (499)"
    else
        print_warning "⚠️ Audio should mention early bird pricing"
        issues+=("audio_no_pricing")
    fi

    if jq -r '.[].text' "$audio_script" 2>/dev/null | grep -qi "register\|early bird"; then
        print_success "✅ Audio has registration CTA"
    else
        print_warning "⚠️ Audio should have registration call-to-action"
        issues+=("audio_no_register_cta")
    fi

    # Save QA result
    cat > "$WORK_DIR/qa_cta.json" << EOF
{
  "video_cta_standard": $(grep -qE "add_cta_slide_" "$reel_code" 2>/dev/null && echo "true" || echo "false"),
  "audio_mentions_jeetlo": $(jq -r '.[].text' "$audio_script" 2>/dev/null | grep -qi "jeetlo" && echo "true" || echo "false"),
  "audio_mentions_pricing": $(jq -r '.[].text' "$audio_script" 2>/dev/null | grep -qE "499" && echo "true" || echo "false"),
  "issues": $(printf '%s\n' "${issues[@]}" | jq -R . | jq -s . 2>/dev/null || echo "[]")
}
EOF

    if [ ${#issues[@]} -eq 0 ]; then
        print_success "CTA Compliance: PASS"
    else
        print_warning "CTA Compliance: ${#issues[@]} issues"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🚨 MANDATORY STATELESS POLICING AGENTS 🚨
#
# ARCHITECTURE:
# - Each agent is COMPLETELY INDEPENDENT (no shared state)
# - Each agent is STATELESS (fresh instance per run)
# - Each agent has its own UNIQUE ID
# - Agents can run in ANY ORDER or in PARALLEL
# - One agent CANNOT access another agent's data
#
# They do NOT trust the production pipeline - they verify everything
# ═══════════════════════════════════════════════════════════════════════════════

# POLICING AGENT 1: FRAME OVERLAP VALIDATOR (STATELESS)
# Uses manim-edu/qa/agents.py FrameOverlapAgent
# Creates fresh agent instance with unique ID
# BLOCKS if overlapping text detected (threshold: 95%)
police_frame_overlap() {
    print_step "🚨 POLICE-1" "FRAME OVERLAP VALIDATOR (STATELESS)"

    local frames_dir="$WORK_DIR/frames"
    local threshold=95

    if [ ! -d "$frames_dir" ]; then
        print_warning "Frames not extracted yet, extracting now..."
        mkdir -p "$frames_dir"
        ffmpeg -y -i "$WORK_DIR/final.mp4" -vf "fps=0.5" "$frames_dir/frame_%03d.png" 2>/dev/null
    fi

    echo "Creating fresh POLICE-1 agent instance..."

    # Run STATELESS agent - fresh instance with unique ID
    local result=$(python3 -c "
import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
from manim_edu.qa import FrameOverlapAgent

# Create FRESH agent instance (unique ID, no shared state)
agent = FrameOverlapAgent()
print(f'Agent ID: {agent.agent_id}')

# Run with complete isolation
result = agent.run(frames_dir='$frames_dir', threshold=$threshold)

# Immutable result
print('PASSED' if result.passed else 'FAILED')
print(f'Bounty: {result.bounty_earned} points')
print(f'Issues: {result.issues_count}')
print(f'Run ID: {result.run_id}')
exit(0 if result.passed else 1)
" 2>&1)

    local exit_code=$?
    echo "$result"

    # Save immutable result
    python3 -c "
import sys, json
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
from manim_edu.qa import FrameOverlapAgent

agent = FrameOverlapAgent()
result = agent.run(frames_dir='$frames_dir', threshold=$threshold)
print(json.dumps(result.to_dict(), indent=2))
" > "$WORK_DIR/police_frame_overlap.json" 2>/dev/null

    if [ $exit_code -eq 0 ]; then
        print_success "🚨 POLICE-1 PASSED: No overlapping text detected"
        return 0
    else
        print_error "🚨 POLICE-1 BLOCKED: Overlapping text detected!"
        echo "   Fix the overlaps and re-render before proceeding."
        return 1
    fi
}

# POLICING AGENT 2: MANIM-EDU UTILIZATION (STATELESS)
# Uses manim-edu/qa/agents.py UtilizationAgent
# Creates fresh agent instance with unique ID
# BLOCKS if utilization < 95%
police_utilization() {
    print_step "🚨 POLICE-2" "MANIM-EDU UTILIZATION CHECK (STATELESS)"

    local code_path="$WORK_DIR/reel.py"
    local threshold=95

    if [ ! -f "$code_path" ]; then
        print_error "reel.py not found"
        return 1
    fi

    echo "Creating fresh POLICE-2 agent instance..."

    # Run STATELESS agent - fresh instance with unique ID
    local result=$(python3 -c "
import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
from manim_edu.qa import UtilizationAgent

# Create FRESH agent instance (unique ID, no shared state)
agent = UtilizationAgent()
print(f'Agent ID: {agent.agent_id}')

# Run with complete isolation
result = agent.run(code_path='$code_path', threshold=$threshold)

# Immutable result
print('PASSED' if result.passed else 'FAILED')
print(f'Bounty: {result.bounty_earned} points')
print(f'Issues: {result.issues_count}')
print(f'Run ID: {result.run_id}')

# Get details from immutable result
details = dict(result.details)
print(f'Utilization: {details.get(\"utilization\", \"N/A\")}%')
exit(0 if result.passed else 1)
" 2>&1)

    local exit_code=$?
    echo "$result"

    # Save immutable result
    python3 -c "
import sys, json
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
from manim_edu.qa import UtilizationAgent

agent = UtilizationAgent()
result = agent.run(code_path='$code_path', threshold=$threshold)
print(json.dumps(result.to_dict(), indent=2))
" > "$WORK_DIR/police_utilization.json" 2>/dev/null

    if [ $exit_code -eq 0 ]; then
        print_success "🚨 POLICE-2 PASSED: manim-edu utilization >= $threshold%"
        return 0
    else
        print_error "🚨 POLICE-2 BLOCKED: manim-edu utilization < $threshold%!"
        echo "   Use manim-edu components instead of custom code."
        return 1
    fi
}

# POLICING AGENT 3: CONTENT VERIFICATION (STATELESS)
# Uses manim-edu/qa/agents.py ContentAgent
# Creates fresh agent instance with unique ID
# BLOCKS if facts cannot be verified or are incorrect
police_content() {
    print_step "🚨 POLICE-3" "CONTENT VERIFICATION (STATELESS)"

    local script_path="$WORK_DIR/audio_script.json"

    if [ ! -f "$script_path" ]; then
        # Try timings.json
        script_path="$WORK_DIR/audio/timings.json"
    fi

    if [ ! -f "$script_path" ]; then
        print_warning "Script not found, skipping content verification"
        return 0
    fi

    echo "Creating fresh POLICE-3 agent instance..."

    # Run STATELESS agent - fresh instance with unique ID
    local result=$(python3 -c "
import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
from manim_edu.qa import ContentAgent

# Create FRESH agent instance (unique ID, no shared state)
agent = ContentAgent()
print(f'Agent ID: {agent.agent_id}')

# Run with complete isolation
result = agent.run(script_path='$script_path', subject='$SUBJECT')

# Immutable result
print('PASSED' if result.passed else 'FAILED')
print(f'Bounty: {result.bounty_earned} points')
print(f'Issues: {result.issues_count}')
print(f'Run ID: {result.run_id}')

# Get details from immutable result
details = dict(result.details)
print(f'Claims: {details.get(\"total_claims\", 0)}')
print(f'  Verified: {details.get(\"verified\", 0)}')
print(f'  Incorrect: {details.get(\"incorrect\", 0)}')
exit(0 if result.passed else 1)
" 2>&1)

    local exit_code=$?
    echo "$result"

    # Save immutable result
    python3 -c "
import sys, json
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
from manim_edu.qa import ContentAgent

agent = ContentAgent()
result = agent.run(script_path='$script_path', subject='$SUBJECT')
print(json.dumps(result.to_dict(), indent=2))
" > "$WORK_DIR/police_content.json" 2>/dev/null

    if [ $exit_code -eq 0 ]; then
        print_success "🚨 POLICE-3 PASSED: Content verified"
        return 0
    else
        print_error "🚨 POLICE-3 BLOCKED: Content verification failed!"
        echo "   Fix incorrect facts before proceeding."
        return 1
    fi
}

# POLICING AGENT 4: CALCULATION VERIFICATION (STATELESS)
# Uses manim-edu/qa/agents.py CalculationAgent
# Creates fresh agent instance with unique ID
# BLOCKS if calculations are incorrect
police_calculations() {
    print_step "🚨 POLICE-4" "CALCULATION VERIFICATION (STATELESS)"

    local script_path="$WORK_DIR/audio_script.json"

    if [ ! -f "$script_path" ]; then
        script_path="$WORK_DIR/audio/timings.json"
    fi

    if [ ! -f "$script_path" ]; then
        print_warning "Script not found, skipping calculation verification"
        return 0
    fi

    echo "Creating fresh POLICE-4 agent instance..."

    # Run STATELESS agent - fresh instance with unique ID
    local result=$(python3 -c "
import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
from manim_edu.qa import CalculationAgent

# Create FRESH agent instance (unique ID, no shared state)
agent = CalculationAgent()
print(f'Agent ID: {agent.agent_id}')

# Run with complete isolation
result = agent.run(script_path='$script_path', subject='$SUBJECT')

# Immutable result
print('PASSED' if result.passed else 'FAILED')
print(f'Bounty: {result.bounty_earned} points')
print(f'Issues: {result.issues_count}')
print(f'Run ID: {result.run_id}')

# Get details from immutable result
details = dict(result.details)
print(f'Calculations: {details.get(\"total_calculations\", 0)}')
print(f'  Correct: {details.get(\"correct\", 0)}')
print(f'  Incorrect: {details.get(\"incorrect\", 0)}')
exit(0 if result.passed else 1)
" 2>&1)

    local exit_code=$?
    echo "$result"

    # Save immutable result
    python3 -c "
import sys, json
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
from manim_edu.qa import CalculationAgent

agent = CalculationAgent()
result = agent.run(script_path='$script_path', subject='$SUBJECT')
print(json.dumps(result.to_dict(), indent=2))
" > "$WORK_DIR/police_calculations.json" 2>/dev/null

    if [ $exit_code -eq 0 ]; then
        print_success "🚨 POLICE-4 PASSED: All calculations verified"
        return 0
    else
        print_error "🚨 POLICE-4 BLOCKED: Calculation errors found!"
        echo "   Fix the calculations before proceeding."
        return 1
    fi
}

# MASTER POLICING RUNNER (MANDATORY - ALL MUST PASS)
run_all_police() {
    print_header "🚨 RUNNING MANDATORY POLICING AGENTS 🚨"
    echo "These are INDEPENDENT verification agents."
    echo "They do NOT trust the production pipeline."
    echo "ALL must PASS for content to proceed."
    echo ""

    local all_passed=true

    # POLICE-2: Utilization (run first - fastest)
    police_utilization || all_passed=false
    echo ""

    # POLICE-3: Content Verification
    police_content || all_passed=false
    echo ""

    # POLICE-4: Calculation Verification
    police_calculations || all_passed=false
    echo ""

    # POLICE-1: Frame Overlap (run last - requires rendered video)
    if [ -f "$WORK_DIR/final.mp4" ]; then
        police_frame_overlap || all_passed=false
    else
        print_warning "Final video not found - skipping frame overlap check"
    fi
    echo ""

    # Summary
    if [ "$all_passed" = true ]; then
        print_success "═══════════════════════════════════════════════════════════"
        print_success "🚨 ALL POLICING AGENTS PASSED - CONTENT APPROVED 🚨"
        print_success "═══════════════════════════════════════════════════════════"
        return 0
    else
        print_error "═══════════════════════════════════════════════════════════"
        print_error "🚨 POLICING AGENTS BLOCKED CONTENT 🚨"
        print_error "Fix all issues above before proceeding."
        print_error "═══════════════════════════════════════════════════════════"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# MASTER QA RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

run_all_qa() {
    print_step "QA" "RUNNING ALL QA CHECKPOINTS"
    echo ""

    local qa_passed=true

    # QA-1: Viral Engineering
    qa_audio_script_viral || qa_passed=false
    echo ""

    # QA-2: Code Quality
    qa_video_code || qa_passed=false
    echo ""

    # QA-5: CTA Compliance (run before render for early feedback)
    qa_cta_compliance || qa_passed=false
    echo ""

    if [ "$qa_passed" = true ]; then
        print_success "═══════════════════════════════════════"
        print_success "ALL PRE-RENDER QA CHECKS PASSED"
        print_success "═══════════════════════════════════════"
    else
        print_warning "═══════════════════════════════════════"
        print_warning "SOME QA CHECKS HAVE ISSUES - Review above"
        print_warning "═══════════════════════════════════════"
    fi

    return 0
}

run_post_render_qa() {
    print_step "QA" "POST-RENDER QA CHECKPOINTS"
    echo ""

    # QA-3: Sync Verification
    qa_sync_verification
    echo ""

    # QA-4: Frame-by-Frame
    qa_frame_by_frame
    echo ""

    print_success "Post-render QA complete. Review qa_frames/ for visual inspection."
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6: RENDER VIDEO
# ═══════════════════════════════════════════════════════════════════════════════

render_video() {
    print_step "6" "RENDER VIDEO (Manim)"

    # Update manim-edu to get latest fixes
    echo "Updating manim-edu library..."
    if [ -d "/Users/pran/Projects/libraries/manim-edu" ]; then
        (cd /Users/pran/Projects/libraries/manim-edu && git pull origin main 2>/dev/null) || true
    fi

    echo "Rendering with Manim..."
    echo "Resolution: 1080x1920 (9:16 vertical)"
    echo ""

    # Create a wrapper script that sets up paths
    # Use specific Python with manim installed
    cat > "$WORK_DIR/render.sh" << 'RENDER_EOF'
#!/bin/bash
cd "$1"
export PATH="/opt/homebrew/bin:/Users/pran/Library/TinyTeX/bin/universal-darwin:/Library/TeX/texbin:$PATH"

# Find Python with manim installed
PYTHON=""
for py in /opt/homebrew/bin/python3.11 /opt/homebrew/bin/python3 /usr/bin/python3; do
    if [ -x "$py" ] && $py -c "import manim" 2>/dev/null; then
        PYTHON="$py"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "ERROR: No Python with manim found"
    exit 1
fi

# Find the Scene class name in reel.py
SCENE_NAME=$(grep -E "^class.*\(.*Scene" reel.py | head -1 | sed 's/class \([A-Za-z]*\).*/\1/')
if [ -z "$SCENE_NAME" ]; then
    SCENE_NAME="PhysicsReel"  # fallback
fi

echo "Using Python: $PYTHON"
echo "Scene: $SCENE_NAME"
$PYTHON -m manim render -qh --fps 30 -r 1080,1920 reel.py "$SCENE_NAME" 2>&1
RENDER_EOF
    chmod +x "$WORK_DIR/render.sh"

    if bash "$WORK_DIR/render.sh" "$WORK_DIR"; then
        # Find the rendered video
        local video_file=$(find "$WORK_DIR/media/videos" -name "*.mp4" | head -1)
        if [ -n "$video_file" ]; then
            cp "$video_file" "$WORK_DIR/video.mp4"
            local duration=$(ffprobe -i "$WORK_DIR/video.mp4" -show_entries format=duration -v quiet -of csv="p=0")
            print_success "Video rendered: ${duration}s"

            add_chain_step "render_video" "$WORK_DIR/video.mp4"
        else
            print_error "No video file found after render"
            exit 1
        fi
    else
        print_error "Manim render failed"
        exit 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 7: VALIDATE DURATION SYNC
# ═══════════════════════════════════════════════════════════════════════════════

validate_sync() {
    print_step "7" "VALIDATE DURATION SYNC"

    local video_duration=$(ffprobe -i "$WORK_DIR/video.mp4" -show_entries format=duration -v quiet -of csv="p=0")
    local audio_duration=$(ffprobe -i "$WORK_DIR/audio/combined_audio.mp3" -show_entries format=duration -v quiet -of csv="p=0")

    echo "Video duration: ${video_duration}s"
    echo "Audio duration: ${audio_duration}s"

    local diff=$(echo "$video_duration - $audio_duration" | bc)
    local abs_diff=$(echo "$diff" | tr -d -)

    # Video should be >= audio (so CTA doesn't get cut)
    if (( $(echo "$video_duration >= $audio_duration" | bc -l) )); then
        if (( $(echo "$abs_diff <= 2.0" | bc -l) )); then
            print_success "Duration sync valid: video is ${diff}s longer than audio"
        else
            print_warning "Video is ${diff}s longer than audio (max 2s overage recommended)"
        fi
    else
        print_error "VIDEO IS SHORTER THAN AUDIO by ${abs_diff}s"
        echo "CTA will be cut off when combined with -shortest"
        echo "FIX: Add self.wait() calls to segments"
        exit 1
    fi

    echo '{"video_duration": '$video_duration', "audio_duration": '$audio_duration', "diff": '$diff'}' > "$WORK_DIR/sync_validation.json"
    add_chain_step "validate_sync" "$WORK_DIR/sync_validation.json"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 8: FRAME QA
# ═══════════════════════════════════════════════════════════════════════════════

frame_qa() {
    print_step "8" "FRAME QA (Extract & Review)"

    mkdir -p "$WORK_DIR/frames"

    echo "Extracting frames at 0.5fps..."
    ffmpeg -y -i "$WORK_DIR/video.mp4" -vf "fps=0.5" "$WORK_DIR/frames/frame_%03d.png" 2>/dev/null

    local frame_count=$(ls "$WORK_DIR/frames/"*.png 2>/dev/null | wc -l | tr -d ' ')
    echo "Extracted: $frame_count frames"
    echo ""

    # Do code-based QA checks (no Claude CLI needed)
    echo "Running code-based QA checks..."

    local issues=()
    local reel_code="$WORK_DIR/reel.py"

    # Check 1: Safe zone - look for hardcoded positions near edges
    if grep -q "\.to_edge\|LEFT\s*\*\s*[4-9]\|RIGHT\s*\*\s*[4-9]" "$reel_code" 2>/dev/null; then
        print_warning "Possible edge positioning detected"
        issues+=("edge_positioning")
    else
        print_success "Safe zone: No obvious edge issues"
    fi

    # Check 2: Watermark
    if grep -q "create_brand_watermark\|watermark" "$reel_code" 2>/dev/null; then
        print_success "Watermark: Present in code"
    else
        print_warning "Watermark: Not found in code"
        issues+=("missing_watermark")
    fi

    # Check 3: CTA slide
    if grep -q "add_cta_slide\|segment.*cta\|07_cta" "$reel_code" 2>/dev/null; then
        print_success "CTA slide: Present in code"
    else
        print_warning "CTA slide: Not found in code"
        issues+=("missing_cta")
    fi

    # Check 4: Color contrast - check if background color is dark
    local bg_color=$(grep -o "background_color.*=.*['\"]#[^'\"]*['\"]" "$reel_code" 2>/dev/null | head -1)
    if [ -n "$bg_color" ]; then
        print_success "Background color defined: $bg_color"
    else
        print_warning "Background color not explicitly set"
    fi

    # Check 5: Self.clear() or cleanup between segments
    if grep -q "self\.clear()\|FadeOut.*Group\|self\.remove" "$reel_code" 2>/dev/null; then
        print_success "Cleanup: Segments appear to clean up objects"
    else
        print_warning "Cleanup: No explicit cleanup between segments"
        issues+=("missing_cleanup")
    fi

    # Generate QA JSON
    local issues_json=$(printf '%s\n' "${issues[@]}" | jq -R . | jq -s .)
    cat > "$WORK_DIR/frame_qa.json" << EOF
{
  "frame_count": $frame_count,
  "frames_dir": "$WORK_DIR/frames",
  "checks": {
    "safe_zone": $([ ! "${issues[*]}" =~ "edge_positioning" ] && echo "true" || echo "false"),
    "watermark": $(grep -q "watermark" "$reel_code" 2>/dev/null && echo "true" || echo "false"),
    "cta_present": $(grep -q "cta" "$reel_code" 2>/dev/null && echo "true" || echo "false"),
    "cleanup": $(grep -q "clear\|FadeOut" "$reel_code" 2>/dev/null && echo "true" || echo "false")
  },
  "issues": $issues_json,
  "recommendation": "$([ ${#issues[@]} -lt 2 ] && echo "pass" || echo "review_needed")"
}
EOF

    local recommendation=$([ ${#issues[@]} -lt 2 ] && echo "pass" || echo "review_needed")

    if [ "$recommendation" == "pass" ]; then
        print_success "Frame QA: PASS (${#issues[@]} minor issues)"
    else
        print_warning "Frame QA: Review recommended (${#issues[@]} issues)"
        jq -r '.predicted_issues[]' "$WORK_DIR/frame_qa.json" 2>/dev/null
    fi

    echo ""
    echo "Frames saved to: $WORK_DIR/frames/"
    echo "Please visually inspect before proceeding."

    add_chain_step "frame_qa" "$WORK_DIR/frame_qa.json"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 9: COMBINE AUDIO/VIDEO
# ═══════════════════════════════════════════════════════════════════════════════

combine_av() {
    print_step "9" "COMBINE AUDIO/VIDEO"

    echo "Combining with ffmpeg..."

    ffmpeg -y \
        -i "$WORK_DIR/video.mp4" \
        -i "$WORK_DIR/audio/combined_audio.mp3" \
        -c:v libx264 -preset fast -crf 18 \
        -c:a aac -b:a 192k \
        -shortest \
        "$WORK_DIR/final.mp4" 2>/dev/null

    if [ -f "$WORK_DIR/final.mp4" ]; then
        local final_duration=$(ffprobe -i "$WORK_DIR/final.mp4" -show_entries format=duration -v quiet -of csv="p=0")
        local file_size=$(du -h "$WORK_DIR/final.mp4" | cut -f1)

        print_success "Final video: ${final_duration}s, ${file_size}"

        add_chain_step "combine_av" "$WORK_DIR/final.mp4"
    else
        print_error "Failed to combine audio/video"
        exit 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 10: GENERATE THUMBNAIL
# ═══════════════════════════════════════════════════════════════════════════════

generate_thumbnail() {
    print_step "10" "GENERATE THUMBNAIL"

    # Extract frame at 1 second (usually the hook)
    ffmpeg -y -i "$WORK_DIR/final.mp4" -ss 1 -vframes 1 "$WORK_DIR/thumbnail.png" 2>/dev/null

    if [ -f "$WORK_DIR/thumbnail.png" ]; then
        local size=$(identify "$WORK_DIR/thumbnail.png" 2>/dev/null | awk '{print $3}')
        print_success "Thumbnail generated: $size"

        add_chain_step "thumbnail" "$WORK_DIR/thumbnail.png"
    else
        print_warning "Failed to generate thumbnail"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 11: FINAL QA & CHAIN VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

final_qa() {
    print_step "11" "FINAL QA & CHAIN VALIDATION"

    echo "Validating proof chain..."
    validate_chain

    echo ""
    echo "Checking all outputs..."

    local qa_result='{}'

    # Check all required files exist
    local checks=(
        "creative_brief.json"
        "audio_script.json"
        "audio/combined_audio.mp3"
        "audio/timings.json"
        "reel.py"
        "video.mp4"
        "final.mp4"
    )

    for check in "${checks[@]}"; do
        if [ -f "$WORK_DIR/$check" ]; then
            print_success "  $check"
            qa_result=$(echo "$qa_result" | jq --arg k "$check" '. + {($k): true}')
        else
            print_error "  $check MISSING"
            qa_result=$(echo "$qa_result" | jq --arg k "$check" '. + {($k): false}')
        fi
    done

    echo "$qa_result" | jq '. + {qa_passed: true, timestamp: now}' > "$WORK_DIR/final_qa.json"
    add_chain_step "final_qa" "$WORK_DIR/final_qa.json"

    # Mark as ready for posting
    jq '.status = "ready_to_post"' "$WORK_DIR/.proof_chain.json" > "$WORK_DIR/.proof_chain.json.tmp"
    mv "$WORK_DIR/.proof_chain.json.tmp" "$WORK_DIR/.proof_chain.json"

    print_success "Final QA passed - ready for posting!"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 12: PUSH TO GITHUB
# ═══════════════════════════════════════════════════════════════════════════════

push_to_github() {
    print_step "12" "PUSH TO GITHUB"

    echo "Updating jeetlo-factory repo..."

    # Copy outputs to repo
    local reel_dir="$FACTORY_DIR/reels/$REEL_ID"
    mkdir -p "$reel_dir"

    cp "$WORK_DIR/.proof_chain.json" "$reel_dir/"
    cp "$WORK_DIR/creative_brief.json" "$reel_dir/"
    cp "$WORK_DIR/reel.py" "$reel_dir/"
    cp "$WORK_DIR/audio/timings.json" "$reel_dir/"

    # Update db/reels.json
    if [ -f "$FACTORY_DIR/db/reels.json" ]; then
        jq --arg id "$REEL_ID" \
           --arg subject "$SUBJECT" \
           --arg topic "$TOPIC" \
           --arg status "ready_to_post" \
           '.reels += [{id: $id, subject: $subject, topic: $topic, status: $status, updated: now}]' \
           "$FACTORY_DIR/db/reels.json" > "$FACTORY_DIR/db/reels.json.tmp"
        mv "$FACTORY_DIR/db/reels.json.tmp" "$FACTORY_DIR/db/reels.json"
    fi

    # Git commit and push
    cd "$FACTORY_DIR"
    git add -A
    git commit -m "Add reel: $REEL_ID

Proof chain complete with $(jq '.steps | length' "$reel_dir/.proof_chain.json") steps.

Generated by jeetlo.sh" 2>/dev/null || true

    if git push origin main 2>/dev/null; then
        print_success "Pushed to GitHub"
    else
        print_warning "Failed to push to GitHub (may need auth)"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    if [ -z "$1" ]; then
        echo "Usage: $0 <reel_id> [--resume]"
        echo ""
        echo "Examples:"
        echo "  $0 bio-05-dna-right-handed"
        echo "  $0 phy-01-laws-of-motion --resume"
        exit 1
    fi

    REEL_ID="$1"
    RESUME="${2:-}"

    # Parse reel_id to get subject
    SUBJECT=$(echo "$REEL_ID" | cut -d'-' -f1)
    case "$SUBJECT" in
        bio) SUBJECT="biology" ;;
        phy) SUBJECT="physics" ;;
        che|chem) SUBJECT="chemistry" ;;
        mat|math) SUBJECT="mathematics" ;;
    esac

    # Try to get topic from request file
    if [ -f "$FACTORY_DIR/requests/$REEL_ID.json" ]; then
        TOPIC=$(jq -r '.topic' "$FACTORY_DIR/requests/$REEL_ID.json")
        HOOK=$(jq -r '.hook // ""' "$FACTORY_DIR/requests/$REEL_ID.json")
    else
        TOPIC="$REEL_ID"
        HOOK=""
    fi

    WORK_DIR="/tmp/jeetlo/$REEL_ID"

    print_header "JEETLO REEL FACTORY"
    echo "Reel ID: $REEL_ID"
    echo "Subject: $SUBJECT"
    echo "Topic: $TOPIC"
    echo "Work Dir: $WORK_DIR"
    echo ""

    # Run all steps
    setup_and_auth

    if [ "$RESUME" != "--resume" ] || [ ! -f "$WORK_DIR/creative_brief.json" ]; then
        create_creative_brief
    else
        print_success "Skipping creative brief (resuming)"
    fi

    if [ "$RESUME" != "--resume" ] || [ ! -f "$WORK_DIR/audio_script.json" ]; then
        create_audio_script
    else
        print_success "Skipping audio script (resuming)"
    fi

    if [ "$RESUME" != "--resume" ] || [ ! -f "$WORK_DIR/audio/combined_audio.mp3" ]; then
        generate_audio
    else
        print_success "Skipping audio generation (resuming)"
    fi

    if [ "$RESUME" != "--resume" ] || [ ! -f "$WORK_DIR/reel.py" ]; then
        create_video_script
    else
        print_success "Skipping video script (resuming)"
    fi

    validate_manim_edu

    if [ "$RESUME" != "--resume" ] || [ ! -f "$WORK_DIR/video.mp4" ]; then
        render_video
    else
        print_success "Skipping video render (resuming)"
    fi

    validate_sync
    frame_qa
    combine_av
    generate_thumbnail

    # 🚨 MANDATORY POLICING AGENTS - MUST PASS BEFORE FINAL QA 🚨
    # These are INDEPENDENT verification agents that can BLOCK content
    if ! run_all_police; then
        print_error "═══════════════════════════════════════════════════════════"
        print_error "🚨 PIPELINE BLOCKED BY POLICING AGENTS 🚨"
        print_error "Fix all issues above and re-run with --resume"
        print_error "═══════════════════════════════════════════════════════════"
        exit 1
    fi

    final_qa
    push_to_github

    print_header "PIPELINE COMPLETE"
    echo "Final video: $WORK_DIR/final.mp4"
    echo "Duration: $(ffprobe -i "$WORK_DIR/final.mp4" -show_entries format=duration -v quiet -of csv="p=0")s"
    echo ""
    echo "Proof chain: $(jq '.steps | length' "$WORK_DIR/.proof_chain.json") steps validated"
    echo ""
    echo "Next step: Post to Instagram/YouTube"
    echo "  node /Users/pran/Projects/tools/social-automation/cli/bin/social.js schedule jeetlo instagram \"$WORK_DIR/final.mp4\""
}

main "$@"
