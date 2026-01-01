"""
JeetLo Physics Reel: What is Gravity? - The Universe's Obsessive Ex
====================================================================
VIRAL CONCEPT: Gravity isn't a force pulling you down - it's curved space
pushing you along! Einstein vs Newton. Mind-blowing spacetime visualization.

Animation Focus:
- Spacetime rubber sheet bending under mass
- Newton vs Einstein visual battle
- Gravitational field lines around Earth
- Gravitational waves from black holes
- Inverse square law visual demonstration
- JEE trick question reveal
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
CYAN = "#00FFFF"
SPACE_PURPLE = "#6B5B95"
GOLD = "#FFD700"
ORANGE = "#FF9800"
LIGHT_BLUE = "#87CEEB"


def load_timings():
    """Load audio timings from JSON file."""
    with open('audio/timings.json', 'r') as f:
        return {t['id']: t for t in json.load(f)}


class GravityReel(JeetLoReelMixin, Scene):
    """Physics reel explaining what gravity really is - spacetime curvature!"""
    subject = "physics"

    def construct(self):
        # Set physics background (dark blue)
        self.camera.background_color = PHYSICS_BG

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
        self.segment_03_content_part3(self.timings['03_content_part3'])
        self.segment_04_reveal(self.timings['04_reveal'])
        self.segment_05_key_point(self.timings['05_key_point'])
        self.segment_06_exam_tip(self.timings['06_exam_tip'])
        self.segment_07_cta(self.timings['07_cta'])

    def segment_01_hook(self, timing):
        """Hook: What is Gravity? WRONG! (4.656s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.3 + 0.4 + 0.3 + 0.4 + 0.3 + 0.2  # 1.9s
        num_waits = 2
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # JeetLo branding intro
        jeet = Text("Jeet", font_size=72, color=TEXT_WHITE, weight=BOLD)
        lo = Text("Lo", font_size=72, color=FLAME_PRIMARY, weight=BOLD)
        jeetlo = VGroup(jeet, lo).arrange(RIGHT, buff=0.05)
        physics = Text("PHYSICS", font_size=48, color=PHYSICS_BLUE, weight=BOLD)
        physics.next_to(jeetlo, DOWN, buff=0.3)
        intro = VGroup(jeetlo, physics).move_to(UP * 4)

        # Gravity question - elegant text
        gravity_q = Text("What is Gravity?", font_size=64, color=CYAN, weight=BOLD)
        gravity_q.move_to(UP * 1)

        # WRONG! stamp with dramatic effect
        wrong = Text("WRONG!", font_size=88, color=WRONG_RED, weight=BOLD)
        wrong.move_to(ORIGIN)
        wrong.rotate(15 * DEGREES)

        # Lie revealed
        lie_text = Text("You've been LIED to!", font_size=44, color=FLAME_CORE)
        lie_text.move_to(DOWN * 2.5)

        # Falling apple with question marks
        apple = Text("?", font_size=80)
        apple.move_to(DOWN * 0.5 + RIGHT * 2.5)
        q1 = Text("?", font_size=48, color=PHYSICS_BLUE).move_to(apple.get_center() + UP * 0.8 + LEFT * 0.4)
        q2 = Text("?", font_size=48, color=PHYSICS_BLUE).move_to(apple.get_center() + UP * 0.6 + RIGHT * 0.5)
        q3 = Text("?", font_size=48, color=PHYSICS_BLUE).move_to(apple.get_center() + RIGHT * 1)

        # Animations
        self.play(FadeIn(intro), run_time=0.3)
        self.play(Write(gravity_q), run_time=0.4)
        self.wait(wait_time)

        # Camera shake effect with WRONG stamp
        self.play(
            GrowFromCenter(wrong),
            Flash(wrong, color=WRONG_RED, line_length=0.4),
            run_time=0.3
        )
        self.play(
            FadeIn(apple),
            FadeIn(q1, scale=0.5),
            FadeIn(q2, scale=0.5),
            FadeIn(q3, scale=0.5),
            run_time=0.4
        )
        self.play(Write(lie_text), run_time=0.3)
        self.wait(wait_time)

        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.2)

    def segment_02_setup(self, timing):
        """Setup: Newton vs Einstein - Two different answers! (10.752s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.5 + 0.5 + 0.5 + 0.5 + 0.5 + 0.3  # 3.2s
        num_waits = 4
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Split screen setup - Newton on left
        newton_circle = Circle(radius=1.2, color=FLAME_PRIMARY, fill_opacity=0.2, stroke_width=3)
        newton_circle.move_to(LEFT * 2.5 + UP * 2.5)
        newton_emoji = Text("NEWTON", font_size=36, color=FLAME_PRIMARY, weight=BOLD)
        newton_emoji.move_to(newton_circle.get_center())
        newton_label = Text("Force PULLS down", font_size=28, color=FLAME_PRIMARY, weight=BOLD)
        newton_label.next_to(newton_circle, DOWN, buff=0.3)

        # Newton's thought bubble
        newton_thought = RoundedRectangle(width=3.5, height=1.5, corner_radius=0.2,
                                          color=FLAME_PRIMARY, fill_opacity=0.15)
        newton_thought.next_to(newton_label, DOWN, buff=0.3)
        newton_idea = Text("Gravity is a\nFORCE!", font_size=26, color=TEXT_WHITE)
        newton_idea.move_to(newton_thought.get_center())

        # Down arrow for Newton's idea
        newton_arrow = Arrow(start=UP * 0.3, end=DOWN * 0.5, color=FLAME_PRIMARY, stroke_width=5)
        newton_arrow.next_to(newton_thought, DOWN, buff=0.2)

        # Einstein on right
        einstein_circle = Circle(radius=1.2, color=PHYSICS_BLUE, fill_opacity=0.2, stroke_width=3)
        einstein_circle.move_to(RIGHT * 2.5 + UP * 2.5)
        einstein_emoji = Text("EINSTEIN", font_size=36, color=PHYSICS_BLUE, weight=BOLD)
        einstein_emoji.move_to(einstein_circle.get_center())
        einstein_label = Text("Space is BENDING!", font_size=28, color=PHYSICS_BLUE, weight=BOLD)
        einstein_label.next_to(einstein_circle, DOWN, buff=0.3)

        # Einstein's thought bubble
        einstein_thought = RoundedRectangle(width=3.5, height=1.5, corner_radius=0.2,
                                            color=PHYSICS_BLUE, fill_opacity=0.15)
        einstein_thought.next_to(einstein_label, DOWN, buff=0.3)
        einstein_idea = Text("Spacetime\nCURVATURE!", font_size=26, color=TEXT_WHITE)
        einstein_idea.move_to(einstein_thought.get_center())

        # Curved line for Einstein's idea
        curve = Arc(radius=0.8, start_angle=PI/4, angle=PI/2, color=PHYSICS_BLUE, stroke_width=4)
        curve.next_to(einstein_thought, DOWN, buff=0.2)

        # VS in center
        vs = Text("VS", font_size=72, color=GOLD, weight=BOLD)
        vs.move_to(UP * 2.5)

        # Bottom text - two different answers
        bottom_text = Text("Two geniuses, COMPLETELY different answers!",
                          font_size=32, color=FLAME_CORE, weight=BOLD)
        bottom_text.move_to(DOWN * 4)

        # Animations
        self.play(
            DrawBorderThenFill(newton_circle),
            FadeIn(newton_emoji),
            run_time=0.4
        )
        self.play(Write(newton_label), run_time=0.5)
        self.play(
            Create(newton_thought),
            Write(newton_idea),
            GrowArrow(newton_arrow),
            run_time=0.5
        )
        self.wait(wait_time)

        self.play(
            DrawBorderThenFill(einstein_circle),
            FadeIn(einstein_emoji),
            GrowFromCenter(vs),
            run_time=0.5
        )
        self.play(Write(einstein_label), run_time=0.5)
        self.wait(wait_time)

        self.play(
            Create(einstein_thought),
            Write(einstein_idea),
            Create(curve),
            run_time=0.5
        )
        self.wait(wait_time)

        self.play(Write(bottom_text), run_time=0.3)
        self.wait(wait_time)

        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_03_content_part1(self, timing):
        """Content Part 1: Space as rubber sheet bending (12.504s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.5 + 0.6 + 0.6 + 0.6 + 0.4 + 0.3  # 3.4s
        num_waits = 4
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Title
        title = Text("Spacetime = Rubber Sheet!", font_size=44, color=CYAN, weight=BOLD)
        title.to_edge(UP, buff=1)

        # Create grid lines for the "rubber sheet"
        grid = VGroup()
        for i in range(-4, 5):
            # Horizontal lines
            h_line = Line(LEFT * 3.5 + UP * (i * 0.5), RIGHT * 3.5 + UP * (i * 0.5),
                         color=SPACE_PURPLE, stroke_width=1.5, stroke_opacity=0.6)
            grid.add(h_line)
            # Vertical lines
            v_line = Line(LEFT * (i * 0.7) + UP * 2, LEFT * (i * 0.7) + DOWN * 2,
                         color=SPACE_PURPLE, stroke_width=1.5, stroke_opacity=0.6)
            grid.add(v_line)
        grid.move_to(DOWN * 0.5)

        # Earth (massive object) that will bend the sheet
        earth = Circle(radius=0.8, color=CORRECT_GREEN, fill_opacity=0.8, stroke_width=3)
        earth.move_to(DOWN * 0.5)
        earth_label = Text("EARTH", font_size=24, color=TEXT_WHITE, weight=BOLD)
        earth_label.move_to(earth.get_center())

        # Create bent grid lines (curved around Earth)
        bent_grid = VGroup()
        for i in range(-4, 5):
            # Create curved horizontal lines
            points = []
            for j in np.linspace(-3.5, 3.5, 50):
                x = j
                # Calculate displacement based on distance from center
                dist = np.sqrt(x**2 + (i * 0.5)**2)
                if dist < 2:
                    # Bend toward center (downward depression)
                    bend = -0.3 * (2 - dist) ** 1.5
                else:
                    bend = 0
                y = i * 0.5 + bend
                points.append([x, y, 0])
            curved = VMobject()
            curved.set_points_smoothly([np.array(p) for p in points])
            curved.set_stroke(color=PHYSICS_BLUE, width=2, opacity=0.8)
            bent_grid.add(curved)
        bent_grid.move_to(DOWN * 0.5)

        # Moon rolling along the curve
        moon = Circle(radius=0.25, color=LIGHT_BLUE, fill_opacity=0.9, stroke_width=2)
        moon.move_to(LEFT * 2.5 + UP * 0.5)
        moon_label = Text("Moon", font_size=18, color=TEXT_WHITE)
        moon_label.move_to(moon.get_center())

        # Curved path for moon to follow
        moon_path = Arc(radius=1.8, start_angle=PI * 0.7, angle=-PI * 0.8, color=CYAN)
        moon_path.move_to(DOWN * 0.3)

        # Key insight text
        insight = Text("Not gravity - CURVED SPACE!", font_size=36, color=FLAME_CORE, weight=BOLD)
        insight.move_to(DOWN * 4)

        # Animations
        self.play(Write(title), run_time=0.4)
        self.play(Create(grid), run_time=0.5)
        self.wait(wait_time)

        # Show Earth and bend the grid
        self.play(
            GrowFromCenter(earth),
            FadeIn(earth_label),
            run_time=0.6
        )
        self.play(
            Transform(grid, bent_grid),
            run_time=0.6
        )
        self.wait(wait_time)

        # Moon rolling along curve
        self.play(FadeIn(moon), FadeIn(moon_label), run_time=0.6)
        self.play(
            MoveAlongPath(moon, moon_path),
            MoveAlongPath(moon_label, moon_path),
            run_time=0.4
        )
        self.wait(wait_time)

        self.play(Write(insight), run_time=0.4)
        self.wait(wait_time)

        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_03_content_part2(self, timing):
        """Content Part 2: Formula and inverse square law (12.0s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.5 + 0.5 + 0.6 + 0.5 + 0.5 + 0.3  # 3.3s
        num_waits = 4
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Title
        title = Text("The Gravity Formula", font_size=48, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=1)

        # Formula box
        formula_box = RoundedRectangle(width=7, height=2.2, corner_radius=0.25,
                                       color=PHYSICS_BLUE, fill_opacity=0.2, stroke_width=3)
        formula_box.move_to(UP * 1.5)

        # Main formula: F = Gm1m2/r^2
        formula = MathTex(r"F = \frac{G \cdot m_1 \cdot m_2}{r^2}",
                         font_size=56, color=CYAN)
        formula.move_to(formula_box.get_center())

        # Two planets showing mutual pull
        planet1 = Circle(radius=0.5, color=PHYSICS_BLUE, fill_opacity=0.7, stroke_width=2)
        planet1.move_to(LEFT * 2 + DOWN * 2)
        p1_label = MathTex(r"m_1", font_size=28, color=TEXT_WHITE)
        p1_label.move_to(planet1.get_center())

        planet2 = Circle(radius=0.4, color=CORRECT_GREEN, fill_opacity=0.7, stroke_width=2)
        planet2.move_to(RIGHT * 2 + DOWN * 2)
        p2_label = MathTex(r"m_2", font_size=28, color=TEXT_WHITE)
        p2_label.move_to(planet2.get_center())

        # Arrows showing mutual attraction
        arrow1 = Arrow(start=LEFT * 1.2 + DOWN * 2, end=RIGHT * 0.8 + DOWN * 2,
                      color=FLAME_PRIMARY, stroke_width=4)
        arrow2 = Arrow(start=RIGHT * 1.2 + DOWN * 2, end=LEFT * 0.8 + DOWN * 2,
                      color=FLAME_PRIMARY, stroke_width=4)

        pull_text = Text("BOTH objects pull each other!", font_size=32, color=FLAME_CORE)
        pull_text.move_to(DOWN * 4)

        # Inverse square law demonstration
        inverse_title = Text("Distance 2x? Gravity = 1/4!", font_size=36, color=GOLD, weight=BOLD)
        inverse_title.move_to(DOWN * 5.5)

        # Animations
        self.play(Write(title), run_time=0.4)
        self.play(Create(formula_box), run_time=0.5)
        self.play(Write(formula), run_time=0.5)
        self.wait(wait_time)

        # Show the planets
        self.play(
            DrawBorderThenFill(planet1), FadeIn(p1_label),
            DrawBorderThenFill(planet2), FadeIn(p2_label),
            run_time=0.6
        )
        self.wait(wait_time)

        # Show mutual attraction
        self.play(GrowArrow(arrow1), GrowArrow(arrow2), run_time=0.5)
        self.play(Write(pull_text), run_time=0.5)
        self.wait(wait_time)

        self.play(Write(inverse_title), run_time=0.5)
        self.wait(wait_time)

        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_03_content_part3(self, timing):
        """Content Part 3: Gravitational waves and 8-minute fact (10.896s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.6 + 0.5 + 0.5 + 0.5 + 0.4 + 0.3  # 3.2s
        num_waits = 4
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Title
        title = Text("SHOCKING FACT!", font_size=52, color=WRONG_RED, weight=BOLD)
        title.to_edge(UP, buff=1)

        # Speed of gravity
        speed_text = Text("Gravity travels at LIGHT SPEED!", font_size=40, color=CYAN, weight=BOLD)
        speed_text.move_to(UP * 2.5)

        # Sun and Earth setup
        sun = Circle(radius=0.8, color=GOLD, fill_opacity=0.9, stroke_width=3)
        sun.move_to(LEFT * 2 + DOWN * 0.5)
        sun_label = Text("SUN", font_size=24, color=TEXT_WHITE, weight=BOLD)
        sun_label.move_to(sun.get_center())

        earth = Circle(radius=0.4, color=PHYSICS_BLUE, fill_opacity=0.8, stroke_width=2)
        earth.move_to(RIGHT * 2.5 + DOWN * 0.5)
        earth_label = Text("Earth", font_size=18, color=TEXT_WHITE)
        earth_label.move_to(earth.get_center())

        # Orbit path
        orbit = Circle(radius=2.2, color=TEXT_GRAY, stroke_width=1, stroke_opacity=0.5)
        orbit.move_to(LEFT * 0.3 + DOWN * 0.5)

        # Gravitational wave ripples
        waves = VGroup()
        for i in range(1, 5):
            wave = Circle(radius=i * 0.5, color=SPACE_PURPLE, stroke_width=2,
                         stroke_opacity=1 - i * 0.2)
            wave.move_to(sun.get_center())
            waves.add(wave)

        # 8 minutes text
        eight_min = Text("8 MINUTES to reach Earth!", font_size=36, color=FLAME_CORE)
        eight_min.move_to(DOWN * 3)

        # Mind-blow scenario
        disappear_text = Text("If Sun DISAPPEARED...", font_size=32, color=TEXT_WHITE)
        disappear_text.move_to(DOWN * 4.2)

        orbit_text = Text("We orbit NOTHING for 8 minutes!", font_size=34, color=GOLD, weight=BOLD)
        orbit_text.move_to(DOWN * 5.5)

        # Animations
        self.play(Write(title), run_time=0.4)
        self.play(Write(speed_text), run_time=0.6)
        self.wait(wait_time)

        # Show Sun and Earth with orbit
        self.play(
            GrowFromCenter(sun), FadeIn(sun_label),
            Create(orbit),
            GrowFromCenter(earth), FadeIn(earth_label),
            run_time=0.5
        )

        # Show gravitational waves
        self.play(
            AnimationGroup(*[GrowFromCenter(w) for w in waves], lag_ratio=0.15),
            run_time=0.5
        )
        self.wait(wait_time)

        self.play(Write(eight_min), run_time=0.5)
        self.play(Write(disappear_text), run_time=0.4)
        self.wait(wait_time)

        # Sun disappears effect
        self.play(
            sun.animate.set_opacity(0.3),
            sun_label.animate.set_opacity(0.3),
            Write(orbit_text),
            run_time=0.3
        )
        self.wait(wait_time)

        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_04_reveal(self, timing):
        """Reveal: Gravity = curved space pushing you! (11.064s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.6 + 0.6 + 0.5 + 0.5 + 0.5 + 0.3  # 3.4s
        num_waits = 4
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Epic title
        title = Text("THE REAL ANSWER!", font_size=56, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=1)

        # First reveal - NOT a force
        not_force = Text("Gravity is NOT a FORCE!", font_size=44, color=WRONG_RED, weight=BOLD)
        not_force.move_to(UP * 2.5)

        # Strike through "FORCE"
        strike = Line(LEFT * 1.2, RIGHT * 1.2, color=WRONG_RED, stroke_width=6)
        strike.move_to(not_force.get_center() + RIGHT * 1)

        # Second reveal - curved space
        curved = Text("It's CURVED SPACE!", font_size=48, color=CYAN, weight=BOLD)
        curved.move_to(UP * 0.5)

        # Push vs Pull visualization
        push_text = Text("That PUSHES you along!", font_size=40, color=CORRECT_GREEN, weight=BOLD)
        push_text.move_to(DOWN * 1)

        # Obsessive ex callback
        ex_box = RoundedRectangle(width=6.5, height=2, corner_radius=0.3,
                                  color=FLAME_PRIMARY, fill_opacity=0.2, stroke_width=3)
        ex_box.move_to(DOWN * 3.5)

        ex_text = Text("Like the Universe's\nOBSESSIVE EX!", font_size=36, color=FLAME_CORE, weight=BOLD)
        ex_text.move_to(ex_box.get_center())

        never_lets_go = Text("NEVER lets go!", font_size=32, color=WRONG_RED)
        never_lets_go.move_to(DOWN * 5.5)

        # Animations
        self.play(Write(title), run_time=0.4)
        self.play(Write(not_force), run_time=0.6)
        self.play(Create(strike), run_time=0.6)
        self.wait(wait_time)

        self.play(
            GrowFromCenter(curved),
            Flash(curved, color=CYAN),
            run_time=0.5
        )
        self.wait(wait_time)

        self.play(Write(push_text), run_time=0.5)
        self.wait(wait_time)

        self.play(
            Create(ex_box),
            Write(ex_text),
            run_time=0.5
        )
        self.play(Write(never_lets_go), run_time=0.3)
        self.wait(wait_time)

        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_05_key_point(self, timing):
        """Key Point: g = 9.8 m/s^2, formula g = GM/R^2 (10.2s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.5 + 0.5 + 0.5 + 0.5 + 0.3  # 2.7s
        num_waits = 4
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Title
        title = Text("Key Formula!", font_size=52, color=PHYSICS_BLUE, weight=BOLD)
        title.to_edge(UP, buff=1)

        # Main formula box
        formula_box = RoundedRectangle(width=6, height=2.5, corner_radius=0.25,
                                       color=PHYSICS_BLUE, fill_opacity=0.2, stroke_width=3)
        formula_box.move_to(UP * 1.5)

        # Formula: g = GM/R^2
        formula = MathTex(r"g = \frac{GM}{R^2}", font_size=64, color=CYAN)
        formula.move_to(formula_box.get_center())

        # Earth with radius marked
        earth = Circle(radius=1.2, color=CORRECT_GREEN, fill_opacity=0.5, stroke_width=3)
        earth.move_to(DOWN * 2 + LEFT * 2)
        earth_label = Text("EARTH", font_size=24, color=TEXT_WHITE, weight=BOLD)
        earth_label.move_to(earth.get_center())

        # Radius arrow
        radius_arrow = Arrow(start=earth.get_center(), end=earth.get_right(),
                            color=GOLD, stroke_width=4)
        r_label = Text("R", font_size=28, color=GOLD, weight=BOLD)
        r_label.next_to(radius_arrow, UP, buff=0.1)

        # Mass label
        m_label = Text("M", font_size=28, color=TEXT_WHITE, weight=BOLD)
        m_label.move_to(earth.get_center())

        # Value at Earth's surface
        value_box = RoundedRectangle(width=5, height=1.5, corner_radius=0.2,
                                     color=CORRECT_GREEN, fill_opacity=0.2, stroke_width=2)
        value_box.move_to(DOWN * 2 + RIGHT * 2)

        g_value = MathTex(r"g = 9.8 \text{ m/s}^2", font_size=40, color=CORRECT_GREEN)
        g_value.move_to(value_box.get_center())

        at_surface = Text("At Earth's surface", font_size=28, color=TEXT_GRAY)
        at_surface.next_to(value_box, DOWN, buff=0.3)

        # Key reminder
        remember = Text("Remember: R = Earth's radius!", font_size=32, color=FLAME_CORE)
        remember.move_to(DOWN * 5)

        # Animations
        self.play(Write(title), run_time=0.4)
        self.play(Create(formula_box), Write(formula), run_time=0.5)
        self.wait(wait_time)

        self.play(
            DrawBorderThenFill(earth),
            FadeIn(earth_label),
            run_time=0.5
        )
        self.play(
            GrowArrow(radius_arrow),
            FadeIn(r_label),
            FadeIn(m_label),
            run_time=0.5
        )
        self.wait(wait_time)

        self.play(Create(value_box), Write(g_value), run_time=0.5)
        self.play(Write(at_surface), run_time=0.3)
        self.wait(wait_time)

        self.play(Write(remember), run_time=0.3)
        self.wait(wait_time)

        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_06_exam_tip(self, timing):
        """Exam Tip: JEE trick - height where g is half (14.664s)"""
        duration = timing['duration']

        # Calculate timing
        fixed_time = 0.4 + 0.5 + 0.6 + 0.6 + 0.5 + 0.5 + 0.4 + 0.3  # 3.8s
        num_waits = 5
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Header
        header_box = RoundedRectangle(width=5, height=1.2, corner_radius=0.2,
                                      color=ORANGE, fill_opacity=0.9, stroke_width=0)
        header_box.to_edge(UP, buff=1)
        header = Text("JEE TRICK!", font_size=48, color=TEXT_WHITE, weight=BOLD)
        header.move_to(header_box.get_center())

        # Question
        question = Text("At what height is g reduced to HALF?", font_size=36, color=CYAN, weight=BOLD)
        question.move_to(UP * 2)

        # Working box
        work_box = RoundedRectangle(width=7, height=3.5, corner_radius=0.25,
                                    color=PHYSICS_BLUE, fill_opacity=0.15, stroke_width=2)
        work_box.move_to(DOWN * 0.5)

        # Step by step
        step1 = MathTex(r"g' = \frac{g}{2}", font_size=36, color=TEXT_WHITE)
        step1.move_to(work_box.get_top() + DOWN * 0.6)

        step2 = MathTex(r"\frac{GM}{(R+h)^2} = \frac{1}{2} \cdot \frac{GM}{R^2}",
                       font_size=32, color=TEXT_WHITE)
        step2.move_to(work_box.get_center())

        # Answer highlight
        answer_box = RoundedRectangle(width=6, height=1.3, corner_radius=0.2,
                                      color=CORRECT_GREEN, fill_opacity=0.3, stroke_width=3)
        answer_box.move_to(DOWN * 2.8)

        answer = MathTex(r"h = (\sqrt{2} - 1)R \approx 0.414R",
                        font_size=40, color=CORRECT_GREEN)
        answer.move_to(answer_box.get_center())

        # Common mistake warning
        mistake_box = RoundedRectangle(width=7, height=1.5, corner_radius=0.2,
                                       color=WRONG_RED, fill_opacity=0.2, stroke_width=3)
        mistake_box.move_to(DOWN * 5)

        mistake_text = Text("NOT half the distance!", font_size=32, color=WRONG_RED, weight=BOLD)
        mistake_text.move_to(mistake_box.get_center() + UP * 0.2)

        avoid = Text("Common mistake - AVOID this!", font_size=26, color=FLAME_CORE)
        avoid.move_to(mistake_box.get_center() + DOWN * 0.4)

        # Red circle around common mistake
        red_circle = Circle(radius=0.6, color=WRONG_RED, stroke_width=4)
        red_circle.move_to(answer.get_center() + LEFT * 2)

        # Animations
        self.play(Create(header_box), Write(header), run_time=0.4)
        self.play(Write(question), run_time=0.5)
        self.wait(wait_time)

        self.play(Create(work_box), Write(step1), run_time=0.6)
        self.play(Write(step2), run_time=0.6)
        self.wait(wait_time)

        self.play(Create(answer_box), Write(answer), run_time=0.5)
        self.wait(wait_time)

        self.play(
            Create(mistake_box),
            Write(mistake_text),
            run_time=0.5
        )
        self.play(Write(avoid), run_time=0.4)
        self.wait(wait_time)

        self.play(Create(red_circle), run_time=0.3)
        self.wait(wait_time)

        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_07_cta(self, timing):
        """CTA: Gravity never lets go... neither do we! (4.8s)"""
        duration = timing['duration']

        # Remove watermark for CTA slide
        self.remove(self.watermark)

        # Calculate timing
        fixed_time = 0.4 + 0.3 + 0.3 + 0.3 + 0.3 + 0.3  # 1.9s
        num_waits = 2
        wait_time = max(0.1, (duration - fixed_time) / num_waits)

        # Official brand flame
        flame = create_brand_flame(scale=0.8)
        flame.move_to(UP * 4)

        # Hearts orbiting (obsessive ex callback)
        hearts = VGroup()
        for i, angle in enumerate([0, PI/3, 2*PI/3, PI, 4*PI/3, 5*PI/3]):
            heart = Text("*", font_size=36, color=WRONG_RED)
            heart.move_to(UP * 4 + np.array([1.5 * np.cos(angle), 1.5 * np.sin(angle), 0]))
            hearts.add(heart)

        # Main CTA text
        gravity_text = Text("Gravity never lets go...", font_size=40, color=TEXT_WHITE)
        gravity_text.move_to(UP * 1.5)

        neither = Text("neither do we!", font_size=44, color=FLAME_CORE, weight=BOLD)
        neither.move_to(UP * 0.3)

        # JeetLo Physics
        jeetlo = VGroup(
            Text("Jeet", font_size=52, color=TEXT_WHITE, weight=BOLD),
            Text("Lo", font_size=52, color=FLAME_PRIMARY, weight=BOLD),
            Text(" Physics!", font_size=52, color=PHYSICS_BLUE, weight=BOLD)
        ).arrange(RIGHT, buff=0.05)
        jeetlo.move_to(DOWN * 1.2)

        # Follow CTA
        follow = Text("Follow for more!", font_size=40, color=GOLD, weight=BOLD)
        follow.move_to(DOWN * 2.8)

        # URL box
        url_box = RoundedRectangle(width=5, height=1.1, corner_radius=0.3,
                                   color=PHYSICS_BLUE, fill_opacity=0.15, stroke_width=3)
        url_box.move_to(DOWN * 4.5)
        url = Text("jeetlo.ai", font_size=44, color=PHYSICS_BLUE, weight=BOLD)
        url.move_to(url_box.get_center())

        # Animations
        self.play(FadeIn(flame, scale=0.5), run_time=0.4)
        self.play(AnimationGroup(*[FadeIn(h, scale=0.5) for h in hearts], lag_ratio=0.1), run_time=0.3)
        self.wait(wait_time)

        self.play(Write(gravity_text), run_time=0.3)
        self.play(Write(neither), run_time=0.3)
        self.play(FadeIn(jeetlo, scale=1.1), run_time=0.3)
        self.wait(wait_time)

        self.play(Write(follow), run_time=0.3)
        self.play(Create(url_box), Write(url), run_time=0.3)

        # Subtle pulse on flame
        self.play(flame.animate.scale(1.1), run_time=0.15)
        self.play(flame.animate.scale(1/1.1), run_time=0.15)


# Manim config for 9:16 vertical video
config.pixel_width = PIXEL_WIDTH
config.pixel_height = PIXEL_HEIGHT
config.frame_width = FRAME_WIDTH
config.frame_height = FRAME_HEIGHT
config.background_color = PHYSICS_BG
