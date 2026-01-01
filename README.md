# JeetLo Factory

[![Chain Validation](https://github.com/pdaxt/jeetlo-factory/actions/workflows/validate.yml/badge.svg)](https://github.com/pdaxt/jeetlo-factory/actions/workflows/validate.yml)

**The ONLY way to create JeetLo reels.**

This library enforces a cryptographic chain for all content creation. Every step is tracked, validated, and verified by CI. **You cannot bypass this system.**

## Why This Exists

LLMs (like Claude) can bypass any trust-based system. This library creates an **enforced cage** where:

1. **Every step is tracked** in a cryptographic manifest
2. **CI validates** the chain on GitHub's servers (not locally)
3. **Posting requires** CI to pass (checked via GitHub API)
4. **Manual file creation** fails validation (no manifest = no post)

## The Enforcement Chain

```
Reel.create()     →  Creates directory + manifest (signed)
    ↓
generate_audio()  →  Validates pronunciation, generates TTS, records hash
    ↓
render_video()    →  Validates text language, renders Manim, records hash
    ↓
combine()         →  Combines A/V, records final hash
    ↓
validate()        →  Runs ALL validators, marks manifest validated
    ↓
post()            →  Checks CI passed via GitHub API, then posts
```

**If ANY step is skipped or faked, CI fails.**

## What Gets Validated

### Chain Validation
- Manifest exists and is valid
- All required steps completed
- Hash chain unbroken (each input = previous output)
- Git commits recorded

### Pronunciation Validation
- Scientific terms in Title Case (not ALL CAPS)
- Acronyms hyphenated (A-T-P, not ATP)
- Hindi in Devanagari (भाई, not BHAI)
- Numbers in English

### Text Validation
- On-screen text in English (not Hindi)
- Headers in proper format

### Audio Validation
- All segments generated
- Duration matches timings
- Combined audio exists

### Video Validation
- Resolution is 1080x1920
- Duration matches audio (within 1s)
- reel.py follows text rules

## Usage

```python
from jeetlo_factory import Reel

# 1. Create reel (generates manifest)
reel = Reel.create("bio-05-topic", subject="biology")

# 2. Generate audio (validates pronunciation first)
reel.generate_audio(segments=[
    {"id": "01_hook", "text": "हर cell में Nucleus होता है... WRONG!"},
    {"id": "02_explain", "text": "R-B-C में Nucleus नहीं होता!"},
    # ... more segments
])

# 3. Render video (validates text language first)
reel.render_video("ReelClassName")

# 4. Combine audio + video
reel.combine()

# 5. Validate everything
reel.validate()  # Must pass!

# 6. Post (checks CI status first)
reel.post(platforms=["instagram", "youtube"])
```

## CI Workflow

The `.github/workflows/validate.yml` runs on every push/PR:

```yaml
- name: Validate all reels
  run: python -m jeetlo_factory.ci . --fail-on-warnings
```

This runs on **GitHub's servers**, not locally. Claude cannot bypass it.

## What Happens If You Cheat

| Cheat Attempt | What Happens |
|---------------|--------------|
| Manual `mkdir` | No manifest → CI fails |
| Fake manifest | Invalid signatures → CI fails |
| Skip audio step | Chain broken → CI fails |
| Hindi text on screen | Text validation → CI fails |
| ALL CAPS terms | Pronunciation validation → CI fails |
| Try to post | CI status check → Blocked |

## The Key Insight

The enforcement works because:

1. **CI runs on GitHub's servers** - Claude can't modify it
2. **Git history is immutable** - Commits can't be faked
3. **Hash chains are cryptographic** - Can't forge hashes
4. **Posting checks GitHub API** - Claude can't fake API responses

## Installation

```bash
pip install -e /path/to/jeetlo-factory
```

## CLI

```bash
# Validate all reels
jeetlo-validate /path/to/reels

# With strict mode (warnings = errors)
jeetlo-validate /path/to/reels --fail-on-warnings
```
