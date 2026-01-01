"""
JeetLo Factory - Enforced Content Creation Pipeline
====================================================

This library is the ONLY way to create JeetLo reels.
All steps are tracked in a cryptographic manifest that CI validates.

Usage:
    from jeetlo_factory import Reel

    reel = Reel.create("bio-05-topic", subject="biology")
    reel.generate_audio(segments=[...])
    reel.render_video("ReelClassName")
    reel.combine()
    reel.validate()  # Must pass before posting
    reel.post(platforms=["instagram", "youtube"])
"""

from .reel import Reel
from .manifest import Manifest
from .exceptions import (
    ManifestError,
    ChainBrokenError,
    ValidationError,
    CINotPassedError
)

__version__ = "1.0.0"
__all__ = ["Reel", "Manifest"]

# Style module path for importing in reels
import os
STYLE_PATH = os.path.dirname(__file__)
