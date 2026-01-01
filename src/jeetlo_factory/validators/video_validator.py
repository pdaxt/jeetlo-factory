"""
Video Validator
===============

Validates video files and reel code:
1. Video duration matches audio
2. Video resolution is correct (1080x1920)
3. Reel code follows text language rules
4. Final video exists
"""

import subprocess
from pathlib import Path
from typing import List, Tuple, Dict, Any

from .text_validator import TextValidator


def get_video_info(filepath: str) -> Dict[str, Any]:
    """Get video info using ffprobe."""
    try:
        # Get duration
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
        duration = float(result.stdout.strip())

        # Get resolution
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height",
                "-of", "csv=p=0",
                filepath
            ],
            capture_output=True,
            text=True
        )
        width, height = map(int, result.stdout.strip().split(","))

        return {
            "duration": duration,
            "width": width,
            "height": height
        }
    except (ValueError, subprocess.SubprocessError):
        return {"duration": 0, "width": 0, "height": 0}


class VideoValidator:
    """Validates video files and configuration."""

    def __init__(self, reel_path: str):
        self.reel_path = Path(reel_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """
        Run all video validations.

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self._check_final_video()
        self._check_video_resolution()
        self._check_duration_sync()
        self._check_reel_code()

        return len(self.errors) == 0, self.errors, self.warnings

    def _check_final_video(self):
        """Check final.mp4 exists."""
        final_video = self.reel_path / "final.mp4"
        if not final_video.exists():
            self.errors.append("VIDEO ERROR: No final.mp4 found")

    def _check_video_resolution(self):
        """Check video is correct resolution for reels (1080x1920)."""
        final_video = self.reel_path / "final.mp4"
        if not final_video.exists():
            return

        info = get_video_info(str(final_video))

        if info["width"] != 1080 or info["height"] != 1920:
            self.errors.append(
                f"VIDEO ERROR: Resolution must be 1080x1920 for reels. "
                f"Got: {info['width']}x{info['height']}"
            )

    def _check_duration_sync(self):
        """Check video duration matches audio duration."""
        final_video = self.reel_path / "final.mp4"
        combined_audio = self.reel_path / "audio" / "combined_audio.mp3"

        if not final_video.exists() or not combined_audio.exists():
            return

        video_info = get_video_info(str(final_video))
        video_duration = video_info["duration"]

        # Get audio duration
        try:
            result = subprocess.run(
                [
                    "ffprobe", "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    str(combined_audio)
                ],
                capture_output=True,
                text=True
            )
            audio_duration = float(result.stdout.strip())
        except (ValueError, subprocess.SubprocessError):
            return

        diff = abs(video_duration - audio_duration)
        if diff > 1.0:
            self.errors.append(
                f"VIDEO ERROR: Duration mismatch. "
                f"Video: {video_duration:.2f}s, Audio: {audio_duration:.2f}s, "
                f"Diff: {diff:.2f}s (max allowed: 1.0s)"
            )
        elif diff > 0.5:
            self.warnings.append(
                f"WARNING: Duration difference is {diff:.2f}s (consider tightening)"
            )

    def _check_reel_code(self):
        """Check reel.py for text language issues."""
        reel_py = self.reel_path / "reel.py"
        if not reel_py.exists():
            self.errors.append("VIDEO ERROR: No reel.py found")
            return

        with open(reel_py, "r") as f:
            content = f.read()

        validator = TextValidator(content)
        is_valid, errors, warnings = validator.validate()

        self.errors.extend(errors)
        self.warnings.extend(warnings)


def validate_video(reel_path: str) -> Tuple[bool, List[str], List[str]]:
    """Validate video for a reel."""
    validator = VideoValidator(reel_path)
    return validator.validate()
