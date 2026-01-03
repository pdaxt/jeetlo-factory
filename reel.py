"""
JeetLo Physics Reel: Why Doesn't the Moon Fall? - Orbital Mechanics
====================================================================
VIRAL CONCEPT: Moon IS falling - every second! But it keeps missing Earth
because of its horizontal velocity. Orbit = Falling + Missing!

Animation Focus:
- Newton's Cannon thought experiment
- Projectile trajectories at different speeds
- Split screen: person falling vs Moon "falling but missing"
- Orbital velocity formula visualization
- JEE exam tip on satellite mass independence
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
    """Physics reel explaining why Moon doesn't fall - it IS falling but missing!"""
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
        """Hook: Moon is FALLING right now - shocking reveal (9.6s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.5 + 0.5 + 0.6 + 0.5 + 0.5 + 0.4 + 0.4 + 0.3  # 3.7s
        num_waits = 3
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Earth at center
        earth = Circle(radius=1.2, color='#0066FF', fill_opacity=0.8, stroke_width=3)
        earth.set_fill(color=['#0066FF', '#004499'])
        earth.move_to(DOWN * 1)

        earth_label = Text("EARTH", font_size=28, color=WHITE, weight=BOLD)
        earth_label.move_to(earth.get_center())

        # Moon above
        moon = Circle(radius=0.4, color='#CCCCCC', fill_opacity=0.9, stroke_width=2)
        moon.move_to(UP * 4)

        moon_label = Text("MOON", font_size=20, color='#333333', weight=BOLD)
        moon_label.move_to(moon.get_center())

        # Gravity arrow from Moon to Earth
        gravity_arrow = Arrow(
            moon.get_bottom() + DOWN * 0.1,
            earth.get_top() + UP * 0.3,
            color='#FF6B35',
            stroke_width=6,
            buff=0
        )

        # FALLING text
        falling_text = Text("FALLING... RIGHT NOW!", font_size=48, color='#FF4444', weight=BOLD)
        falling_text.move_to(UP * 6)

        # WRONG text for misconception
        wrong_text = Text("WRONG!", font_size=72, color='#FF4444', weight=BOLD)
        wrong_text.move_to(UP * 5)

        # Animation sequence
        self.play(FadeIn(earth), FadeIn(earth_label), run_time=0.5)
        self.play(FadeIn(moon, scale=1.3), FadeIn(moon_label), run_time=0.5)
        self.wait(wait_time)

        # Show "stable" misconception then WRONG
        stable_text = Text("STABLE?", font_size=40, color=YELLOW, weight=BOLD)
        stable_text.next_to(moon, RIGHT, buff=0.5)
        self.play(Write(stable_text), run_time=0.6)
        self.wait(wait_time * 0.5)

        self.play(
            FadeIn(wrong_text, scale=1.5),
            FadeOut(stable_text),
            run_time=0.5
        )

        # Show gravity arrow and falling text
        self.play(
            Create(gravity_arrow),
            moon.animate.shift(DOWN * 0.3),  # Wobble effect
            run_time=0.5
        )
        self.play(
            FadeIn(falling_text, shift=DOWN),
            moon.animate.shift(UP * 0.3),  # Wobble back
            run_time=0.4
        )
        self.wait(wait_time)

        # JEE Critical text
        jee_text = Text("J.E.E. CRITICAL!", font_size=36, color='#FFD700', weight=BOLD)
        jee_text.move_to(DOWN * 4.5)
        self.play(FadeIn(jee_text, scale=1.2), run_time=0.4)
        self.wait(wait_time * 0.5)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_02_setup(self, timing):
        """Newton's question: If apple falls, why not Moon? (9.648s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.3 + 0.4 + 0.5 + 0.5 + 0.4 + 0.5 + 0.3  # 3.3s
        num_waits = 4
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Newton silhouette (simple)
        newton_body = Ellipse(width=1.2, height=2.5, color=WHITE, fill_opacity=0.3, stroke_width=2)
        newton_body.move_to(LEFT * 2 + DOWN * 1)

        newton_head = Circle(radius=0.4, color=WHITE, fill_opacity=0.4, stroke_width=2)
        newton_head.next_to(newton_body, UP, buff=0.1)

        newton = VGroup(newton_body, newton_head)

        # Apple tree (simplified)
        trunk = Rectangle(width=0.4, height=2, color='#8B4513', fill_opacity=0.8)
        trunk.move_to(LEFT * 0.5 + DOWN * 2)

        leaves = Circle(radius=1.2, color='#228B22', fill_opacity=0.6)
        leaves.next_to(trunk, UP, buff=-0.3)

        tree = VGroup(trunk, leaves)

        # Apple
        apple = Circle(radius=0.2, color='#FF0000', fill_opacity=0.9)
        apple.move_to(LEFT * 0.3 + UP * 0.5)

        # Moon (small, in sky)
        moon = Circle(radius=0.5, color='#CCCCCC', fill_opacity=0.8)
        moon.move_to(RIGHT * 2 + UP * 4)

        # Thought bubble
        bubble = RoundedRectangle(width=4.5, height=1.8, corner_radius=0.3,
                                   color=WHITE, fill_opacity=0.1, stroke_width=2)
        bubble.move_to(RIGHT * 1 + UP * 1)

        question_text = Text("Apple falls...\nWhy not Moon?", font_size=28, color=YELLOW)
        question_text.move_to(bubble.get_center())

        # Question mark
        question_mark = Text("?", font_size=80, color='#FF6B35', weight=BOLD)
        question_mark.move_to(RIGHT * 3 + UP * 4)

        # Animation
        self.play(FadeIn(tree), FadeIn(newton), run_time=0.4)
        self.play(FadeIn(apple), run_time=0.3)

        # Apple falls
        self.play(apple.animate.move_to(LEFT * 0.3 + DOWN * 2.5), run_time=0.4)
        self.wait(wait_time)

        # Newton looks up
        self.play(FadeIn(moon), run_time=0.5)
        self.wait(wait_time)

        # Thought bubble with question
        self.play(FadeIn(bubble), Write(question_text), run_time=0.5)
        self.wait(wait_time)

        # Question mark appears dramatically
        self.play(FadeIn(question_mark, scale=2), run_time=0.4)
        self.wait(wait_time)

        # Gravity text
        gravity_label = Text("Same Gravity!", font_size=32, color='#0066FF', weight=BOLD)
        gravity_label.move_to(DOWN * 4)
        self.play(Write(gravity_label), run_time=0.5)
        self.wait(wait_time * 0.5)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_03_content_part1(self, timing):
        """Newton's cannon experiment - slow to fast (14.016s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.5 + 0.4 + 0.8 + 0.3 + 0.8 + 0.3 + 1.0 + 0.3  # 4.4s
        num_waits = 4
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Mountain
        mountain = Polygon(
            np.array([-3, -3, 0]),
            np.array([0, 2, 0]),
            np.array([3, -3, 0]),
            color='#654321', fill_opacity=0.7, stroke_width=2
        )

        # Cannon on top
        cannon_body = Rectangle(width=0.8, height=0.4, color='#333333', fill_opacity=0.9)
        cannon_body.move_to(np.array([-0.3, 2.2, 0]))
        cannon_body.rotate(-20 * DEGREES)

        cannon = VGroup(cannon_body)

        # Earth curve (bottom arc suggesting Earth's curvature)
        earth_arc = Arc(radius=8, start_angle=210 * DEGREES, angle=120 * DEGREES,
                        color='#0066FF', stroke_width=4)
        earth_arc.move_to(DOWN * 8)

        # Title
        title = Text("Newton's Cannon", font_size=36, color=WHITE, weight=BOLD)
        title.move_to(UP * 5.5)

        # Show scene
        self.play(FadeIn(mountain), FadeIn(cannon), FadeIn(earth_arc), run_time=0.5)
        self.play(Write(title), run_time=0.4)
        self.wait(wait_time)

        # Shot 1: Slow - falls quickly
        speed1_label = Text("SLOW", font_size=28, color='#FF4444')
        speed1_label.move_to(LEFT * 2 + UP * 3)

        ball1_path = Arc(radius=1.5, start_angle=70 * DEGREES, angle=-60 * DEGREES,
                         color='#FF6B35', stroke_width=4)
        ball1_path.move_to(np.array([0.5, 1, 0]))

        ball1 = Circle(radius=0.15, color='#FF6B35', fill_opacity=1)
        ball1.move_to(ball1_path.get_start())

        self.play(FadeIn(speed1_label), run_time=0.3)
        self.play(
            MoveAlongPath(ball1, ball1_path),
            Create(ball1_path),
            run_time=0.8
        )
        self.wait(wait_time)

        # Shot 2: Faster - goes further
        speed2_label = Text("FASTER", font_size=28, color=YELLOW)
        speed2_label.move_to(LEFT * 2 + UP * 2)

        ball2_path = Arc(radius=3, start_angle=70 * DEGREES, angle=-90 * DEGREES,
                         color=YELLOW, stroke_width=4)
        ball2_path.move_to(np.array([1.5, -0.5, 0]))

        ball2 = Circle(radius=0.15, color=YELLOW, fill_opacity=1)
        ball2.move_to(ball2_path.get_start())

        self.play(
            FadeIn(speed2_label),
            FadeOut(speed1_label),
            run_time=0.3
        )
        self.play(
            MoveAlongPath(ball2, ball2_path),
            Create(ball2_path),
            run_time=0.8
        )
        self.wait(wait_time)

        # Shot 3: Even faster - halfway around
        speed3_label = Text("EVEN FASTER!", font_size=28, color='#00FF00', weight=BOLD)
        speed3_label.move_to(LEFT * 2 + UP * 1)

        ball3_path = Arc(radius=5, start_angle=100 * DEGREES, angle=-140 * DEGREES,
                         color='#00FF00', stroke_width=4)
        ball3_path.move_to(np.array([0, -3, 0]))

        ball3 = Circle(radius=0.15, color='#00FF00', fill_opacity=1)
        ball3.move_to(ball3_path.get_start())

        self.play(
            FadeIn(speed3_label),
            FadeOut(speed2_label),
            run_time=0.3
        )
        self.play(
            MoveAlongPath(ball3, ball3_path),
            Create(ball3_path),
            run_time=1.0
        )
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_03_content_part2(self, timing):
        """Perfect speed = orbit! Ball becomes Moon (15.0s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.5 + 0.4 + 0.4 + 0.4 + 3.0 + 0.5 + 0.5 + 0.3  # 6.0s
        num_waits = 3
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Earth at center
        earth = Circle(radius=1.5, color='#0066FF', fill_opacity=0.8, stroke_width=3)
        earth.move_to(ORIGIN)

        earth_label = Text("EARTH", font_size=24, color=WHITE, weight=BOLD)
        earth_label.move_to(ORIGIN)

        # Orbit path (circle around Earth)
        orbit_path = Circle(radius=3.5, color='#FFD700', stroke_width=3, stroke_opacity=0.5)

        # Cannonball/Moon
        ball = Circle(radius=0.3, color='#FF6B35', fill_opacity=1)
        ball.move_to(UP * 3.5)

        # Velocity arrow (tangential)
        v_arrow = Arrow(
            ball.get_center(),
            ball.get_center() + RIGHT * 1.2,
            color='#00FF00',
            stroke_width=5,
            buff=0
        )
        v_label = Text("v", font_size=24, color='#00FF00', weight=BOLD)
        v_label.next_to(v_arrow, UP, buff=0.1)

        # Gravity arrow (toward Earth)
        g_arrow = Arrow(
            ball.get_center(),
            ball.get_center() + DOWN * 1.0,
            color='#FF4444',
            stroke_width=5,
            buff=0
        )
        g_label = Text("g", font_size=24, color='#FF4444', weight=BOLD)
        g_label.next_to(g_arrow, LEFT, buff=0.1)

        # Perfect Speed label
        perfect_label = Text("PERFECT SPEED!", font_size=36, color='#FFD700', weight=BOLD)
        perfect_label.move_to(UP * 6)

        # "This is ORBIT!" text
        orbit_text = Text("This is ORBIT!", font_size=42, color='#00FF00', weight=BOLD)
        orbit_text.move_to(DOWN * 5)

        # Animation
        self.play(FadeIn(earth), FadeIn(earth_label), run_time=0.5)
        self.play(FadeIn(ball), Create(orbit_path), run_time=0.4)
        self.wait(wait_time)

        # Show velocity and gravity vectors
        self.play(Create(v_arrow), FadeIn(v_label), run_time=0.4)
        self.play(Create(g_arrow), FadeIn(g_label), run_time=0.4)
        self.wait(wait_time)

        # Animate ball going around orbit
        self.play(
            FadeIn(perfect_label),
            MoveAlongPath(ball, orbit_path),
            Rotate(v_arrow, angle=2*PI, about_point=ORIGIN),
            Rotate(g_arrow, angle=2*PI, about_point=ORIGIN),
            Rotate(v_label, angle=2*PI, about_point=ORIGIN),
            Rotate(g_label, angle=2*PI, about_point=ORIGIN),
            run_time=3.0,
            rate_func=linear
        )

        # Transform ball to Moon
        moon = Circle(radius=0.4, color='#CCCCCC', fill_opacity=0.9, stroke_width=2)
        moon.move_to(ball.get_center())
        moon_label = Text("MOON", font_size=18, color='#333333', weight=BOLD)
        moon_label.move_to(moon.get_center())

        self.play(
            Transform(ball, moon),
            FadeIn(moon_label),
            run_time=0.5
        )

        self.play(FadeIn(orbit_text, scale=1.3), run_time=0.5)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_04_reveal(self, timing):
        """Split screen: person falling vs Moon falling but missing (12.96s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.4 + 0.4 + 1.0 + 1.5 + 0.5 + 0.5 + 0.3  # 5.0s
        num_waits = 3
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Dividing line
        divider = Line(UP * 7, DOWN * 7, color=WHITE, stroke_width=2)

        # LEFT SIDE: Person falling straight
        left_title = Text("Normal Fall", font_size=28, color='#FF4444', weight=BOLD)
        left_title.move_to(LEFT * 2 + UP * 5.5)

        person = VGroup()
        body = Ellipse(width=0.5, height=1.2, color='#FF6B35', fill_opacity=0.8)
        head = Circle(radius=0.25, color='#FFCC99', fill_opacity=0.9)
        head.next_to(body, UP, buff=0.05)
        person.add(body, head)
        person.move_to(LEFT * 2 + UP * 3)

        ground_left = Line(LEFT * 3.5 + DOWN * 2, LEFT * 0.5 + DOWN * 2,
                           color='#654321', stroke_width=4)

        # RIGHT SIDE: Moon falling but missing Earth
        right_title = Text("Orbital Fall", font_size=28, color='#00FF00', weight=BOLD)
        right_title.move_to(RIGHT * 2 + UP * 5.5)

        earth_small = Circle(radius=0.8, color='#0066FF', fill_opacity=0.8)
        earth_small.move_to(RIGHT * 2 + DOWN * 1)

        moon_small = Circle(radius=0.25, color='#CCCCCC', fill_opacity=0.9)
        moon_small.move_to(RIGHT * 2 + UP * 2.5)

        # Curved path showing Moon "missing" Earth
        orbit_arc = Arc(radius=2.5, start_angle=90 * DEGREES, angle=-180 * DEGREES,
                        color='#FFD700', stroke_width=3, stroke_opacity=0.5)
        orbit_arc.move_to(RIGHT * 2 + DOWN * 1)

        # "Both FALLING!" text
        both_text = Text("Both FALLING!", font_size=40, color=YELLOW, weight=BOLD)
        both_text.move_to(DOWN * 4)

        # Mind-blow reveal
        reveal_text = Text("Orbit = Falling + MISSING!", font_size=36, color='#00FF00', weight=BOLD)
        reveal_text.move_to(DOWN * 5.5)

        # Animation
        self.play(Create(divider), run_time=0.4)
        self.play(
            Write(left_title), Write(right_title),
            run_time=0.4
        )

        # Left side setup
        self.play(
            FadeIn(person), FadeIn(ground_left),
            FadeIn(earth_small), FadeIn(moon_small),
            run_time=0.4
        )
        self.wait(wait_time)

        # Person falls straight down
        self.play(
            person.animate.move_to(LEFT * 2 + DOWN * 1.5),
            run_time=1.0
        )

        # Moon "falls" but curves around (orbit)
        self.play(
            Create(orbit_arc),
            MoveAlongPath(moon_small, orbit_arc),
            run_time=1.5
        )
        self.wait(wait_time)

        # Reveal text
        self.play(FadeIn(both_text, scale=1.2), run_time=0.5)
        self.play(FadeIn(reveal_text, shift=UP), run_time=0.5)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_05_key_point(self, timing):
        """Formula: v = sqrt(GM/r) with Goldilocks explanation (13.848s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.6 + 0.5 + 0.5 + 0.5 + 0.4 + 0.4 + 0.3  # 3.2s
        num_waits = 4
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Formula using Text (no LaTeX)
        formula_parts = VGroup()

        v_text = Text("v", font_size=60, color='#00FF00', weight=BOLD)
        equals = Text("=", font_size=50, color=WHITE)
        sqrt_symbol = Text("root", font_size=40, color=WHITE)

        # Fraction representation
        gm_text = Text("GM", font_size=40, color='#FFD700', weight=BOLD)
        fraction_line = Line(LEFT * 0.6, RIGHT * 0.6, color=WHITE, stroke_width=3)
        r_text = Text("r", font_size=40, color='#FF6B35', weight=BOLD)

        # Arrange formula
        v_text.move_to(LEFT * 2)
        equals.next_to(v_text, RIGHT, buff=0.3)
        sqrt_symbol.next_to(equals, RIGHT, buff=0.3)

        fraction = VGroup(gm_text, fraction_line, r_text)
        gm_text.move_to(UP * 0.3)
        fraction_line.next_to(gm_text, DOWN, buff=0.1)
        r_text.next_to(fraction_line, DOWN, buff=0.1)
        fraction.next_to(sqrt_symbol, RIGHT, buff=0.1)

        formula = VGroup(v_text, equals, sqrt_symbol, fraction)
        formula.move_to(UP * 3)

        # Legend
        g_legend = Text("G = Gravity constant", font_size=24, color='#FFD700')
        m_legend = Text("M = Earth's mass", font_size=24, color='#FFD700')
        r_legend = Text("r = Distance from center", font_size=24, color='#FF6B35')

        legend = VGroup(g_legend, m_legend, r_legend)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        legend.move_to(UP * 0.5)

        # Speedometer visual concept
        speedometer_bg = Arc(radius=1.5, start_angle=150 * DEGREES, angle=-120 * DEGREES,
                             color=WHITE, stroke_width=8)
        speedometer_bg.move_to(DOWN * 3)

        # Speed zones
        slow_zone = Arc(radius=1.5, start_angle=150 * DEGREES, angle=-40 * DEGREES,
                        color='#FF4444', stroke_width=8)
        slow_zone.move_to(DOWN * 3)

        perfect_zone = Arc(radius=1.5, start_angle=110 * DEGREES, angle=-40 * DEGREES,
                           color='#00FF00', stroke_width=8)
        perfect_zone.move_to(DOWN * 3)

        fast_zone = Arc(radius=1.5, start_angle=70 * DEGREES, angle=-40 * DEGREES,
                        color='#0066FF', stroke_width=8)
        fast_zone.move_to(DOWN * 3)

        # Labels
        crash_label = Text("CRASH", font_size=20, color='#FF4444', weight=BOLD)
        crash_label.move_to(DOWN * 3 + LEFT * 1.8 + UP * 0.3)

        orbit_label = Text("ORBIT", font_size=20, color='#00FF00', weight=BOLD)
        orbit_label.move_to(DOWN * 1.8)

        escape_label = Text("ESCAPE", font_size=20, color='#0066FF', weight=BOLD)
        escape_label.move_to(DOWN * 3 + RIGHT * 1.8 + UP * 0.3)

        # Goldilocks text
        goldilocks = Text("Goldilocks Speed!", font_size=32, color='#FFD700', weight=BOLD)
        goldilocks.move_to(DOWN * 5.5)

        # Key insight
        insight = Text("Satellite mass does NOT matter!", font_size=26, color='#FF6B35')
        insight.move_to(DOWN * 6.5)

        # Animation
        self.play(Write(formula), run_time=0.6)
        self.wait(wait_time)

        self.play(FadeIn(legend, shift=LEFT), run_time=0.5)
        self.wait(wait_time)

        # Speedometer
        self.play(
            Create(slow_zone),
            Create(perfect_zone),
            Create(fast_zone),
            run_time=0.5
        )
        self.play(
            FadeIn(crash_label),
            FadeIn(orbit_label),
            FadeIn(escape_label),
            run_time=0.5
        )
        self.wait(wait_time)

        self.play(FadeIn(goldilocks, scale=1.2), run_time=0.4)
        self.wait(wait_time)

        self.play(FadeIn(insight), run_time=0.4)
        self.wait(wait_time * 0.5)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_06_exam_tip(self, timing):
        """JEE exam tip: Orbital velocity depends on r, NOT satellite mass (9.648s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.4 + 0.4 + 0.5 + 0.5 + 0.5 + 0.4 + 0.3  # 3.4s
        num_waits = 3
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # JEE question box
        question_box = RoundedRectangle(
            width=7, height=2.5, corner_radius=0.2,
            color='#FFD700', fill_opacity=0.1, stroke_width=3
        )
        question_box.move_to(UP * 3)

        jee_badge = Text("J.E.E. QUESTION", font_size=24, color='#FFD700', weight=BOLD)
        jee_badge.move_to(UP * 4.8)

        question = Text(
            "Orbital velocity depends on:",
            font_size=28, color=WHITE
        )
        question.move_to(UP * 3)

        # Options
        option_a = Text("A) Satellite mass", font_size=26, color='#FF4444')
        option_b = Text("B) Orbital radius r", font_size=26, color='#00FF00')

        options = VGroup(option_a, option_b)
        options.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        options.move_to(UP * 0.5)

        # Cross on wrong answer
        wrong_cross = VGroup(
            Line(LEFT * 0.3 + UP * 0.3, RIGHT * 0.3 + DOWN * 0.3, color='#FF4444', stroke_width=5),
            Line(LEFT * 0.3 + DOWN * 0.3, RIGHT * 0.3 + UP * 0.3, color='#FF4444', stroke_width=5)
        )
        wrong_cross.move_to(option_a.get_left() + LEFT * 0.5)

        # Checkmark on correct answer
        checkmark = Text("CHECK", font_size=24, color='#00FF00', weight=BOLD)
        checkmark.move_to(option_b.get_left() + LEFT * 0.6)

        # Common mistake warning
        warning_box = RoundedRectangle(
            width=6, height=1.5, corner_radius=0.15,
            color='#FF4444', fill_opacity=0.2, stroke_width=2
        )
        warning_box.move_to(DOWN * 3)

        warning_text = Text("Common Mistake!", font_size=28, color='#FF4444', weight=BOLD)
        warning_text.move_to(DOWN * 2.5)

        tip_text = Text("Satellite mass cancels out!", font_size=24, color=WHITE)
        tip_text.move_to(DOWN * 3.5)

        # Remember text
        remember = Text("v depends on r only!", font_size=30, color='#00FF00', weight=BOLD)
        remember.move_to(DOWN * 5.5)

        # Animation
        self.play(FadeIn(question_box), Write(jee_badge), run_time=0.4)
        self.play(Write(question), run_time=0.4)
        self.wait(wait_time)

        self.play(FadeIn(options), run_time=0.4)
        self.wait(wait_time)

        # Show wrong and right
        self.play(Create(wrong_cross), run_time=0.5)
        self.play(FadeIn(checkmark, scale=1.5), run_time=0.5)
        self.wait(wait_time)

        # Warning
        self.play(
            FadeIn(warning_box),
            Write(warning_text),
            run_time=0.5
        )
        self.play(FadeIn(tip_text), run_time=0.4)

        self.play(FadeIn(remember, shift=UP), run_time=0.4)
        self.wait(wait_time * 0.5)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_07_cta(self, timing):
        """CTA: JeetLo Physics! - Use pre-built CTA slide (3.552s)"""
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
