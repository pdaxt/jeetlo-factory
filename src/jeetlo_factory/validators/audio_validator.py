"""
Audio Validator
===============

Validates audio files and scripts:
1. Audio duration matches timings.json
2. Combined audio exists
3. All segment files exist
4. Script follows pronunciation rules
"""

import json
import subprocess
from pathlib import Path
from typing import List, Tuple

from .pronunciation_validator import PronunciationValidator


def get_audio_duration(filepath: str) -> float:
    """Get duration of an audio file using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                filepath
            ],
            capture_output=True,
            text=True
        )
        return float(result.stdout.strip())
    except (ValueError, subprocess.SubprocessError):
        return 0.0


class AudioValidator:
    """Validates audio files and configuration."""

    def __init__(self, reel_path: str):
        self.reel_path = Path(reel_path)
        self.audio_dir = self.reel_path / "audio"
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """
        Run all audio validations.

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self._check_audio_dir_exists()
        if self.errors:
            return False, self.errors, self.warnings

        self._check_timings_json()
        self._check_combined_audio()
        self._check_segment_files()
        self._check_script_pronunciation()

        return len(self.errors) == 0, self.errors, self.warnings

    def _check_audio_dir_exists(self):
        """Check audio directory exists."""
        if not self.audio_dir.exists():
            self.errors.append(
                f"AUDIO ERROR: No audio directory found at {self.audio_dir}"
            )

    def _check_timings_json(self):
        """Check timings.json exists and is valid."""
        timings_path = self.audio_dir / "timings.json"
        if not timings_path.exists():
            self.errors.append("AUDIO ERROR: No timings.json found")
            return

        try:
            with open(timings_path, "r") as f:
                timings = json.load(f)

            if not isinstance(timings, list):
                self.errors.append("AUDIO ERROR: timings.json must be a list")
                return

            for i, segment in enumerate(timings):
                required = ["id", "file", "duration"]
                for field in required:
                    if field not in segment:
                        self.errors.append(
                            f"AUDIO ERROR: Segment {i} missing required field: {field}"
                        )

        except json.JSONDecodeError as e:
            self.errors.append(f"AUDIO ERROR: Invalid timings.json: {e}")

    def _check_combined_audio(self):
        """Check combined audio exists and duration matches."""
        combined = self.audio_dir / "combined_audio.mp3"
        if not combined.exists():
            self.errors.append("AUDIO ERROR: No combined_audio.mp3 found")
            return

        timings_path = self.audio_dir / "timings.json"
        if timings_path.exists():
            try:
                with open(timings_path, "r") as f:
                    timings = json.load(f)

                expected_duration = sum(s.get("duration", 0) for s in timings)
                actual_duration = get_audio_duration(str(combined))

                if abs(actual_duration - expected_duration) > 1.0:
                    self.errors.append(
                        f"AUDIO ERROR: Combined audio duration ({actual_duration:.2f}s) "
                        f"doesn't match timings ({expected_duration:.2f}s)"
                    )
            except (json.JSONDecodeError, KeyError):
                pass

    def _check_segment_files(self):
        """Check all segment files exist."""
        timings_path = self.audio_dir / "timings.json"
        if not timings_path.exists():
            return

        try:
            with open(timings_path, "r") as f:
                timings = json.load(f)

            for segment in timings:
                segment_file = self.audio_dir / segment.get("file", "")
                if not segment_file.exists():
                    self.errors.append(
                        f"AUDIO ERROR: Segment file missing: {segment.get('file')}"
                    )
        except json.JSONDecodeError:
            pass

    def _check_script_pronunciation(self):
        """Validate pronunciation in the script."""
        # Check generate-audio-sdk.js
        script_files = list(self.reel_path.glob("generate-audio*.js"))

        for script_file in script_files:
            with open(script_file, "r") as f:
                content = f.read()

            validator = PronunciationValidator(content)
            is_valid, errors, warnings = validator.validate()

            self.errors.extend(errors)
            self.warnings.extend(warnings)

        # Also check timings.json for text content
        timings_path = self.audio_dir / "timings.json"
        if timings_path.exists():
            with open(timings_path, "r") as f:
                content = f.read()

            validator = PronunciationValidator(content)
            is_valid, errors, warnings = validator.validate()

            self.errors.extend(errors)
            self.warnings.extend(warnings)


def validate_audio(reel_path: str) -> Tuple[bool, List[str], List[str]]:
    """Validate audio for a reel."""
    validator = AudioValidator(reel_path)
    return validator.validate()
