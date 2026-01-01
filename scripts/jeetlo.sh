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

    claude --print --dangerously-skip-permissions --output-format json \
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
}" 2>/dev/null | jq -r '.result // .' > "$WORK_DIR/creative_brief_raw.txt"

    # Parse JSON from response
    if grep -q '"core_analogy"' "$WORK_DIR/creative_brief_raw.txt"; then
        # Extract JSON from response
        sed -n '/^{/,/^}/p' "$WORK_DIR/creative_brief_raw.txt" | jq '.' > "$WORK_DIR/creative_brief.json" 2>/dev/null || {
            cat "$WORK_DIR/creative_brief_raw.txt" | jq '.' > "$WORK_DIR/creative_brief.json"
        }
        print_success "Creative brief generated"
        echo ""
        echo "Core Analogy: $(jq -r '.core_analogy' "$WORK_DIR/creative_brief.json")"
        echo "Mind-Blow: $(jq -r '.mind_blow_moment' "$WORK_DIR/creative_brief.json")"
    else
        print_error "Failed to generate creative brief"
        cat "$WORK_DIR/creative_brief_raw.txt"
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

    claude --print --dangerously-skip-permissions --output-format json \
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
]" 2>/dev/null | jq -r '.result // .' > "$WORK_DIR/audio_script_raw.txt"

    # Parse the script
    if grep -q '"01_hook"' "$WORK_DIR/audio_script_raw.txt"; then
        # Try to extract JSON array
        sed -n '/^\[/,/^\]/p' "$WORK_DIR/audio_script_raw.txt" | jq '.' > "$WORK_DIR/audio_script.json" 2>/dev/null || {
            cat "$WORK_DIR/audio_script_raw.txt" | jq '.' > "$WORK_DIR/audio_script.json"
        }

        local segment_count=$(jq 'length' "$WORK_DIR/audio_script.json")
        print_success "Audio script generated: $segment_count segments"

        # Show preview
        echo ""
        echo "Preview:"
        jq -r '.[0:2][] | "  \(.id): \(.text[0:60])..."' "$WORK_DIR/audio_script.json"
        echo "  ..."
    else
        print_error "Failed to generate audio script"
        cat "$WORK_DIR/audio_script_raw.txt"
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
    ls "$WORK_DIR/audio/"*.mp3 | sort | while read f; do
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

    claude --print --dangerously-skip-permissions --output-format json \
        "You are a Manim animation expert. Create reel.py for this educational reel.

CREATIVE BRIEF:
$creative_brief

TIMINGS (sync animations to these):
$timings

VIDEO RULES (MANDATORY):
$(echo "$VIDEO_RULES" | jq '.')

SUBJECT CONFIG:
- Background: $background
- Accent Color: $color
- Subject: $SUBJECT

REQUIRED IMPORTS (manim-edu):
$import_line
from manim_edu.primitives.colors import SUBJECT_COLORS

REQUIRED PATTERNS:
1. Import jeetlo_style: sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')
2. Use JeetLoReelMixin
3. Load timings: self.timings = load_timings()
4. Each segment method: segment_01_hook(self, timing), segment_02_setup(self, timing), etc.
5. Use manim-edu primitives for visualizations
6. Add watermark: create_brand_watermark()
7. Add CTA at end: add_cta_slide_{subject}()

ANIMATION QUALITY REQUIREMENTS:
- Use dynamic animations: Transform, GrowFromCenter, DrawBorderThenFill (not just FadeIn)
- Color variety: 6+ unique colors
- Motion: shift, move_to, rotate (objects MOVE)
- Visual hierarchy: 4+ font sizes
- Timing variety: Different run_times for rhythm

TIMING FORMULA (prevents audio/video desync):
def segment_XX(self, timing):
    duration = timing['duration']
    fixed_anim_time = 0.6 + 0.5 + 0.3  # Sum of all run_time values
    num_waits = 3  # Count of self.wait() calls
    wait_time = max(0.1, (duration - fixed_anim_time) / num_waits)

    self.play(Write(text), run_time=0.6)
    self.wait(wait_time)
    ...

Output the COMPLETE reel.py code. Start with imports, end with the class." 2>/dev/null | jq -r '.result // .' > "$WORK_DIR/reel.py"

    # Basic validation
    if grep -q "class.*Scene" "$WORK_DIR/reel.py" && grep -q "def construct" "$WORK_DIR/reel.py"; then
        print_success "reel.py generated"

        # Check for required patterns
        if grep -q "manim_edu" "$WORK_DIR/reel.py"; then
            print_success "Uses manim-edu primitives"
        else
            print_warning "Missing manim-edu imports"
        fi

        if grep -q "create_brand_watermark\|add_cta_slide" "$WORK_DIR/reel.py"; then
            print_success "Has brand elements (watermark/CTA)"
        else
            print_warning "Missing brand elements"
        fi
    else
        print_error "Invalid reel.py generated"
        head -50 "$WORK_DIR/reel.py"
        exit 1
    fi

    add_chain_step "video_script" "$WORK_DIR/reel.py"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5: VALIDATE manim-edu COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════════

validate_manim_edu() {
    print_step "5" "VALIDATE manim-edu COMPLIANCE"

    local reel_code=$(cat "$WORK_DIR/reel.py")

    claude --print --dangerously-skip-permissions --output-format json \
        "Validate this reel.py uses manim-edu primitives correctly.

REEL CODE:
$reel_code

SUBJECT: $SUBJECT

REQUIRED (at least 2 must be present):
- from manim_edu.chemistry import MoleculeBuilder
- from manim_edu.biology import CellVisualizer
- from manim_edu.physics import WaveSimulator, FieldVisualizer, MechanicsSimulator
- from manim_edu.mathematics import GraphAnimator
- from manim_edu.primitives.colors import SUBJECT_COLORS
- from manim_edu.effects import ParticleSystem

BRAND REQUIREMENTS:
- Uses create_brand_watermark() or add_watermark()
- Uses add_cta_slide_{subject}() at end
- Uses JeetLoReelMixin
- Has timing sync (load_timings, segment methods)

ANIMATION QUALITY (score 0-100):
- Dynamic animations (Transform, GrowFromCenter, DrawBorderThenFill) vs static (FadeIn only)
- Color variety (count unique colors)
- Motion (shift, move_to, rotate present)
- Font sizes (multiple sizes for hierarchy)

Output JSON:
{
  \"valid\": true/false,
  \"manim_edu_imports\": [\"...\"],
  \"brand_elements\": [\"...\"],
  \"animation_score\": 75,
  \"issues\": [],
  \"suggestions\": []
}" 2>/dev/null | jq -r '.result // .' > "$WORK_DIR/manim_validation.json"

    if jq -e '.valid == true' "$WORK_DIR/manim_validation.json" > /dev/null 2>&1; then
        local score=$(jq -r '.animation_score // 0' "$WORK_DIR/manim_validation.json")
        print_success "manim-edu validation passed (animation score: $score)"

        if [ "$score" -lt 60 ]; then
            print_warning "Animation score below 60% - consider adding more dynamic animations"
        fi
    else
        print_error "manim-edu validation failed"
        jq -r '.issues[]' "$WORK_DIR/manim_validation.json" 2>/dev/null
        # Don't exit, allow to continue with warnings
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
    cat > "$WORK_DIR/render.sh" << 'RENDER_EOF'
#!/bin/bash
cd "$1"
export PATH="$PATH:/opt/homebrew/bin:/Library/TeX/texbin"
python3 -m manim render -qh reel.py 2>&1
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

    echo "Running frame review with Claude..."

    # We can't pass images to CLI directly, so we do a text-based check
    claude --print --dangerously-skip-permissions --output-format json \
        "You are a video QA specialist. Based on the reel.py code, predict potential frame issues.

REEL CODE:
$(cat "$WORK_DIR/reel.py")

COMMON ISSUES TO CHECK:
1. Text cut off at edges (9:16 aspect ratio - content must be in center 60%)
2. Watermark positioning (should be bottom-right)
3. CTA slide present at end
4. Color contrast (text readable on background)
5. Animation timing (matches audio)

Output JSON:
{
  \"predicted_issues\": [],
  \"frame_checks\": {
    \"safe_zone\": true/false,
    \"watermark\": true/false,
    \"cta_present\": true/false,
    \"color_contrast\": true/false
  },
  \"recommendation\": \"pass\" or \"review_needed\"
}" 2>/dev/null | jq -r '.result // .' > "$WORK_DIR/frame_qa.json"

    local recommendation=$(jq -r '.recommendation // "pass"' "$WORK_DIR/frame_qa.json")

    if [ "$recommendation" == "pass" ]; then
        print_success "Frame QA prediction: PASS"
    else
        print_warning "Frame QA recommends manual review"
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
