"""
Chain Validator
===============

Validates the cryptographic chain in the manifest.
This is the CORE enforcement mechanism.

The chain validator checks:
1. Manifest exists and is valid JSON
2. All required steps are present
3. Hash chain is unbroken (each step's input = previous output)
4. Git commits are recorded
5. Files match their recorded hashes
"""

import json
from pathlib import Path
from typing import List, Tuple, Dict, Any

from ..manifest import Manifest, get_file_hash, get_directory_hash, MANIFEST_FILENAME
from ..exceptions import ChainBrokenError, ManifestError, ValidationError


REQUIRED_STEPS = ["create", "audio", "video", "combine"]


class ChainValidator:
    """Validates the cryptographic chain in a reel manifest."""

    def __init__(self, reel_path: str):
        self.reel_path = Path(reel_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """
        Run full chain validation.

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self._check_manifest_exists()
        if self.errors:
            return False, self.errors, self.warnings

        self._check_manifest_valid()
        if self.errors:
            return False, self.errors, self.warnings

        self._check_required_steps()
        self._check_hash_chain()
        self._check_file_hashes()
        self._check_git_commits()

        return len(self.errors) == 0, self.errors, self.warnings

    def _check_manifest_exists(self):
        """Check manifest file exists."""
        manifest_path = self.reel_path / MANIFEST_FILENAME
        if not manifest_path.exists():
            self.errors.append(
                f"CHAIN ERROR: No manifest found at {manifest_path}. "
                f"Reel must be created using jeetlo-factory library."
            )

    def _check_manifest_valid(self):
        """Check manifest is valid JSON with required fields."""
        manifest_path = self.reel_path / MANIFEST_FILENAME

        try:
            with open(manifest_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"CHAIN ERROR: Invalid manifest JSON: {e}")
            return

        required_fields = ["version", "reel_id", "subject", "created_at", "steps"]
        for field in required_fields:
            if field not in data:
                self.errors.append(f"CHAIN ERROR: Manifest missing required field: {field}")

    def _check_required_steps(self):
        """Check all required steps are present."""
        try:
            manifest = Manifest.load(str(self.reel_path))
        except ManifestError as e:
            self.errors.append(f"CHAIN ERROR: {e}")
            return

        completed_steps = [s["step_name"] for s in manifest.data.get("steps", [])]

        for step in REQUIRED_STEPS:
            if step not in completed_steps:
                self.errors.append(
                    f"CHAIN ERROR: Required step '{step}' not completed. "
                    f"Completed steps: {completed_steps}"
                )

    def _check_hash_chain(self):
        """Check the cryptographic hash chain is unbroken."""
        try:
            manifest = Manifest.load(str(self.reel_path))
            manifest.verify_chain()
        except ChainBrokenError as e:
            self.errors.append(f"CHAIN ERROR: {e}")
        except ManifestError as e:
            self.errors.append(f"CHAIN ERROR: {e}")

    def _check_file_hashes(self):
        """Verify files match their recorded hashes."""
        try:
            manifest = Manifest.load(str(self.reel_path))
        except ManifestError:
            return  # Already reported

        for step in manifest.data.get("steps", []):
            step_name = step["step_name"]
            output_hash = step.get("output_hash")
            metadata = step.get("metadata", {})

            # Check specific files based on step
            if step_name == "audio":
                audio_dir = self.reel_path / "audio"
                if audio_dir.exists():
                    current_hash = get_directory_hash(str(audio_dir), [".mp3", ".json"])
                    if current_hash != output_hash:
                        self.errors.append(
                            f"CHAIN ERROR: Audio files have been modified after step was recorded. "
                            f"Expected hash: {output_hash[:16]}..., Current: {current_hash[:16]}..."
                        )

            elif step_name == "video":
                # Check for video file
                video_files = list(self.reel_path.rglob("*.mp4"))
                if video_files and "video_hash" in metadata:
                    for vf in video_files:
                        if "final" not in vf.name:  # Skip final.mp4
                            current_hash = get_file_hash(str(vf))
                            if current_hash != metadata["video_hash"]:
                                self.warnings.append(
                                    f"WARNING: Video file {vf.name} hash mismatch"
                                )

    def _check_git_commits(self):
        """Check git commits are recorded for each step."""
        try:
            manifest = Manifest.load(str(self.reel_path))
        except ManifestError:
            return

        for step in manifest.data.get("steps", []):
            if not step.get("git_commit"):
                self.warnings.append(
                    f"WARNING: Step '{step['step_name']}' has no git commit recorded"
                )

            if step.get("git_has_uncommitted_changes"):
                self.warnings.append(
                    f"WARNING: Step '{step['step_name']}' was recorded with uncommitted changes"
                )


def validate_reel(reel_path: str) -> Tuple[bool, List[str], List[str]]:
    """
    Validate a reel's chain.

    This is the main entry point for CI validation.
    """
    validator = ChainValidator(reel_path)
    return validator.validate()
