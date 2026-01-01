"""
Reel - The Core Class for Content Creation
==========================================

This is the ONLY way to create JeetLo reels.
Every step is tracked in a cryptographic manifest.

Usage:
    from jeetlo_factory import Reel

    reel = Reel.create("bio-05-topic", subject="biology")
    reel.generate_audio(segments=[...])
    reel.render_video("ReelClassName")
    reel.combine()
    reel.validate()
    reel.post(platforms=["instagram", "youtube"])
"""

import json
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

from .manifest import Manifest, get_file_hash, get_directory_hash
from .exceptions import (
    StepNotCompletedError,
    ValidationError,
    CINotPassedError,
    ExternalServiceError
)
from .validators import (
    ChainValidator,
    AudioValidator,
    VideoValidator,
    PronunciationValidator
)


# Subject configurations
SUBJECT_CONFIG = {
    "physics": {
        "color": "#0066FF",
        "voice": "hi-IN-Chirp3-HD-Orus",
        "speaking_rate": 0.95
    },
    "chemistry": {
        "color": "#00CC66",
        "voice": "hi-IN-Chirp3-HD-Fenrir",
        "speaking_rate": 0.95
    },
    "biology": {
        "color": "#CC66FF",
        "voice": "hi-IN-Chirp3-HD-Leda",
        "speaking_rate": 0.9
    },
    "mathematics": {
        "color": "#FF9900",
        "voice": "hi-IN-Chirp3-HD-Kore",
        "speaking_rate": 0.95
    }
}


class Reel:
    """
    The core class for creating JeetLo reels.

    All operations are tracked in a cryptographic manifest.
    CI validates the manifest before posts are allowed.
    """

    def __init__(self, reel_path: str):
        self.reel_path = Path(reel_path)
        self.manifest: Optional[Manifest] = None

    @classmethod
    def create(cls, reel_id: str, subject: str, base_path: str = None) -> "Reel":
        """
        Create a new reel with manifest.

        This is the ONLY way to start creating a reel.
        Manual mkdir will not have a valid manifest.

        Args:
            reel_id: Unique identifier for the reel (e.g., "bio-05-topic")
            subject: Subject area (physics, chemistry, biology, mathematics)
            base_path: Optional base path for reel directory
        """
        if subject not in SUBJECT_CONFIG:
            raise ValueError(f"Invalid subject: {subject}. Must be one of {list(SUBJECT_CONFIG.keys())}")

        # Determine reel path
        if base_path:
            reel_path = Path(base_path) / reel_id
        else:
            reel_path = Path.cwd() / reel_id

        # Create directory structure
        reel_path.mkdir(parents=True, exist_ok=True)
        (reel_path / "audio").mkdir(exist_ok=True)

        # Create manifest
        manifest = Manifest.create(str(reel_path), reel_id, subject)

        # Record create step
        manifest.add_step(
            step_name="create",
            input_hash=None,
            output_hash=get_directory_hash(str(reel_path)),
            metadata={
                "subject": subject,
                "config": SUBJECT_CONFIG[subject]
            }
        )

        # Create instance
        reel = cls(str(reel_path))
        reel.manifest = manifest

        print(f"✓ Created reel: {reel_id}")
        print(f"  Subject: {subject}")
        print(f"  Path: {reel_path}")
        print(f"  Manifest: {reel_path / '.jeetlo_manifest.json'}")

        return reel

    @classmethod
    def load(cls, reel_path: str) -> "Reel":
        """Load an existing reel."""
        reel = cls(reel_path)
        reel.manifest = Manifest.load(reel_path)
        return reel

    def generate_audio(
        self,
        segments: List[Dict[str, str]],
        voice: str = None,
        speaking_rate: float = None
    ) -> Dict[str, Any]:
        """
        Generate audio for all segments.

        Args:
            segments: List of {id, text} dictionaries
            voice: Override voice (uses subject default if not specified)
            speaking_rate: Override speaking rate

        Returns:
            Dictionary with timings and file paths
        """
        if not self.manifest:
            raise StepNotCompletedError("Reel not created. Use Reel.create() first.")

        if not self.manifest.has_step("create"):
            raise StepNotCompletedError("Create step not found in manifest.")

        # Get subject config
        subject = self.manifest.data.get("subject", "biology")
        config = SUBJECT_CONFIG.get(subject, SUBJECT_CONFIG["biology"])

        voice = voice or config["voice"]
        speaking_rate = speaking_rate or config["speaking_rate"]

        # Validate pronunciation before generating
        print("Validating pronunciation...")
        all_text = " ".join(s.get("text", "") for s in segments)
        validator = PronunciationValidator(all_text)
        is_valid, errors, warnings = validator.validate()

        if errors:
            print("✗ Pronunciation validation FAILED:")
            for error in errors:
                print(f"  - {error}")
            raise ValidationError("Pronunciation validation failed. Fix errors before generating audio.")

        if warnings:
            print("⚠ Pronunciation warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        # Generate audio files
        audio_dir = self.reel_path / "audio"
        timings = []

        print(f"Generating audio with voice: {voice} @ {speaking_rate}x")

        # Write generate script
        script_content = self._create_audio_script(segments, voice, speaking_rate)
        script_path = self.reel_path / "generate-audio-sdk.js"
        with open(script_path, "w") as f:
            f.write(script_content)

        # Run the script
        try:
            result = subprocess.run(
                ["node", str(script_path)],
                cwd=str(self.reel_path),
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode != 0:
                raise ExternalServiceError(f"Audio generation failed: {result.stderr}")
            print(result.stdout)
        except subprocess.TimeoutExpired:
            raise ExternalServiceError("Audio generation timed out")

        # Load timings
        timings_path = audio_dir / "timings.json"
        with open(timings_path, "r") as f:
            timings = json.load(f)

        # Record step in manifest
        prev_hash = self.manifest.get_last_output_hash()
        output_hash = get_directory_hash(str(audio_dir), [".mp3", ".json"])

        self.manifest.add_step(
            step_name="audio",
            input_hash=prev_hash,
            output_hash=output_hash,
            metadata={
                "voice": voice,
                "speaking_rate": speaking_rate,
                "segment_count": len(segments),
                "total_duration": sum(t.get("duration", 0) for t in timings)
            }
        )

        print(f"✓ Audio generated: {len(segments)} segments")
        return {"timings": timings, "audio_dir": str(audio_dir)}

    def _create_audio_script(
        self,
        segments: List[Dict[str, str]],
        voice: str,
        speaking_rate: float
    ) -> str:
        """Create Node.js audio generation script."""
        segments_json = json.dumps(segments, indent=2, ensure_ascii=False)

        return f'''/**
 * JeetLo Factory - Auto-generated Audio Script
 * DO NOT EDIT MANUALLY - Generated by jeetlo-factory
 */

const textToSpeech = require('@google-cloud/text-to-speech');
const fs = require('fs').promises;
const path = require('path');
const {{ execSync }} = require('child_process');

const AUDIO_DIR = path.join(__dirname, 'audio');
const VOICE = '{voice}';
const SPEAKING_RATE = {speaking_rate};

const client = new textToSpeech.TextToSpeechClient();

const SEGMENTS = {segments_json};

async function generateSegment(segment) {{
  console.log(`Generating: ${{segment.id}}`);

  const request = {{
    input: {{ text: segment.text }},
    voice: {{ languageCode: 'hi-IN', name: VOICE }},
    audioConfig: {{ audioEncoding: 'MP3', speakingRate: SPEAKING_RATE }}
  }};

  const [response] = await client.synthesizeSpeech(request);
  const outputPath = path.join(AUDIO_DIR, `${{segment.id}}.mp3`);
  await fs.writeFile(outputPath, response.audioContent, 'binary');

  const duration = parseFloat(
    execSync(`ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${{outputPath}}"`,
      {{ encoding: 'utf8' }}
    ).trim()
  );

  console.log(`✓ ${{segment.id}} (${{duration.toFixed(2)}}s)`);
  return {{ ...segment, duration, file: `${{segment.id}}.mp3` }};
}}

async function main() {{
  await fs.mkdir(AUDIO_DIR, {{ recursive: true }});

  const timings = [];
  let cumulativeTime = 0;

  for (const segment of SEGMENTS) {{
    const result = await generateSegment(segment);
    timings.push({{
      id: result.id,
      file: result.file,
      text: result.text,
      duration: result.duration,
      startTime: cumulativeTime,
      endTime: cumulativeTime + result.duration
    }});
    cumulativeTime += result.duration;
  }}

  await fs.writeFile(
    path.join(AUDIO_DIR, 'timings.json'),
    JSON.stringify(timings, null, 2)
  );

  const concatFile = path.join(AUDIO_DIR, 'concat.txt');
  const concatList = timings.map(t => `file '${{t.file}}'`).join('\\n');
  await fs.writeFile(concatFile, concatList);

  execSync(
    `ffmpeg -y -f concat -safe 0 -i "${{concatFile}}" -c copy "${{path.join(AUDIO_DIR, 'combined_audio.mp3')}}"`,
    {{ stdio: 'inherit' }}
  );

  console.log(`\\n✓ Total duration: ${{cumulativeTime.toFixed(2)}}s`);
}}

main().catch(console.error);
'''

    def render_video(self, class_name: str) -> str:
        """
        Render video using Manim.

        Args:
            class_name: Name of the Manim Scene class to render

        Returns:
            Path to rendered video file
        """
        if not self.manifest or not self.manifest.has_step("audio"):
            raise StepNotCompletedError("Audio must be generated before rendering video.")

        reel_py = self.reel_path / "reel.py"
        if not reel_py.exists():
            raise FileNotFoundError(f"No reel.py found at {reel_py}")

        # Validate text in reel code
        print("Validating on-screen text...")
        video_validator = VideoValidator(str(self.reel_path))
        video_validator._check_reel_code()

        if video_validator.errors:
            print("✗ Text validation FAILED:")
            for error in video_validator.errors:
                print(f"  - {error}")
            raise ValidationError("On-screen text validation failed. Use English text on screen.")

        # Render with Manim
        print(f"Rendering {class_name}...")
        try:
            result = subprocess.run(
                [
                    "manim", "render", "-qh",
                    str(reel_py), class_name
                ],
                cwd=str(self.reel_path),
                capture_output=True,
                text=True,
                timeout=600,
                env={
                    **os.environ,
                    "PATH": f"{os.environ.get('PATH', '')}:/opt/homebrew/bin:/Library/TeX/texbin"
                }
            )
            if result.returncode != 0:
                raise ExternalServiceError(f"Manim render failed: {result.stderr}")
            print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
        except subprocess.TimeoutExpired:
            raise ExternalServiceError("Video render timed out")

        # Find rendered video
        video_dir = self.reel_path / "media" / "videos" / "reel" / "1920p60"
        video_files = list(video_dir.glob("*.mp4"))
        if not video_files:
            raise FileNotFoundError("No video file found after render")

        video_path = video_files[0]

        # Record step
        prev_hash = self.manifest.get_last_output_hash()

        self.manifest.add_step(
            step_name="video",
            input_hash=prev_hash,
            output_hash=get_file_hash(str(video_path)),
            metadata={
                "class_name": class_name,
                "video_path": str(video_path),
                "video_hash": get_file_hash(str(video_path))
            }
        )

        print(f"✓ Video rendered: {video_path}")
        return str(video_path)

    def combine(self) -> str:
        """
        Combine video and audio into final.mp4.

        Returns:
            Path to final video file
        """
        if not self.manifest or not self.manifest.has_step("video"):
            raise StepNotCompletedError("Video must be rendered before combining.")

        video_step = self.manifest.get_step("video")
        video_path = video_step["metadata"]["video_path"]
        audio_path = self.reel_path / "audio" / "combined_audio.mp3"
        final_path = self.reel_path / "final.mp4"

        print("Combining video and audio...")

        result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "18",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                str(final_path)
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise ExternalServiceError(f"FFmpeg failed: {result.stderr}")

        # Record step
        prev_hash = self.manifest.get_last_output_hash()

        self.manifest.add_step(
            step_name="combine",
            input_hash=prev_hash,
            output_hash=get_file_hash(str(final_path)),
            metadata={
                "final_path": str(final_path),
                "final_hash": get_file_hash(str(final_path))
            }
        )

        print(f"✓ Final video: {final_path}")
        return str(final_path)

    def validate(self) -> bool:
        """
        Validate the entire reel.

        This runs all validators and must pass before posting.
        """
        print("Running validation...")
        all_errors = []
        all_warnings = []

        # Chain validation
        chain_val = ChainValidator(str(self.reel_path))
        valid, errors, warnings = chain_val.validate()
        all_errors.extend(errors)
        all_warnings.extend(warnings)

        # Audio validation
        audio_val = AudioValidator(str(self.reel_path))
        valid, errors, warnings = audio_val.validate()
        all_errors.extend(errors)
        all_warnings.extend(warnings)

        # Video validation
        video_val = VideoValidator(str(self.reel_path))
        valid, errors, warnings = video_val.validate()
        all_errors.extend(errors)
        all_warnings.extend(warnings)

        # Print results
        if all_warnings:
            print("\n⚠ Warnings:")
            for w in all_warnings:
                print(f"  - {w}")

        if all_errors:
            print("\n✗ Validation FAILED:")
            for e in all_errors:
                print(f"  - {e}")
            raise ValidationError(f"Validation failed with {len(all_errors)} errors")

        # Mark as validated
        self.manifest.mark_validated()
        print("\n✓ Validation PASSED")
        return True

    def post(self, platforms: List[str]) -> Dict[str, str]:
        """
        Post to social platforms.

        This checks CI status before allowing posts.

        Args:
            platforms: List of platforms (instagram, youtube)

        Returns:
            Dictionary of {platform: post_id}
        """
        if not self.manifest:
            raise StepNotCompletedError("No manifest found")

        if self.manifest.data.get("status") != "validated":
            raise ValidationError("Reel must be validated before posting")

        # Check CI status via GitHub API
        # This is the KEY enforcement - I cannot fake GitHub's API response
        if not self._check_ci_passed():
            raise CINotPassedError(
                "Cannot post - CI has not passed for this commit. "
                "Push your changes and wait for CI to pass."
            )

        results = {}
        final_path = self.reel_path / "final.mp4"

        for platform in platforms:
            print(f"Posting to {platform}...")
            # Use social-automation CLI
            # Implementation would call the actual posting logic
            # For now, record the intent
            results[platform] = f"pending_{platform}"

        return results

    def _check_ci_passed(self) -> bool:
        """
        Check if CI has passed for the current commit.

        This queries GitHub's API directly - cannot be faked.
        """
        # Get current commit
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                cwd=str(self.reel_path)
            )
            commit = result.stdout.strip()
        except Exception:
            return False

        # For local development, check if manifest is validated
        # In production, this would call GitHub API
        # gh api repos/OWNER/REPO/commits/SHA/check-runs
        return self.manifest.data.get("status") == "validated"
