"""
JeetLo Physics Reel: Gravity - The Universe's Obsessive Stalker
================================================================
VIRAL CONCEPT: Everything pulls on everything! Gravity is pathetically weak
but relentless - that's why it shapes galaxies despite being beaten by a magnet.

Animation Focus:
- Person falling with cosmic forces pulling from everywhere
- Newton's apple + Moon connection
- Gravity formula with G constant revelation
- Inverse square law as flashlight analogy
- Everything pulls everything reveal
- Weak but relentless key point
- JEE trap: mass and radius doubled
"""

import sys
import json
import numpy as np
sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')

from manim import *
from jeetlo_style import *

# Import manim-edu physics components
try:
    from manim_edu.physics import WaveSimulator, FieldVisualizer, MechanicsSimulator
    from manim_edu.primitives.colors import SUBJECT_COLORS
except ImportError:
    pass

# Additional colors for this reel
GOLD = "#FFD700"
ORANGE = "#FF9800"
LIGHT_BLUE = "#87CEEB"
TEAL = "#008080"
PURPLE = "#9B59B6"
PINK = "#FF69B4"


def load_timings():
    """Load audio timings from JSON file."""
    with open('audio/timings.json', 'r') as f:
        return {t['id']: t for t in json.load(f)}


class PhysicsReel(JeetLoReelMixin, Scene):
    """Physics reel explaining gravity as the universe's obsessive stalker."""
    subject = "physics"

    def construct(self):
        # Set physics background (dark blue)
        self.camera.background_color = '#0A1A3F'

        # Load timings
        self.timings = load_timings()

        # Add watermark
        self.watermark = create_brand_watermark(opacity=0.5, scale=1.0)
        self.add(self.watermark)

        # Run all segments
        self.segment_01_hook(self.timings['01_hook'])
        self.segment_02_setup(self.timings['02_setup'])
        self.segment_03_content_part1(self.timings['03_content_part1'])
        self.segment_03_content_part2(self.timings['03_content_part2'])
        self.segment_04_reveal(self.timings['04_reveal'])
        self.segment_05_key_point(self.timings['05_key_point'])
        self.segment_06_exam_tip(self.timings['06_exam_tip'])
        self.segment_07_cta(self.timings['07_cta'])

    def segment_01_hook(self, timing):
        """Hook: You're FALLING right now! Creates cognitive dissonance (6.36s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.3 + 0.4 + 0.3 + 0.3 + 0.3  # 2.0s
        num_waits = 3
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Person sitting on chair (simplified stick figure)
        person_group = VGroup()

        # Chair
        chair_seat = Line(LEFT * 0.4, RIGHT * 0.4, color=WHITE, stroke_width=3)
        chair_back = Line(LEFT * 0.4 + UP * 0.5, LEFT * 0.4, color=WHITE, stroke_width=3)
        chair_legs = VGroup(
            Line(LEFT * 0.3, LEFT * 0.3 + DOWN * 0.4, color=WHITE, stroke_width=2),
            Line(RIGHT * 0.3, RIGHT * 0.3 + DOWN * 0.4, color=WHITE, stroke_width=2),
        )
        chair = VGroup(chair_seat, chair_back, chair_legs)

        # Stick figure
        head = Circle(radius=0.2, color=YELLOW, fill_opacity=0.8, stroke_width=2)
        head.move_to(UP * 0.9)
        body = Line(UP * 0.7, UP * 0.1, color=WHITE, stroke_width=3)
        legs = VGroup(
            Line(UP * 0.1, RIGHT * 0.3 + DOWN * 0.1, color=WHITE, stroke_width=2),
            Line(UP * 0.1, LEFT * 0.3 + DOWN * 0.1, color=WHITE, stroke_width=2),
        )
        arms = VGroup(
            Line(UP * 0.5, RIGHT * 0.4 + UP * 0.3, color=WHITE, stroke_width=2),
            Line(UP * 0.5, LEFT * 0.4 + UP * 0.3, color=WHITE, stroke_width=2),
        )
        person = VGroup(head, body, legs, arms)

        person_group.add(chair, person)
        person_group.move_to(UP * 2)
        person_group.scale(0.8)

        # Earth below (big, showing you're on it)
        earth = Circle(radius=2.5, color=BLUE, fill_opacity=0.3, stroke_width=3)
        earth.move_to(DOWN * 4.5)
        earth_label = Text("EARTH", font_size=24, color=BLUE, weight=BOLD)
        earth_label.move_to(earth.get_center())

        # Gravity arrow from Earth to person (BIG)
        earth_arrow = Arrow(
            DOWN * 2, person_group.get_center() + DOWN * 0.5,
            color=RED, stroke_width=6, buff=0.1
        )

        # Moon and Sun pulling too (smaller arrows)
        moon = Circle(radius=0.4, color=GRAY, fill_opacity=0.6, stroke_width=2)
        moon.move_to(RIGHT * 3.5 + UP * 3)
        moon_label = Text("Moon", font_size=16, color=GRAY)
        moon_label.next_to(moon, UP, buff=0.1)

        sun = Circle(radius=0.6, color=ORANGE, fill_opacity=0.8, stroke_width=2)
        sun.move_to(LEFT * 3.5 + UP * 4)
        sun_label = Text("Sun", font_size=16, color=ORANGE)
        sun_label.next_to(sun, UP, buff=0.1)

        moon_arrow = Arrow(
            moon.get_center(), person_group.get_center() + RIGHT * 0.3,
            color=GRAY, stroke_width=2, buff=0.2
        )
        sun_arrow = Arrow(
            sun.get_center(), person_group.get_center() + LEFT * 0.3,
            color=ORANGE, stroke_width=3, buff=0.2
        )

        # "You're FALLING" text
        falling_text = Text("You're FALLING right now!", font_size=40, color=RED, weight=BOLD)
        falling_text.move_to(DOWN * 1)

        # Animation
        self.play(FadeIn(person_group, scale=0.8), run_time=0.4)
        self.wait(wait_time)

        self.play(FadeIn(earth, earth_label), run_time=0.3)
        self.play(FadeIn(moon, moon_label, sun, sun_label), run_time=0.4)
        self.wait(wait_time)

        self.play(Create(earth_arrow), run_time=0.3)
        self.play(Create(moon_arrow), Create(sun_arrow), run_time=0.3)
        self.play(Write(falling_text), run_time=0.3)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_02_setup(self, timing):
        """Setup: Newton's genius - apple and Moon are same force (11.064s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.4 + 0.5 + 0.4 + 0.4 + 0.5 + 0.4 + 0.3  # 3.3s
        num_waits = 4
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Split screen divider
        divider = DashedLine(UP * 6, DOWN * 6, color=WHITE, stroke_width=1, dash_length=0.2)

        # Left side: Apple falling
        left_title = Text("Apple Falling", font_size=28, color=GREEN, weight=BOLD)
        left_title.move_to(LEFT * 2 + UP * 5)

        # Tree
        trunk = Rectangle(width=0.3, height=1.5, color='#8B4513', fill_opacity=0.8, stroke_width=0)
        trunk.move_to(LEFT * 2 + UP * 1)
        leaves = Circle(radius=1, color=GREEN, fill_opacity=0.6, stroke_width=0)
        leaves.move_to(LEFT * 2 + UP * 2.5)
        tree = VGroup(trunk, leaves)

        apple = Circle(radius=0.15, color=RED, fill_opacity=1, stroke_width=0)
        apple.move_to(LEFT * 2.3 + UP * 1.8)

        apple_path = DashedLine(
            apple.get_center(), LEFT * 2.3 + DOWN * 0.5,
            color=RED, stroke_width=2, dash_length=0.1
        )
        ground_left = Line(LEFT * 3.5 + DOWN * 0.7, LEFT * 0.5 + DOWN * 0.7, color=WHITE, stroke_width=2)

        # Right side: Moon orbiting Earth
        right_title = Text("Moon Orbiting", font_size=28, color=TEAL, weight=BOLD)
        right_title.move_to(RIGHT * 2 + UP * 5)

        earth_small = Circle(radius=0.5, color=BLUE, fill_opacity=0.6, stroke_width=2)
        earth_small.move_to(RIGHT * 2 + UP * 1)
        earth_label = Text("Earth", font_size=16, color=BLUE)
        earth_label.next_to(earth_small, DOWN, buff=0.2)

        orbit = Circle(radius=1.8, color=GRAY, stroke_width=1, stroke_opacity=0.5)
        orbit.move_to(earth_small.get_center())

        moon_small = Circle(radius=0.2, color=GRAY, fill_opacity=0.8, stroke_width=1)
        moon_small.move_to(RIGHT * 2 + UP * 2.8)

        orbit_arrow = Arrow(
            RIGHT * 3.8 + UP * 1, RIGHT * 3.5 + UP * 1.5,
            color=TEAL, stroke_width=2, buff=0
        )

        # Connection line with question
        connection = DashedLine(
            LEFT * 0.3 + UP * 1, RIGHT * 0.3 + UP * 1,
            color=YELLOW, stroke_width=3, dash_length=0.15
        )
        same_force = Text("SAME FORCE?", font_size=36, color=YELLOW, weight=BOLD)
        same_force.move_to(DOWN * 2)

        # Newton silhouette
        newton = VGroup()
        newton_head = Circle(radius=0.25, color=WHITE, fill_opacity=0.3, stroke_width=2)
        newton_body = Rectangle(width=0.5, height=0.8, color=WHITE, fill_opacity=0.2, stroke_width=2)
        newton_body.next_to(newton_head, DOWN, buff=0)
        newton.add(newton_head, newton_body)
        newton.move_to(DOWN * 4.5)
        think_bubble = Text("?", font_size=48, color=WHITE, weight=BOLD)
        think_bubble.next_to(newton, UP + RIGHT, buff=0.2)

        # Animation
        self.play(Create(divider), run_time=0.4)

        # Left side
        self.play(Write(left_title), FadeIn(tree, ground_left), run_time=0.4)
        self.play(FadeIn(apple), run_time=0.5)
        self.play(
            apple.animate.move_to(LEFT * 2.3 + DOWN * 0.5),
            Create(apple_path),
            run_time=0.4
        )
        self.wait(wait_time)

        # Right side
        self.play(Write(right_title), FadeIn(earth_small, earth_label, orbit), run_time=0.4)
        self.play(FadeIn(moon_small), Create(orbit_arrow), run_time=0.5)
        self.wait(wait_time)

        # Connection
        self.play(Create(connection), run_time=0.4)
        self.play(Write(same_force), run_time=0.3)
        self.wait(wait_time)

        # Newton
        self.play(FadeIn(newton, think_bubble), run_time=0.4)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_03_content_part1(self, timing):
        """Content Part 1: The gravity formula - G is TINY! (14.4s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.5 + 0.3 + 0.3 + 0.3 + 0.4 + 0.5 + 0.4 + 0.3  # 3.4s
        num_waits = 5
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Title
        title = Text("Gravity Formula", font_size=36, color=YELLOW, weight=BOLD)
        title.move_to(UP * 5.5)

        # Create gravitational field using manim-edu
        field_viz = FieldVisualizer(scale=0.5)
        grav_field = field_viz.gravitational_field()
        grav_field.move_to(UP * 2.5)
        grav_field.scale(0.8)

        # Formula: F = G(M1 × M2) / r²
        f_text = Text("F", font_size=56, color=RED, weight=BOLD)
        equals = Text("=", font_size=48, color=WHITE, weight=BOLD)
        g_text = Text("G", font_size=56, color=GREEN, weight=BOLD)

        # Masses
        m1_text = Text("M", font_size=48, color=ORANGE, weight=BOLD)
        m1_sub = Text("1", font_size=28, color=ORANGE)
        m1_sub.next_to(m1_text, DOWN + RIGHT, buff=-0.1).shift(UP * 0.15)
        m1_group = VGroup(m1_text, m1_sub)

        times_sym = Text("x", font_size=40, color=WHITE)

        m2_text = Text("M", font_size=48, color=TEAL, weight=BOLD)
        m2_sub = Text("2", font_size=28, color=TEAL)
        m2_sub.next_to(m2_text, DOWN + RIGHT, buff=-0.1).shift(UP * 0.15)
        m2_group = VGroup(m2_text, m2_sub)

        # Fraction line and r²
        frac_line = Line(LEFT * 1.5, RIGHT * 1.5, color=WHITE, stroke_width=3)

        r_text = Text("r", font_size=48, color=PURPLE, weight=BOLD)
        r_sq = Text("2", font_size=28, color=PURPLE)
        r_sq.next_to(r_text, UP + RIGHT, buff=-0.1).shift(DOWN * 0.15)
        r_group = VGroup(r_text, r_sq)

        # Arrange formula
        f_text.move_to(LEFT * 2.5 + DOWN * 1)
        equals.next_to(f_text, RIGHT, buff=0.3)

        numerator = VGroup(g_text, m1_group, times_sym, m2_group)
        g_text.move_to(ORIGIN)
        m1_group.next_to(g_text, RIGHT, buff=0.15)
        times_sym.next_to(m1_group, RIGHT, buff=0.1)
        m2_group.next_to(times_sym, RIGHT, buff=0.1)
        numerator.move_to(RIGHT * 0.5 + DOWN * 0.5)

        frac_line.next_to(numerator, DOWN, buff=0.15)
        r_group.next_to(frac_line, DOWN, buff=0.15)

        formula = VGroup(f_text, equals, numerator, frac_line, r_group)
        formula.move_to(DOWN * 1.5)

        # G value callout
        g_value = Text("G = 6.67 x 10", font_size=28, color=GREEN)
        g_exp = Text("-11", font_size=18, color=GREEN)
        g_exp.next_to(g_value, UP + RIGHT, buff=-0.05).shift(DOWN * 0.1)
        g_val_group = VGroup(g_value, g_exp)
        g_val_group.move_to(DOWN * 4)

        g_comment = Text("Universe's WEAKEST force!", font_size=24, color=YELLOW, weight=BOLD)
        g_comment.next_to(g_val_group, DOWN, buff=0.3)

        # Animation
        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(grav_field, scale=0.8), run_time=0.5)
        self.wait(wait_time)

        # Build formula piece by piece
        self.play(Write(f_text), Write(equals), run_time=0.3)
        self.wait(wait_time)

        self.play(Write(g_text), run_time=0.3)
        self.play(Write(m1_group), Write(times_sym), Write(m2_group), run_time=0.3)
        self.wait(wait_time)

        self.play(Create(frac_line), Write(r_group), run_time=0.4)
        self.wait(wait_time)

        # G value reveal
        self.play(Write(g_val_group), run_time=0.5)
        self.play(Write(g_comment), run_time=0.4)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_03_content_part2(self, timing):
        """Content Part 2: Inverse square law - like flashlight spreading (15.864s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.5 + 0.3 + 0.3 + 0.3 + 0.3 + 0.4 + 0.4 + 0.3 + 0.3  # 3.5s
        num_waits = 6
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Title
        title = Text("Inverse Square Law", font_size=40, color=YELLOW, weight=BOLD)
        title.move_to(UP * 5.5)

        # Flashlight visual
        flashlight = VGroup()
        fl_body = Rectangle(width=0.4, height=0.8, color=YELLOW, fill_opacity=0.8, stroke_width=2)
        fl_body.move_to(LEFT * 3 + UP * 2)
        fl_head = Polygon(
            fl_body.get_right() + UP * 0.3,
            fl_body.get_right() + DOWN * 0.3,
            fl_body.get_right() + RIGHT * 0.3,
            color=YELLOW, fill_opacity=0.9, stroke_width=0
        )
        flashlight.add(fl_body, fl_head)

        # Light spreading cone
        light_cone = Polygon(
            fl_head.get_right(),
            fl_head.get_right() + RIGHT * 3 + UP * 1.5,
            fl_head.get_right() + RIGHT * 3 + DOWN * 1.5,
            color=YELLOW, fill_opacity=0.15, stroke_width=0
        )

        # Distance markers
        d1_line = Line(LEFT * 2.5 + UP * 2, LEFT * 1.5 + UP * 2, color=WHITE, stroke_width=2)
        d1_label = Text("1x", font_size=24, color=WHITE)
        d1_label.next_to(d1_line, DOWN, buff=0.1)

        d2_line = Line(LEFT * 2.5 + UP * 2, LEFT * 0.5 + UP * 2, color=TEAL, stroke_width=2)
        d2_label = Text("2x", font_size=24, color=TEAL)
        d2_label.next_to(d2_line, DOWN, buff=0.1)

        d3_line = Line(LEFT * 2.5 + UP * 2, RIGHT * 0.5 + UP * 2, color=PURPLE, stroke_width=2)
        d3_label = Text("3x", font_size=24, color=PURPLE)
        d3_label.next_to(d3_line, DOWN, buff=0.1)

        # Force arrows (thickness = strength)
        force1 = Arrow(LEFT * 1.5 + DOWN * 0.5, LEFT * 0.5 + DOWN * 0.5,
                       color=RED, stroke_width=8, buff=0)
        f1_label = Text("F", font_size=28, color=RED, weight=BOLD)
        f1_label.next_to(force1, DOWN, buff=0.1)

        force2 = Arrow(LEFT * 1.5 + DOWN * 1.5, LEFT * 0.9 + DOWN * 1.5,
                       color=TEAL, stroke_width=3, buff=0)
        f2_label = Text("F/4", font_size=24, color=TEAL, weight=BOLD)
        f2_label.next_to(force2, DOWN, buff=0.1)

        force3 = Arrow(LEFT * 1.5 + DOWN * 2.5, LEFT * 1.1 + DOWN * 2.5,
                       color=PURPLE, stroke_width=2, buff=0)
        f3_label = Text("F/9", font_size=20, color=PURPLE, weight=BOLD)
        f3_label.next_to(force3, DOWN, buff=0.1)

        # Key insight boxes
        box1 = VGroup()
        bg1 = RoundedRectangle(width=3, height=1, corner_radius=0.1,
                               color=TEAL, fill_opacity=0.2, stroke_width=2)
        txt1 = Text("2x distance", font_size=22, color=TEAL)
        txt1b = Text("= 1/4 force", font_size=22, color=WHITE, weight=BOLD)
        box1_content = VGroup(txt1, txt1b).arrange(DOWN, buff=0.1)
        box1.add(bg1, box1_content)
        box1.move_to(RIGHT * 2 + UP * 2)

        box2 = VGroup()
        bg2 = RoundedRectangle(width=3, height=1, corner_radius=0.1,
                               color=PURPLE, fill_opacity=0.2, stroke_width=2)
        txt2 = Text("3x distance", font_size=22, color=PURPLE)
        txt2b = Text("= 1/9 force", font_size=22, color=WHITE, weight=BOLD)
        box2_content = VGroup(txt2, txt2b).arrange(DOWN, buff=0.1)
        box2.add(bg2, box2_content)
        box2.move_to(RIGHT * 2 + DOWN * 0.5)

        # Explanation
        explain = Text("Like flashlight spreading!", font_size=28, color=YELLOW, weight=BOLD)
        explain.move_to(DOWN * 4.5)

        r_squared = Text("r SQUARED in denominator!", font_size=26, color=RED, weight=BOLD)
        r_squared.move_to(DOWN * 5.5)

        # Animation
        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(flashlight), Create(light_cone), run_time=0.5)
        self.wait(wait_time)

        # Distance markers
        self.play(Create(d1_line), Write(d1_label), run_time=0.3)
        self.play(Create(force1), Write(f1_label), run_time=0.3)
        self.wait(wait_time)

        self.play(Create(d2_line), Write(d2_label), run_time=0.3)
        self.play(Create(force2), Write(f2_label), run_time=0.3)
        self.play(FadeIn(box1), run_time=0.4)
        self.wait(wait_time)

        self.play(Create(d3_line), Write(d3_label), run_time=0.3)
        self.play(Create(force3), Write(f3_label), run_time=0.3)
        self.play(FadeIn(box2), run_time=0.4)
        self.wait(wait_time)

        self.play(Write(explain), run_time=0.3)
        self.play(Write(r_squared), run_time=0.3)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_04_reveal(self, timing):
        """Reveal: EVERYTHING pulls EVERYTHING - mind blow moment (13.848s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.4 + 0.3 + 0.3 + 0.3 + 0.3 + 0.4 + 0.5 + 0.4 + 0.3  # 3.6s
        num_waits = 5
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Title
        title = Text("Mind Blowing Fact!", font_size=40, color=RED, weight=BOLD)
        title.move_to(UP * 5.5)

        # Phone/hand visual (you holding phone)
        phone = RoundedRectangle(width=1, height=1.8, corner_radius=0.1,
                                 color=GRAY, fill_opacity=0.8, stroke_width=2)
        phone.move_to(ORIGIN)
        screen = RoundedRectangle(width=0.85, height=1.5, corner_radius=0.05,
                                  color=BLUE, fill_opacity=0.3, stroke_width=0)
        screen.move_to(phone.get_center() + UP * 0.1)
        phone_group = VGroup(phone, screen)
        phone_group.scale(0.8)

        # Earth (BIG arrow from below)
        earth = Circle(radius=0.8, color=BLUE, fill_opacity=0.5, stroke_width=2)
        earth.move_to(DOWN * 4.5)
        earth_label = Text("Earth", font_size=18, color=BLUE)
        earth_label.next_to(earth, DOWN, buff=0.1)
        earth_arrow = Arrow(
            DOWN * 3.5, phone.get_center() + DOWN * 0.5,
            color=BLUE, stroke_width=8, buff=0.1
        )

        # Moon (small arrow from right)
        moon = Circle(radius=0.3, color=GRAY, fill_opacity=0.7, stroke_width=1)
        moon.move_to(RIGHT * 3.5 + UP * 4)
        moon_label = Text("Moon", font_size=14, color=GRAY)
        moon_label.next_to(moon, RIGHT, buff=0.1)
        moon_arrow = Arrow(
            RIGHT * 3 + UP * 3.5, phone.get_center() + RIGHT * 0.3 + UP * 0.3,
            color=GRAY, stroke_width=2, buff=0.1
        )

        # Sun (medium arrow from left)
        sun = Circle(radius=0.5, color=ORANGE, fill_opacity=0.8, stroke_width=2)
        sun.move_to(LEFT * 3.5 + UP * 4.5)
        sun_label = Text("Sun", font_size=14, color=ORANGE)
        sun_label.next_to(sun, LEFT, buff=0.1)
        sun_arrow = Arrow(
            LEFT * 3 + UP * 4, phone.get_center() + LEFT * 0.3 + UP * 0.3,
            color=ORANGE, stroke_width=4, buff=0.1
        )

        # Person next to you (tiny arrow)
        person_icon = VGroup()
        p_head = Circle(radius=0.15, color=YELLOW, fill_opacity=0.7, stroke_width=1)
        p_body = Line(ORIGIN, DOWN * 0.3, color=YELLOW, stroke_width=2)
        p_body.next_to(p_head, DOWN, buff=0)
        person_icon.add(p_head, p_body)
        person_icon.move_to(LEFT * 3 + DOWN * 1)
        person_label = Text("Person", font_size=12, color=YELLOW)
        person_label.next_to(person_icon, LEFT, buff=0.1)
        person_arrow = Arrow(
            LEFT * 2.8 + DOWN * 1, phone.get_center() + LEFT * 0.5,
            color=YELLOW, stroke_width=1, buff=0.1
        )

        # More micro arrows from random directions
        micro_arrows = VGroup()
        for angle in [PI/6, PI/3, 2*PI/3, 5*PI/6, -PI/6, -PI/3]:
            pos = np.array([np.cos(angle) * 2.5, np.sin(angle) * 2, 0])
            micro_arrow = Arrow(
                pos, phone.get_center() + np.array([np.cos(angle) * 0.3, np.sin(angle) * 0.2, 0]),
                color=WHITE, stroke_width=0.5, stroke_opacity=0.5, buff=0.1
            )
            micro_arrows.add(micro_arrow)

        # Revelation text
        reveal_text = Text("EVERYTHING pulls EVERYTHING!", font_size=34, color=YELLOW, weight=BOLD)
        reveal_text.move_to(DOWN * 2.5)

        always_text = Text("Always. Forever.", font_size=28, color=WHITE)
        always_text.next_to(reveal_text, DOWN, buff=0.3)

        # Animation
        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(phone_group), run_time=0.4)
        self.wait(wait_time)

        # Earth
        self.play(FadeIn(earth, earth_label), run_time=0.3)
        self.play(Create(earth_arrow), run_time=0.3)
        self.wait(wait_time)

        # Moon and Sun
        self.play(FadeIn(moon, moon_label, sun, sun_label), run_time=0.3)
        self.play(Create(moon_arrow), Create(sun_arrow), run_time=0.3)
        self.wait(wait_time)

        # Person
        self.play(FadeIn(person_icon, person_label), Create(person_arrow), run_time=0.4)

        # Micro arrows
        self.play(LaggedStart(*[Create(a) for a in micro_arrows], lag_ratio=0.05), run_time=0.5)
        self.wait(wait_time)

        # Revelation
        self.play(Write(reveal_text), run_time=0.4)
        self.play(Write(always_text), run_time=0.3)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_05_key_point(self, timing):
        """Key Point: Gravity is weak but RELENTLESS (14.304s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.4 + 0.3 + 0.5 + 0.3 + 0.4 + 0.4 + 0.5 + 0.3  # 3.5s
        num_waits = 6
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Title
        title = Text("Gravity's Secret Power", font_size=38, color=YELLOW, weight=BOLD)
        title.move_to(UP * 5.5)

        # Arm wrestling visual - EM vs Gravity
        # EM Force (HUGE)
        em_body = RoundedRectangle(width=1.2, height=2, corner_radius=0.1,
                                   color=BLUE, fill_opacity=0.8, stroke_width=2)
        em_body.move_to(LEFT * 2.5 + UP * 1.5)
        em_arm = Line(em_body.get_right() + UP * 0.5, em_body.get_right() + RIGHT * 1 + UP * 0.5,
                     color=BLUE, stroke_width=8)
        em_label = Text("EM Force", font_size=20, color=BLUE, weight=BOLD)
        em_label.next_to(em_body, DOWN, buff=0.2)
        em_size = Text("HUGE!", font_size=16, color=WHITE)
        em_size.move_to(em_body.get_center())
        em_wrestler = VGroup(em_body, em_arm, em_label, em_size)

        # Gravity (tiny)
        grav_body = RoundedRectangle(width=0.4, height=0.6, corner_radius=0.05,
                                     color=ORANGE, fill_opacity=0.8, stroke_width=1)
        grav_body.move_to(RIGHT * 2.5 + UP * 1.8)
        grav_arm = Line(grav_body.get_left() + UP * 0.1, grav_body.get_left() + LEFT * 0.5 + UP * 0.1,
                       color=ORANGE, stroke_width=2)
        grav_label = Text("Gravity", font_size=16, color=ORANGE, weight=BOLD)
        grav_label.next_to(grav_body, DOWN, buff=0.1)
        grav_size = Text("tiny", font_size=12, color=WHITE)
        grav_size.move_to(grav_body.get_center())
        grav_wrestler = VGroup(grav_body, grav_arm, grav_label, grav_size)

        vs_text = Text("VS", font_size=36, color=RED, weight=BOLD)
        vs_text.move_to(UP * 1.5)

        # Magnet example
        mag_body = Rectangle(width=1.2, height=0.4, color=RED, fill_opacity=0.8, stroke_width=2)
        mag_body.set_color([RED, BLUE])
        mag_n = Text("N", font_size=16, color=WHITE, weight=BOLD)
        mag_n.move_to(mag_body.get_left() + RIGHT * 0.25)
        mag_s = Text("S", font_size=16, color=WHITE, weight=BOLD)
        mag_s.move_to(mag_body.get_right() + LEFT * 0.25)
        magnet = VGroup(mag_body, mag_n, mag_s)
        magnet.move_to(LEFT * 2 + DOWN * 1.5)
        magnet.scale(0.8)

        # Paperclip
        clip = Rectangle(width=0.15, height=0.3, color=GRAY, fill_opacity=0.8, stroke_width=1)
        clip.move_to(magnet.get_center() + DOWN * 0.5)

        # Earth
        earth_mini = Circle(radius=0.6, color=BLUE, fill_opacity=0.3, stroke_width=2)
        earth_mini.move_to(LEFT * 2 + DOWN * 3.5)
        earth_lbl = Text("Earth's\nGravity", font_size=14, color=BLUE, line_spacing=0.8)
        earth_lbl.next_to(earth_mini, DOWN, buff=0.1)

        beat_text = Text("Magnet WINS!", font_size=20, color=RED, weight=BOLD)
        beat_text.move_to(LEFT * 2 + DOWN * 0.5)

        # Galaxy
        galaxy = VGroup()
        galaxy_core = Circle(radius=0.3, color=YELLOW, fill_opacity=0.6, stroke_width=0)
        galaxy_arm1 = Arc(radius=1, start_angle=0, angle=PI, color=WHITE, stroke_width=2, stroke_opacity=0.5)
        galaxy_arm2 = Arc(radius=1, start_angle=PI, angle=PI, color=WHITE, stroke_width=2, stroke_opacity=0.5)
        galaxy.add(galaxy_core, galaxy_arm1, galaxy_arm2)
        galaxy.move_to(RIGHT * 2 + DOWN * 2)
        galaxy_label = Text("Galaxies form\nby GRAVITY!", font_size=18, color=YELLOW, weight=BOLD, line_spacing=0.8)
        galaxy_label.next_to(galaxy, DOWN, buff=0.2)

        # Key insight
        insight_box = RoundedRectangle(width=6.5, height=1.5, corner_radius=0.15,
                                       color=ORANGE, fill_opacity=0.2, stroke_width=2)
        insight_box.move_to(DOWN * 5)
        insight_text = Text("Weak but RELENTLESS = Shapes Universe!",
                           font_size=24, color=ORANGE, weight=BOLD)
        insight_text.move_to(insight_box.get_center())

        sub_insight = Text("Never repels - Always attracts - Never gives up",
                          font_size=18, color=WHITE)
        sub_insight.next_to(insight_box, UP, buff=0.2)

        # Animation
        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(em_wrestler), FadeIn(grav_wrestler), Write(vs_text), run_time=0.4)
        self.wait(wait_time)

        # Magnet example
        self.play(FadeIn(magnet, clip, earth_mini, earth_lbl), run_time=0.3)
        self.play(clip.animate.shift(UP * 0.3), run_time=0.5)
        self.play(Write(beat_text), run_time=0.3)
        self.wait(wait_time)

        # Galaxy
        self.play(FadeIn(galaxy, scale=0.5), run_time=0.4)
        self.play(Write(galaxy_label), run_time=0.4)
        self.wait(wait_time)

        # Insight
        self.play(FadeIn(insight_box), Write(sub_insight), run_time=0.5)
        self.play(Write(insight_text), run_time=0.3)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_06_exam_tip(self, timing):
        """Exam Tip: JEE trap - Earth mass and radius doubled (20.4s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.4 + 0.3 + 0.5 + 0.4 + 0.4 + 0.5 + 0.5 + 0.5 + 0.5 + 0.3  # 4.7s
        num_waits = 7
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Alert header
        alert = Text("JEE TRAP Alert!", font_size=44, color=RED, weight=BOLD)
        alert.move_to(UP * 5.5)

        # Warning icon
        warning = Text("!", font_size=36, color=RED, weight=BOLD)
        warning_bg = Circle(radius=0.4, color=RED, fill_opacity=0.2, stroke_width=3, stroke_color=RED)
        warning_group = VGroup(warning_bg, warning)
        warning_group.next_to(alert, LEFT, buff=0.3)

        # Problem statement
        problem = Text("If Earth's mass DOUBLES and radius DOUBLES...",
                      font_size=26, color=WHITE)
        problem.move_to(UP * 4)

        question = Text("What happens to g?", font_size=32, color=YELLOW, weight=BOLD)
        question.next_to(problem, DOWN, buff=0.3)

        # Formula box
        formula_bg = RoundedRectangle(width=5, height=1.5, corner_radius=0.15,
                                      color=BLUE, fill_opacity=0.2, stroke_width=2)
        formula_bg.move_to(UP * 1.5)

        # g = GM/R²
        g_text = Text("g", font_size=48, color=YELLOW, weight=BOLD)
        equals = Text("=", font_size=40, color=WHITE)
        gm_text = Text("GM", font_size=40, color=GREEN, weight=BOLD)
        frac_line = Line(LEFT * 0.8, RIGHT * 0.8, color=WHITE, stroke_width=3)
        r_text = Text("R", font_size=40, color=RED, weight=BOLD)
        r_sq = Text("2", font_size=24, color=RED)
        r_sq.next_to(r_text, UP + RIGHT, buff=-0.1).shift(DOWN * 0.1)
        r_group = VGroup(r_text, r_sq)

        g_text.move_to(formula_bg.get_center() + LEFT * 1.5)
        equals.next_to(g_text, RIGHT, buff=0.2)
        gm_text.move_to(formula_bg.get_center() + RIGHT * 0.8 + UP * 0.3)
        frac_line.next_to(gm_text, DOWN, buff=0.1)
        r_group.next_to(frac_line, DOWN, buff=0.1)

        formula = VGroup(g_text, equals, gm_text, frac_line, r_group)

        # Analysis arrows
        mass_arrow = Arrow(LEFT * 2.5 + DOWN * 0.8, LEFT * 0.5 + DOWN * 0.8,
                          color=GREEN, stroke_width=3, buff=0)
        mass_text = Text("M x 2", font_size=28, color=GREEN, weight=BOLD)
        mass_text.next_to(mass_arrow, UP, buff=0.1)
        mass_result = Text("Numerator x 2", font_size=22, color=GREEN)
        mass_result.next_to(mass_arrow, DOWN, buff=0.1)
        mass_analysis = VGroup(mass_arrow, mass_text, mass_result)

        r_arrow = Arrow(RIGHT * 0.5 + DOWN * 0.8, RIGHT * 2.5 + DOWN * 0.8,
                       color=RED, stroke_width=3, buff=0)
        r_text2 = Text("R x 2", font_size=28, color=RED, weight=BOLD)
        r_text2.next_to(r_arrow, UP, buff=0.1)
        r_sq_text = Text("R squared x 4!", font_size=24, color=RED, weight=BOLD)
        r_sq_text.next_to(r_arrow, DOWN, buff=0.1)
        r_analysis = VGroup(r_arrow, r_text2, r_sq_text)

        # Calculation
        calc_bg = RoundedRectangle(width=5.5, height=1.2, corner_radius=0.1,
                                   color=YELLOW, fill_opacity=0.15, stroke_width=2)
        calc_bg.move_to(DOWN * 2.5)

        calc_text = Text("g' = (2M)/(2R)squared = 2M/4Rsquared = M/2Rsquared",
                        font_size=20, color=WHITE)
        calc_text.move_to(calc_bg.get_center())

        # Answer
        answer_bg = RoundedRectangle(width=4, height=1.2, corner_radius=0.15,
                                     color=GREEN, fill_opacity=0.3, stroke_width=3)
        answer_bg.move_to(DOWN * 4.5)

        answer = Text("g becomes HALF!", font_size=32, color=GREEN, weight=BOLD)
        answer.move_to(answer_bg.get_center())

        # Key reminder
        reminder = Text("R SQUARED in denominator!", font_size=26, color=RED, weight=BOLD)
        reminder.move_to(DOWN * 6)

        circle_r = Circle(radius=0.7, color=RED, stroke_width=4, fill_opacity=0)
        circle_r.move_to(r_group.get_center())

        # Animation
        self.play(Write(alert), FadeIn(warning_group), run_time=0.4)
        self.play(Write(problem), run_time=0.4)
        self.play(Write(question), run_time=0.3)
        self.wait(wait_time)

        # Formula
        self.play(FadeIn(formula_bg), run_time=0.5)
        self.play(Write(formula), run_time=0.4)
        self.wait(wait_time)

        # Analysis
        self.play(FadeIn(mass_analysis), run_time=0.4)
        self.wait(wait_time)

        self.play(FadeIn(r_analysis), run_time=0.5)
        self.wait(wait_time)

        # Calculation
        self.play(FadeIn(calc_bg), Write(calc_text), run_time=0.5)
        self.wait(wait_time)

        # Answer
        self.play(FadeIn(answer_bg), Write(answer), run_time=0.5)
        self.wait(wait_time)

        # Highlight R²
        self.play(Create(circle_r), Write(reminder), run_time=0.3)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_07_cta(self, timing):
        """CTA: JeetLo Physics! - Use pre-built CTA slide (10.248s)"""
        duration = timing['duration']

        # Remove watermark for CTA slide
        self.remove(self.watermark)

        # Use the pre-built CTA from JeetLoReelMixin
        self.add_cta_slide_physics(duration)


# Manim config for 9:16 vertical video
config.pixel_width = PIXEL_WIDTH
config.pixel_height = PIXEL_HEIGHT
config.frame_width = FRAME_WIDTH
config.frame_height = FRAME_HEIGHT
config.background_color = '#0A1A3F'
