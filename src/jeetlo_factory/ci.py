"""
CI Validation Entry Point
=========================

This module is called by GitHub Actions to validate all reels.
It runs on GitHub's servers, so it CANNOT be bypassed.

Usage:
    python -m jeetlo_factory.ci /path/to/reels
    python -m jeetlo_factory.ci /path/to/reels --chain-only  # For GitHub CI

Exit codes:
    0 - All validations passed
    1 - Validation errors found
"""

import argparse
import sys
import os
import json
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


def validate_chain_only(reel_path: Path) -> Tuple[bool, List[str], List[str], dict]:
    """Validate only the manifest chain (for GitHub CI where media files aren't pushed)."""
    errors = []
    warnings = []
    metadata = {}

    manifest_path = reel_path / MANIFEST_FILENAME
    if not manifest_path.exists():
        errors.append("No manifest found")
        return False, errors, warnings, metadata

    try:
        with open(manifest_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {e}")
        return False, errors, warnings, metadata

    # Required fields
    required = ["version", "reel_id", "subject", "steps"]
    for field in required:
        if field not in data:
            errors.append(f"Missing field: {field}")

    if errors:
        return False, errors, warnings, metadata

    steps = data.get("steps", [])
    metadata["step_count"] = len(steps)
    metadata["status"] = data.get("status", "unknown")
    metadata["reel_id"] = data.get("reel_id", "unknown")

    # Verify hash chain
    if steps:
        # First step should have null input_hash
        if steps[0].get("input_hash") is not None:
            errors.append("First step must have null input_hash")

        # Each subsequent step's input must match previous output
        for i in range(1, len(steps)):
            prev_output = steps[i-1].get("output_hash")
            curr_input = steps[i].get("input_hash")

            if prev_output != curr_input:
                errors.append(
                    f"Chain broken at step '{steps[i].get('step_name')}': "
                    f"input_hash doesn't match previous output_hash"
                )

    # Check required steps for completed reels
    if data.get("status") == "completed":
        required_steps = ["create", "audio", "video", "combine"]
        step_names = [s.get("step_name") for s in steps]
        for req in required_steps:
            if req not in step_names:
                warnings.append(f"Missing step: {req}")

    return len(errors) == 0, errors, warnings, metadata


def validate_reel(reel_path: Path, chain_only: bool = False) -> Tuple[bool, List[str], List[str]]:
    """Validate a single reel."""
    if chain_only:
        valid, errors, warnings, _ = validate_chain_only(reel_path)
        return valid, errors, warnings

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


def write_github_summary(results: List[dict]):
    """Write summary to GitHub Actions."""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_file:
        return

    with open(summary_file, "a") as f:
        f.write("## 🔗 Chain Validation Results\n\n")

        total = len(results)
        passed = sum(1 for r in results if r["passed"])
        failed = total - passed

        f.write("| Metric | Count |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Total Manifests | {total} |\n")
        f.write(f"| ✅ Valid | {passed} |\n")
        f.write(f"| ❌ Invalid | {failed} |\n\n")

        if results:
            f.write("### Details\n\n")
            f.write("| Reel | Steps | Status | Chain |\n")
            f.write("|------|-------|--------|-------|\n")
            for r in results:
                status = r.get("metadata", {}).get("status", "?")
                steps = r.get("metadata", {}).get("step_count", 0)
                chain = "✅" if r["passed"] else "❌"
                f.write(f"| {r['reel_id']} | {steps} | {status} | {chain} |\n")

        f.write("\n")
        if failed > 0:
            f.write("### ❌ Failures\n\n")
            for r in results:
                if not r["passed"]:
                    f.write(f"**{r['reel_id']}**\n")
                    for err in r.get("errors", []):
                        f.write(f"- {err}\n")
                    f.write("\n")


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
    parser.add_argument(
        "--chain-only",
        action="store_true",
        help="Only validate manifest chain (for GitHub CI without media files)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("JeetLo Factory CI Validator")
    if args.chain_only:
        print("Mode: Chain-only (manifest validation)")
    else:
        print("Mode: Full validation (chain + media files)")
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
    results = []

    for reel in reels:
        print(f"Validating: {reel.name}")
        print("-" * 40)

        if args.chain_only:
            is_valid, errors, warnings, metadata = validate_chain_only(reel)
            results.append({
                "reel_id": reel.name,
                "passed": is_valid,
                "errors": errors,
                "warnings": warnings,
                "metadata": metadata
            })
        else:
            is_valid, errors, warnings = validate_reel(reel, chain_only=False)
            results.append({
                "reel_id": reel.name,
                "passed": is_valid,
                "errors": errors,
                "warnings": warnings,
                "metadata": {}
            })

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

    # Write GitHub summary
    write_github_summary(results)

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
