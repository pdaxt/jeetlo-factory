"""
Manifest - Cryptographic Chain for Content Creation
====================================================

The manifest tracks every step of reel creation with:
1. Timestamps (when each step occurred)
2. File hashes (SHA256 of inputs/outputs)
3. Git commit SHA (links to immutable git history)
4. External service IDs (TTS request IDs that can be verified)

The chain is cryptographic:
- Each step's input_hash must match the previous step's output_hash
- The git_commit ties the manifest to an immutable point in history
- External IDs can be verified against third-party logs

CI validates this entire chain. If any link is broken, CI fails.
"""

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .exceptions import ManifestError, ChainBrokenError


MANIFEST_VERSION = "1.0.0"
MANIFEST_FILENAME = ".jeetlo_manifest.json"


def get_file_hash(filepath: str) -> str:
    """Get SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_directory_hash(dirpath: str, extensions: List[str] = None) -> str:
    """Get combined hash of all files in a directory."""
    sha256 = hashlib.sha256()
    dirpath = Path(dirpath)

    files = sorted(dirpath.rglob("*"))
    for f in files:
        if f.is_file():
            if extensions is None or f.suffix in extensions:
                sha256.update(f.name.encode())
                sha256.update(get_file_hash(str(f)).encode())

    return sha256.hexdigest()


def get_git_commit() -> Optional[str]:
    """Get current git commit SHA."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def get_git_status() -> Dict[str, Any]:
    """Get git status info."""
    try:
        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        has_changes = bool(result.stdout.strip())

        return {
            "commit": get_git_commit(),
            "has_uncommitted_changes": has_changes
        }
    except Exception:
        return {"commit": None, "has_uncommitted_changes": True}


class Manifest:
    """
    Cryptographic manifest for tracking reel creation steps.

    Each step in the pipeline records:
    - step_name: Name of the step (create, audio, video, combine)
    - timestamp: ISO format UTC timestamp
    - input_hash: Hash of inputs (must match previous output_hash)
    - output_hash: Hash of outputs (becomes next step's input_hash)
    - git_commit: Current git commit SHA
    - metadata: Step-specific data (TTS request IDs, etc.)
    """

    def __init__(self, reel_path: str):
        self.reel_path = Path(reel_path)
        self.manifest_path = self.reel_path / MANIFEST_FILENAME
        self.data: Dict[str, Any] = {}

    @classmethod
    def create(cls, reel_path: str, reel_id: str, subject: str) -> "Manifest":
        """Create a new manifest for a reel."""
        manifest = cls(reel_path)
        manifest.data = {
            "version": MANIFEST_VERSION,
            "reel_id": reel_id,
            "subject": subject,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "steps": [],
            "status": "in_progress"
        }
        manifest.save()
        return manifest

    @classmethod
    def load(cls, reel_path: str) -> "Manifest":
        """Load existing manifest from a reel directory."""
        manifest = cls(reel_path)
        if not manifest.manifest_path.exists():
            raise ManifestError(f"No manifest found at {manifest.manifest_path}")

        try:
            with open(manifest.manifest_path, "r") as f:
                manifest.data = json.load(f)
        except json.JSONDecodeError as e:
            raise ManifestError(f"Invalid manifest JSON: {e}")

        return manifest

    def save(self):
        """Save manifest to disk."""
        with open(self.manifest_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_last_output_hash(self) -> Optional[str]:
        """Get the output hash of the last completed step."""
        if not self.data.get("steps"):
            return None
        return self.data["steps"][-1].get("output_hash")

    def add_step(
        self,
        step_name: str,
        input_hash: Optional[str],
        output_hash: str,
        metadata: Dict[str, Any] = None
    ):
        """
        Add a step to the manifest.

        The input_hash MUST match the previous step's output_hash.
        This creates an unbreakable chain.
        """
        # Verify chain integrity
        last_output = self.get_last_output_hash()
        if last_output is not None and input_hash != last_output:
            raise ChainBrokenError(
                f"Chain broken at step '{step_name}': "
                f"input_hash ({input_hash[:8]}...) != "
                f"previous output_hash ({last_output[:8]}...)"
            )

        git_info = get_git_status()

        step = {
            "step_name": step_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_hash": input_hash,
            "output_hash": output_hash,
            "git_commit": git_info["commit"],
            "git_has_uncommitted_changes": git_info["has_uncommitted_changes"],
            "metadata": metadata or {}
        }

        self.data["steps"].append(step)
        self.save()

    def get_step(self, step_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific step from the manifest."""
        for step in self.data.get("steps", []):
            if step["step_name"] == step_name:
                return step
        return None

    def has_step(self, step_name: str) -> bool:
        """Check if a step has been completed."""
        return self.get_step(step_name) is not None

    def verify_chain(self) -> bool:
        """
        Verify the entire cryptographic chain is intact.

        Returns True if valid, raises ChainBrokenError if not.
        """
        steps = self.data.get("steps", [])

        for i, step in enumerate(steps):
            if i == 0:
                # First step should have no input_hash
                if step.get("input_hash") is not None:
                    raise ChainBrokenError(
                        f"First step '{step['step_name']}' should have null input_hash"
                    )
            else:
                # Subsequent steps must chain
                prev_output = steps[i - 1].get("output_hash")
                curr_input = step.get("input_hash")
                if curr_input != prev_output:
                    raise ChainBrokenError(
                        f"Chain broken between step {i-1} and {i}: "
                        f"{prev_output[:8]}... != {curr_input[:8]}..."
                    )

        return True

    def mark_validated(self):
        """Mark the manifest as validated."""
        self.data["status"] = "validated"
        self.data["validated_at"] = datetime.now(timezone.utc).isoformat()
        self.save()

    def mark_posted(self, platform: str, post_id: str):
        """Record a successful post."""
        if "posts" not in self.data:
            self.data["posts"] = []

        self.data["posts"].append({
            "platform": platform,
            "post_id": post_id,
            "posted_at": datetime.now(timezone.utc).isoformat()
        })
        self.data["status"] = "posted"
        self.save()

    def to_dict(self) -> Dict[str, Any]:
        """Return manifest as dictionary."""
        return self.data.copy()
