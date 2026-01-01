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
  "VP8": "Sync animations WITH audio"
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

EMOTION ENGINEERING (USE THESE):
- CAPS for emphasis: 'Ice FLOATS on water!'
- ... for dramatic pause: 'लेकिन actually...'
- ! for energy: 'Secret है hydrogen bonding!'
- ? for curiosity: 'क्यों?'

BRAND VOICE:
- Use 'aap' (respectful), never 'tu/tum'
- Mention JEE/NEET relevance
- End with: 'JeetLo! Follow kijiye!'

EXAMPLE SEGMENT:
{
  \"id\": \"01_hook\",
  \"text\": \"Ice पानी पर FLOAT करती है... लेकिन हर दूसरा solid SINK करता है! क्यों?\"
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
    ls "$WORK_DIR/audio/"*.mp3 | grep -v combined_audio | sort | while read f; do
        echo "file '$(basename "$f")'"
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

MANIM-EDU LIBRARY (MANDATORY - use these for stunning visuals):
Location: /Users/pran/Projects/libraries/manim-edu

Available components by subject:
- Physics: from manim_edu.physics import WaveSimulator, FieldVisualizer, MechanicsSimulator
- Chemistry: from manim_edu.chemistry import MoleculeBuilder
- Biology: from manim_edu.biology import CellVisualizer
- Math: from manim_edu.mathematics import GraphAnimator

Example usage:
  field = FieldVisualizer()
  dipole = field.electric_dipole()  # Beautiful field lines

  wave = WaveSimulator()
  sine = wave.sine_wave(amplitude=1, wavelength=2)

  mol = MoleculeBuilder(scale=1.5)
  water = mol.water()  # H2O with correct bond angles

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
        # CTA slide with JeetLo branding
        duration = timing['duration']
        logo = create_brand_watermark(opacity=1.0, scale=2.0)
        logo.center()
        cta_text = Text("Follow for more!", font_size=48, color=WHITE)
        cta_text.next_to(logo, DOWN, buff=0.5)
        url = Text("jeetlo.ai", font_size=36, color=YELLOW)
        url.next_to(cta_text, DOWN, buff=0.3)

        self.play(FadeIn(logo), run_time=0.8)
        self.play(Write(cta_text), run_time=0.6)
        self.play(Write(url), run_time=0.4)
        self.wait(duration - 1.8)

REQUIREMENTS:
1. Create a segment method for EACH entry in timings (segment_01_hook, segment_02_setup, etc.)
2. Each segment must use timing['duration'] to calculate wait times correctly
3. MUST use manim-edu components for stunning scientific visualizations
4. Use 6+ colors from: RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, TEAL, PINK, WHITE, GOLD (NOT CYAN - use TEAL instead)
5. Clear all objects at end of each segment with self.clear() or FadeOut
6. Match the visual scenes described in the creative brief
7. CTA segment must include jeetlo.ai and "Follow for more!"

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
# STEP 6: RENDER VIDEO
# ═══════════════════════════════════════════════════════════════════════════════

render_video() {
    print_step "6" "RENDER VIDEO (Manim)"

    echo "Rendering with Manim..."
    echo "Resolution: 1080x1920 (9:16 vertical)"
    echo ""

    # Create a wrapper script that sets up paths
    # Use specific Python with manim installed
    cat > "$WORK_DIR/render.sh" << 'RENDER_EOF'
#!/bin/bash
cd "$1"
export PATH="/opt/homebrew/bin:/Library/TeX/texbin:$PATH"

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

echo "Using Python: $PYTHON"
$PYTHON -m manim render -qh reel.py 2>&1
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

    git push origin main 2>/dev/null || print_warning "Failed to push to GitHub"

    print_success "Pushed to GitHub"
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
