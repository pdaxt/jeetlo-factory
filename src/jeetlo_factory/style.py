"""
JeetLo.ai - Shared Reel Style
==============================
Single source of truth for all visual styling across all 4 subjects.

Usage:
    from jeetlo_factory.style import *

    class MyReel(JeetLoReelMixin, Scene):
        subject = "biology"

        def construct(self):
            self.set_subject_background("biology")
            watermark = create_brand_watermark()
            self.add(watermark)
            # ... your content ...
"""

from manim import *
import json
import os

# ============================================
# FRAME CONFIGURATION (9:16 Vertical)
# ============================================
FRAME_WIDTH = 8
FRAME_HEIGHT = 14.22
PIXEL_WIDTH = 1080
PIXEL_HEIGHT = 1920

# ============================================
# BRAND COLORS
# ============================================
BG_COLOR = "#0D0D0D"  # Near black

# Subject colors
SUBJECT_COLORS = {
    "physics": "#0066FF",      # Electric blue
    "chemistry": "#00CC66",    # Emerald green
    "biology": "#CC66FF",      # Violet purple
    "mathematics": "#FF9900",  # Orange
}

# Subject backgrounds (darker versions)
SUBJECT_BACKGROUNDS = {
    "physics": "#0A1628",      # Dark blue
    "chemistry": "#0A1F14",    # Dark green
    "biology": "#1A0A2E",      # Dark purple
    "mathematics": "#1F1408",  # Dark orange
}

# Common colors
PRIMARY = "#FFFFFF"
SECONDARY = "#B0B0B0"
ACCENT = "#FFD700"       # Gold
CORRECT = "#22C55E"      # Green
WRONG = "#EF4444"        # Red
CYAN = "#00FFFF"
YELLOW = "#FCD34D"
ORANGE = "#FF6B35"

# ============================================
# TYPOGRAPHY
# ============================================
FONT_PRIMARY = "Arial"
FONT_HINDI = "Noto Sans Devanagari"

FONT_SIZE_TITLE = 48
FONT_SIZE_HEADER = 42
FONT_SIZE_BODY = 32
FONT_SIZE_SMALL = 24
FONT_SIZE_TINY = 18

# ============================================
# WATERMARK & BRANDING
# ============================================
def create_brand_watermark(opacity: float = 0.6) -> VGroup:
    """Create JeetLo watermark for bottom right corner."""
    watermark = VGroup()

    # Flame icon (simplified)
    flame = VGroup()
    # Outer flame
    outer = Polygon(
        [0, 0.4, 0], [-0.15, 0, 0], [0, -0.3, 0], [0.15, 0, 0],
        color="#FF6B35", fill_opacity=0.9, stroke_width=0
    )
    # Inner flame
    inner = Polygon(
        [0, 0.25, 0], [-0.08, 0.05, 0], [0, -0.15, 0], [0.08, 0.05, 0],
        color="#FFD93D", fill_opacity=0.9, stroke_width=0
    )
    flame.add(outer, inner)
    flame.scale(0.5)

    # Text
    jeet = Text("Jeet", font_size=24, color=WHITE, weight=BOLD)
    lo = Text("Lo", font_size=24, color="#FFD93D", weight=BOLD)
    lo.next_to(jeet, RIGHT, buff=0.02)

    text_group = VGroup(jeet, lo)
    flame.next_to(text_group, LEFT, buff=0.1)

    watermark.add(flame, text_group)
    watermark.set_opacity(opacity)
    watermark.to_corner(DR, buff=0.3)

    return watermark


def create_flame_logo(scale: float = 1.0) -> VGroup:
    """Create the JeetLo flame logo."""
    flame = VGroup()

    # Outer flame (orange)
    outer = Polygon(
        [0, 0.8, 0], [-0.3, 0, 0], [0, -0.5, 0], [0.3, 0, 0],
        color="#FF6B35", fill_opacity=0.9, stroke_width=0
    )

    # Middle flame (yellow)
    middle = Polygon(
        [0, 0.5, 0], [-0.18, 0.05, 0], [0, -0.3, 0], [0.18, 0.05, 0],
        color="#FFD93D", fill_opacity=0.9, stroke_width=0
    )

    # Inner glow (white)
    inner = Ellipse(width=0.15, height=0.2, color=WHITE, fill_opacity=0.8, stroke_width=0)
    inner.move_to([0, -0.15, 0])

    flame.add(outer, middle, inner)
    flame.scale(scale)

    return flame


# ============================================
# JEETLO REEL MIXIN
# ============================================
class JeetLoReelMixin:
    """Mixin class providing common JeetLo reel functionality."""

    subject = "physics"  # Override in subclass

    def set_subject_background(self, subject: str):
        """Set the background color for the subject."""
        bg_color = SUBJECT_BACKGROUNDS.get(subject, BG_COLOR)
        self.camera.background_color = bg_color

    def get_subject_color(self) -> str:
        """Get the primary color for current subject."""
        return SUBJECT_COLORS.get(self.subject, SUBJECT_COLORS["physics"])

    def load_timings(self) -> list:
        """Load audio timings from timings.json."""
        try:
            timings_path = os.path.join(os.path.dirname(self.__module__), 'audio', 'timings.json')
            with open(timings_path, 'r') as f:
                return json.load(f)
        except:
            return [{'duration': 6.0}] * 10

    def add_cta_slide_physics(self, duration: float = 8.0):
        """Add physics CTA slide."""
        self._add_cta_slide("Physics", "#0066FF", duration)

    def add_cta_slide_chemistry(self, duration: float = 8.0):
        """Add chemistry CTA slide."""
        self._add_cta_slide("Chemistry", "#00CC66", duration)

    def add_cta_slide_biology(self, duration: float = 8.0):
        """Add biology CTA slide."""
        self._add_cta_slide("Biology", "#CC66FF", duration)

    def add_cta_slide_mathematics(self, duration: float = 8.0):
        """Add mathematics CTA slide."""
        self._add_cta_slide("Mathematics", "#FF9900", duration)

    def _add_cta_slide(self, subject_name: str, color: str, duration: float):
        """Generic CTA slide."""
        # Flame logo
        flame = create_flame_logo(scale=1.5)
        flame.move_to(UP * 3)

        # JeetLo + Subject
        jeet = Text("Jeet", font_size=56, color=WHITE, weight=BOLD)
        lo = Text("Lo", font_size=56, color=YELLOW, weight=BOLD)
        lo.next_to(jeet, RIGHT, buff=0.05)
        subject = Text(subject_name + "!", font_size=56, color=color, weight=BOLD)
        subject.next_to(lo, RIGHT, buff=0.1)

        title = VGroup(jeet, lo, subject)
        title.move_to(UP * 0.5)

        # Follow
        follow = Text("Follow for more!", font_size=36, color=YELLOW, weight=BOLD)
        follow.move_to(DOWN * 1)

        # Website
        website = Text("jeetlo.ai", font_size=42, color=CYAN, weight=BOLD)
        website.move_to(DOWN * 2.5)

        # Register
        register = Text("Register for Early Access!", font_size=28, color=WHITE)
        register.move_to(DOWN * 3.5)

        # Price
        price = Text("All courses for just ₹499/month", font_size=24, color=SECONDARY)
        price.move_to(DOWN * 4.5)

        # Animation
        self.play(FadeIn(flame, scale=0.5), run_time=0.5)
        self.play(Write(title), run_time=0.6)
        self.play(Write(follow), run_time=0.4)
        self.play(Write(website), run_time=0.4)
        self.play(FadeIn(register), run_time=0.3)
        self.play(FadeIn(price), run_time=0.3)
        self.wait(duration - 2.5)

        self.play(FadeOut(VGroup(flame, title, follow, website, register, price)), run_time=0.4)


# ============================================
# EXPORTS
# ============================================
__all__ = [
    # Colors
    "BG_COLOR", "SUBJECT_COLORS", "SUBJECT_BACKGROUNDS",
    "PRIMARY", "SECONDARY", "ACCENT", "CORRECT", "WRONG", "CYAN", "YELLOW", "ORANGE",
    # Typography
    "FONT_PRIMARY", "FONT_HINDI",
    "FONT_SIZE_TITLE", "FONT_SIZE_HEADER", "FONT_SIZE_BODY", "FONT_SIZE_SMALL", "FONT_SIZE_TINY",
    # Frame
    "FRAME_WIDTH", "FRAME_HEIGHT", "PIXEL_WIDTH", "PIXEL_HEIGHT",
    # Functions
    "create_brand_watermark", "create_flame_logo",
    # Classes
    "JeetLoReelMixin",
]
