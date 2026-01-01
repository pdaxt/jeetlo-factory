"""
CI Validation Entry Point
=========================

This module is called by GitHub Actions to validate all reels.
It runs on GitHub's servers, so it CANNOT be bypassed.

Usage:
    python -m jeetlo_factory.ci /path/to/reels

Exit codes:
    0 - All validations passed
    1 - Validation errors found
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple

from .validators import ChainValidator, AudioValidator, VideoValidator
from .manifest import MANIFEST_FILENAME


def find_reels(base_path: str) -> List[Path]:
    """Find all reel directories (those with manifests)."""
    base = Path(base_path)
    reels = []

    for manifest in base.rglob(MANIFEST_FILENAME):
        reels.append(manifest.parent)

    return reels


def validate_reel(reel_path: Path) -> Tuple[bool, List[str], List[str]]:
    """Validate a single reel."""
    all_errors = []
    all_warnings = []

    # Chain validation
    chain_val = ChainValidator(str(reel_path))
    _, errors, warnings = chain_val.validate()
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    # Audio validation
    audio_val = AudioValidator(str(reel_path))
    _, errors, warnings = audio_val.validate()
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    # Video validation
    video_val = VideoValidator(str(reel_path))
    _, errors, warnings = video_val.validate()
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    return len(all_errors) == 0, all_errors, all_warnings


def main():
    parser = argparse.ArgumentParser(
        description="JeetLo Factory CI Validator"
    )
    parser.add_argument(
        "path",
        help="Path to validate (directory containing reels)"
    )
    parser.add_argument(
        "--fail-on-warnings",
        action="store_true",
        help="Treat warnings as errors"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("JeetLo Factory CI Validator")
    print("=" * 60)

    # Find all reels
    reels = find_reels(args.path)

    if not reels:
        print(f"No reels found in {args.path}")
        print("Reels must have a .jeetlo_manifest.json file")
        sys.exit(0)

    print(f"\nFound {len(reels)} reel(s) to validate:\n")

    total_errors = 0
    total_warnings = 0

    for reel in reels:
        print(f"Validating: {reel.name}")
        print("-" * 40)

        is_valid, errors, warnings = validate_reel(reel)

        if warnings:
            for w in warnings:
                print(f"  ⚠ {w}")
            total_warnings += len(warnings)

        if errors:
            for e in errors:
                print(f"  ✗ {e}")
            total_errors += len(errors)
            print(f"  FAILED: {len(errors)} error(s)\n")
        else:
            print(f"  ✓ PASSED\n")

    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Reels validated: {len(reels)}")
    print(f"Total errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")

    if total_errors > 0:
        print("\n✗ CI FAILED")
        sys.exit(1)

    if args.fail_on_warnings and total_warnings > 0:
        print("\n✗ CI FAILED (warnings treated as errors)")
        sys.exit(1)

    print("\n✓ CI PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
