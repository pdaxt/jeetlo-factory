import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')
from manim import *
import numpy as np
from jeetlo_style import JeetLoReelMixin, create_brand_watermark, PHYSICS_BLUE, FLAME_PRIMARY, FLAME_CORE, TEXT_WHITE

# Import manim-edu components for physics
from manim_edu.physics import FieldVisualizer, MechanicsSimulator

# Color palette for this reel
EARTH_BLUE = "#4169E1"
MOON_GRAY = "#C0C0C0"
SUN_YELLOW = "#FFD700"
FORCE_ORANGE = "#FF6B35"
FORMULA_GREEN = "#00FF88"
HIGHLIGHT_TEAL = "#20B2AA"
ACCENT_PURPLE = "#9370DB"
STAR_WHITE = "#FFFFFF"


class GravityReel(JeetLoReelMixin, Scene):
    subject = "physics"

    def construct(self):
        self.camera.background_color = '#0A1A3F'
        self.add(create_brand_watermark())

        # Load timings from file
        import json
        with open('audio/timings.json') as f:
            self.timings = json.load(f)

        # Call each segment
        for seg in self.timings:
            method_name = f"segment_{seg['id']}"
            method = getattr(self, method_name, None)
            if method:
                method(seg)

    def segment_01_hook(self, timing):
        """Hook: Person 'falling' toward Earth - clingy ex metaphor"""
        duration = timing['duration']

        # Calculate timing
        total_anim = 0.5 + 0.8 + 0.6 + 0.4 + 0.3  # = 2.6s
        wait_time = max(0.1, (duration - total_anim) / 3)

        # Person (stick figure)
        person = VGroup()
        head = Circle(radius=0.25, color=WHITE, fill_opacity=1)
        body = Line(ORIGIN, DOWN * 0.8, color=WHITE, stroke_width=4)
        left_arm = Line(ORIGIN, DL * 0.4, color=WHITE, stroke_width=3)
        right_arm = Line(ORIGIN, DR * 0.4, color=WHITE, stroke_width=3)
        left_leg = Line(DOWN * 0.8, DOWN * 0.8 + DL * 0.5, color=WHITE, stroke_width=3)
        right_leg = Line(DOWN * 0.8, DOWN * 0.8 + DR * 0.5, color=WHITE, stroke_width=3)

        head.move_to(UP * 0.25)
        left_arm.shift(DOWN * 0.1)
        right_arm.shift(DOWN * 0.1)
        person.add(head, body, left_arm, right_arm, left_leg, right_leg)
        person.move_to(UP * 2)
        person.scale(0.8)

        # Earth with heart eyes (clingy ex)
        earth = Circle(radius=1.5, color=EARTH_BLUE, fill_opacity=0.9, stroke_width=3)
        earth.move_to(DOWN * 4)

        # Heart eyes on Earth
        heart_left = Text("♥", font_size=30, color=FORCE_ORANGE)
        heart_left.move_to(earth.get_center() + UP * 0.3 + LEFT * 0.4)
        heart_right = Text("♥", font_size=30, color=FORCE_ORANGE)
        heart_right.move_to(earth.get_center() + UP * 0.3 + RIGHT * 0.4)
        earth_group = VGroup(earth, heart_left, heart_right)

        # Text
        falling_text = Text("You're FALLING right now!", font_size=42, color=FORCE_ORANGE, weight=BOLD)
        falling_text.move_to(UP * 5)

        # Gravity arrows pulling person down
        arrows = VGroup()
        for i in range(5):
            angle = (i - 2) * 0.3
            start = person.get_center() + DOWN * 0.8
            end = start + DOWN * 1.2 + RIGHT * angle * 0.5
            arrow = Arrow(start, end, color=FORCE_ORANGE, stroke_width=4, buff=0)
            arrows.add(arrow)

        # Animation sequence
        self.play(FadeIn(person, shift=DOWN), run_time=0.5)
        self.wait(wait_time)

        self.play(
            FadeIn(earth_group, shift=UP),
            run_time=0.8
        )
        self.wait(wait_time)

        # Show arrows pulling down
        self.play(
            LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.1),
            run_time=0.6
        )

        self.play(
            Write(falling_text),
            person.animate.shift(DOWN * 0.5),
            run_time=0.4
        )
        self.wait(wait_time)

        # Pulse the hearts
        self.play(
            heart_left.animate.scale(1.3),
            heart_right.animate.scale(1.3),
            run_time=0.3
        )

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_02_setup(self, timing):
        """Setup: Apple falling vs Moon orbiting - same force?"""
        duration = timing['duration']

        total_anim = 0.5 + 0.5 + 0.5 + 0.4 + 0.4  # = 2.3s
        wait_time = max(0.1, (duration - total_anim) / 3)

        # Left side - Apple falling (Newton moment)
        left_title = Text("Apple", font_size=36, color=FORMULA_GREEN)
        left_title.move_to(LEFT * 2.5 + UP * 5)

        tree = VGroup()
        trunk = Rectangle(width=0.3, height=1.5, color="#8B4513", fill_opacity=1, stroke_width=0)
        leaves = Circle(radius=0.8, color=FORMULA_GREEN, fill_opacity=0.8, stroke_width=0)
        leaves.move_to(UP * 1.2)
        tree.add(trunk, leaves)
        tree.move_to(LEFT * 2.5 + UP * 1)
        tree.scale(0.8)

        apple = Circle(radius=0.15, color="#FF0000", fill_opacity=1, stroke_width=0)
        apple.move_to(LEFT * 2.5 + UP * 2)

        ground = Line(LEFT * 4 + DOWN * 2, LEFT * 1 + DOWN * 2, color=WHITE, stroke_width=2)

        # Right side - Moon orbiting
        right_title = Text("Moon", font_size=36, color=MOON_GRAY)
        right_title.move_to(RIGHT * 2.5 + UP * 5)

        small_earth = Circle(radius=0.4, color=EARTH_BLUE, fill_opacity=0.9, stroke_width=2)
        small_earth.move_to(RIGHT * 2.5)

        orbit_path = Circle(radius=1.5, color=WHITE, stroke_width=1, stroke_opacity=0.5)
        orbit_path.move_to(RIGHT * 2.5)

        moon = Circle(radius=0.2, color=MOON_GRAY, fill_opacity=0.9, stroke_width=2)
        moon.move_to(RIGHT * 2.5 + UP * 1.5)

        # Divider
        divider = DashedLine(UP * 5, DOWN * 5, color=WHITE, stroke_width=1, dash_length=0.2)

        # Question mark and text
        question = Text("Same Force?", font_size=48, color=SUN_YELLOW, weight=BOLD)
        question.move_to(DOWN * 4)

        # Animations
        self.play(
            FadeIn(left_title), FadeIn(right_title),
            Create(divider),
            run_time=0.5
        )

        self.play(
            FadeIn(tree), FadeIn(apple),
            Create(ground),
            FadeIn(small_earth), Create(orbit_path), FadeIn(moon),
            run_time=0.5
        )
        self.wait(wait_time)

        # Apple falls, moon orbits
        self.play(
            apple.animate.move_to(LEFT * 2.5 + DOWN * 1.8),
            Rotate(moon, angle=PI/2, about_point=RIGHT * 2.5),
            run_time=0.5
        )
        self.wait(wait_time)

        self.play(Write(question), run_time=0.4)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def segment_03_content_part1(self, timing):
        """Content Part 1: Universal Law of Gravitation formula breakdown"""
        duration = timing['duration']

        total_anim = 0.6 + 0.5 + 0.5 + 0.5 + 0.5 + 0.6 + 0.4  # = 3.6s
        wait_time = max(0.1, (duration - total_anim) / 5)

        # Title
        title = Text("Universal Law of Gravitation", font_size=36, color=PHYSICS_BLUE, weight=BOLD)
        title.move_to(UP * 5.5)

        # Build formula piece by piece using Text (not MathTex)
        # F = G m₁m₂/r²

        f_text = Text("F", font_size=72, color=FORCE_ORANGE, weight=BOLD)
        equals = Text("=", font_size=72, color=WHITE)
        g_text = Text("G", font_size=72, color=HIGHLIGHT_TEAL, weight=BOLD)

        m1_text = Text("m", font_size=60, color=EARTH_BLUE, weight=BOLD)
        m1_sub = Text("1", font_size=36, color=EARTH_BLUE)
        m1_sub.next_to(m1_text, DR, buff=-0.1).shift(DOWN * 0.1)
        m1_group = VGroup(m1_text, m1_sub)

        m2_text = Text("m", font_size=60, color=MOON_GRAY, weight=BOLD)
        m2_sub = Text("2", font_size=36, color=MOON_GRAY)
        m2_sub.next_to(m2_text, DR, buff=-0.1).shift(DOWN * 0.1)
        m2_group = VGroup(m2_text, m2_sub)

        # Fraction line
        frac_line = Line(LEFT * 1.2, RIGHT * 1.2, color=WHITE, stroke_width=3)

        r_text = Text("r", font_size=60, color=ACCENT_PURPLE, weight=BOLD)
        r_sup = Text("2", font_size=36, color=ACCENT_PURPLE)
        r_sup.next_to(r_text, UR, buff=-0.1).shift(UP * 0.1)
        r_group = VGroup(r_text, r_sup)

        # Arrange formula
        f_text.move_to(LEFT * 2.5 + UP * 2)
        equals.next_to(f_text, RIGHT, buff=0.3)
        g_text.next_to(equals, RIGHT, buff=0.3)

        numerator = VGroup(m1_group, m2_group).arrange(RIGHT, buff=0.1)
        numerator.next_to(g_text, RIGHT, buff=0.3).shift(UP * 0.3)

        frac_line.next_to(numerator, DOWN, buff=0.1)
        r_group.next_to(frac_line, DOWN, buff=0.1)

        formula_group = VGroup(f_text, equals, g_text, numerator, frac_line, r_group)
        formula_group.move_to(UP * 1.5)

        # Labels for each variable
        g_label = Text("Universe's relationship\ncounselor", font_size=24, color=HIGHLIGHT_TEAL)
        g_label.move_to(DOWN * 0.5)

        m_label = Text("Both masses", font_size=28, color=FORMULA_GREEN)
        m_label.move_to(DOWN * 2)

        r_label = Text("Distance between them", font_size=28, color=ACCENT_PURPLE)
        r_label.move_to(DOWN * 3.5)

        # Animations
        self.play(Write(title), run_time=0.6)
        self.wait(wait_time)

        # Build formula piece by piece
        self.play(Write(f_text), Write(equals), run_time=0.5)
        self.wait(wait_time)

        self.play(
            Write(g_text),
            FadeIn(g_label, shift=UP),
            run_time=0.5
        )
        self.wait(wait_time)

        self.play(
            Write(m1_group), Write(m2_group),
            FadeOut(g_label),
            FadeIn(m_label, shift=UP),
            run_time=0.5
        )
        self.wait(wait_time)

        self.play(
            Create(frac_line),
            Write(r_group),
            FadeOut(m_label),
            FadeIn(r_label, shift=UP),
            run_time=0.5
        )
        self.wait(wait_time)

        # Highlight the complete formula
        formula_box = SurroundingRectangle(formula_group, color=PHYSICS_BLUE, buff=0.3, corner_radius=0.2)
        self.play(Create(formula_box), run_time=0.6)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def segment_03_content_part2(self, timing):
        """Content Part 2: Ice rink analogy - same force, different acceleration"""
        duration = timing['duration']

        total_anim = 0.6 + 0.6 + 0.8 + 0.5 + 0.5 + 0.5 + 0.4  # = 3.9s
        wait_time = max(0.1, (duration - total_anim) / 5)

        # Title
        title = Text("Same Force, Different Effect!", font_size=36, color=FORCE_ORANGE, weight=BOLD)
        title.move_to(UP * 5.5)

        # Ice rink background
        ice_rink = Rectangle(width=7, height=4, color="#ADD8E6", fill_opacity=0.3, stroke_width=2)
        ice_rink.move_to(UP * 0.5)

        # Small person (you)
        small_person = VGroup()
        sp_head = Circle(radius=0.2, color=FORCE_ORANGE, fill_opacity=1, stroke_width=0)
        sp_body = Rectangle(width=0.3, height=0.6, color=FORCE_ORANGE, fill_opacity=0.8, stroke_width=0)
        sp_body.next_to(sp_head, DOWN, buff=0.05)
        small_person.add(sp_head, sp_body)
        small_person.move_to(LEFT * 1.5 + UP * 0.5)

        you_label = Text("You", font_size=24, color=FORCE_ORANGE)
        you_label.next_to(small_person, UP, buff=0.2)

        # Big person (Earth)
        big_person = VGroup()
        bp_head = Circle(radius=0.4, color=EARTH_BLUE, fill_opacity=1, stroke_width=0)
        bp_body = Rectangle(width=0.8, height=1.2, color=EARTH_BLUE, fill_opacity=0.8, stroke_width=0)
        bp_body.next_to(bp_head, DOWN, buff=0.05)
        big_person.add(bp_head, bp_body)
        big_person.move_to(RIGHT * 1.5 + UP * 0.5)

        earth_label = Text("Earth", font_size=24, color=EARTH_BLUE)
        earth_label.next_to(big_person, UP, buff=0.2)

        # Force arrows (equal and opposite)
        force_left = Arrow(
            big_person.get_left() + LEFT * 0.2,
            big_person.get_left() + LEFT * 1.2,
            color=FORMULA_GREEN, stroke_width=5, buff=0
        )
        force_right = Arrow(
            small_person.get_right() + RIGHT * 0.2,
            small_person.get_right() + RIGHT * 1.2,
            color=FORMULA_GREEN, stroke_width=5, buff=0
        )

        force_label = Text("Same Force F", font_size=28, color=FORMULA_GREEN, weight=BOLD)
        force_label.move_to(DOWN * 2)

        # Result text
        result_text = Text("Small person moves MORE!", font_size=32, color=SUN_YELLOW, weight=BOLD)
        result_text.move_to(DOWN * 3.5)

        # Explanation
        explain = Text("F = ma → Same F, smaller m = bigger a!", font_size=28, color=WHITE)
        explain.move_to(DOWN * 5)

        # Animations
        self.play(Write(title), run_time=0.6)

        self.play(
            FadeIn(ice_rink),
            FadeIn(small_person), FadeIn(you_label),
            FadeIn(big_person), FadeIn(earth_label),
            run_time=0.6
        )
        self.wait(wait_time)

        # Show equal forces
        self.play(
            Create(force_left),
            Create(force_right),
            Write(force_label),
            run_time=0.8
        )
        self.wait(wait_time)

        # Small person moves a lot, big person barely moves
        self.play(
            small_person.animate.shift(LEFT * 2),
            you_label.animate.shift(LEFT * 2),
            force_right.animate.shift(LEFT * 2),
            big_person.animate.shift(RIGHT * 0.2),
            earth_label.animate.shift(RIGHT * 0.2),
            force_left.animate.shift(RIGHT * 0.2),
            run_time=0.5
        )
        self.wait(wait_time)

        self.play(Write(result_text), run_time=0.5)
        self.wait(wait_time)

        self.play(Write(explain), run_time=0.5)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def segment_03_content_part3(self, timing):
        """Content Part 3: Distance squared - double distance = quarter force"""
        duration = timing['duration']

        total_anim = 0.5 + 0.6 + 0.6 + 0.5 + 0.5 + 0.4  # = 3.1s
        wait_time = max(0.1, (duration - total_anim) / 4)

        # Title
        title = Text("Distance SQUARED Magic!", font_size=36, color=ACCENT_PURPLE, weight=BOLD)
        title.move_to(UP * 5.5)

        # Scene 1: Two masses at distance r
        mass1 = Circle(radius=0.4, color=EARTH_BLUE, fill_opacity=0.9, stroke_width=2)
        mass1.move_to(LEFT * 2 + UP * 2)
        m1_label = Text("m₁", font_size=24, color=WHITE)
        m1_label.move_to(mass1)

        mass2 = Circle(radius=0.3, color=MOON_GRAY, fill_opacity=0.9, stroke_width=2)
        mass2.move_to(RIGHT * 0 + UP * 2)
        m2_label = Text("m₂", font_size=24, color=WHITE)
        m2_label.move_to(mass2)

        # Distance label
        dist_line1 = Line(mass1.get_right(), mass2.get_left(), color=ACCENT_PURPLE, stroke_width=3)
        dist_label1 = Text("r", font_size=36, color=ACCENT_PURPLE, weight=BOLD)
        dist_label1.next_to(dist_line1, UP, buff=0.1)

        # Force arrow (big)
        force1 = Arrow(
            mass2.get_left() + LEFT * 0.1,
            mass2.get_left() + LEFT * 1.5,
            color=FORCE_ORANGE, stroke_width=6, buff=0
        )
        force1_label = Text("F", font_size=32, color=FORCE_ORANGE, weight=BOLD)
        force1_label.next_to(force1, DOWN, buff=0.1)

        # Scene 2: Same masses at distance 2r
        mass1_far = Circle(radius=0.4, color=EARTH_BLUE, fill_opacity=0.9, stroke_width=2)
        mass1_far.move_to(LEFT * 3 + DOWN * 2)
        m1_label_far = Text("m₁", font_size=24, color=WHITE)
        m1_label_far.move_to(mass1_far)

        mass2_far = Circle(radius=0.3, color=MOON_GRAY, fill_opacity=0.9, stroke_width=2)
        mass2_far.move_to(RIGHT * 1 + DOWN * 2)
        m2_label_far = Text("m₂", font_size=24, color=WHITE)
        m2_label_far.move_to(mass2_far)

        # Distance label 2r
        dist_line2 = Line(mass1_far.get_right(), mass2_far.get_left(), color=ACCENT_PURPLE, stroke_width=3)
        dist_label2 = Text("2r", font_size=36, color=ACCENT_PURPLE, weight=BOLD)
        dist_label2.next_to(dist_line2, UP, buff=0.1)

        # Force arrow (small - 1/4)
        force2 = Arrow(
            mass2_far.get_left() + LEFT * 0.1,
            mass2_far.get_left() + LEFT * 0.4,
            color=FORCE_ORANGE, stroke_width=4, buff=0
        )
        force2_label = Text("F/4", font_size=28, color=FORCE_ORANGE, weight=BOLD)
        force2_label.next_to(force2, DOWN, buff=0.1)

        # Key insight
        key_text = Text("Double distance → Quarter force!", font_size=36, color=SUN_YELLOW, weight=BOLD)
        key_text.move_to(DOWN * 5)

        sun_note = Text("That's why Sun's pull feels weak despite its mass!", font_size=26, color=WHITE)
        sun_note.move_to(DOWN * 6)

        # Animations
        self.play(Write(title), run_time=0.5)

        # Show first scenario
        self.play(
            FadeIn(mass1), FadeIn(m1_label),
            FadeIn(mass2), FadeIn(m2_label),
            Create(dist_line1), Write(dist_label1),
            run_time=0.6
        )

        self.play(
            Create(force1),
            Write(force1_label),
            run_time=0.6
        )
        self.wait(wait_time)

        # Show second scenario (doubled distance)
        self.play(
            FadeIn(mass1_far), FadeIn(m1_label_far),
            FadeIn(mass2_far), FadeIn(m2_label_far),
            Create(dist_line2), Write(dist_label2),
            run_time=0.5
        )

        self.play(
            Create(force2),
            Write(force2_label),
            run_time=0.5
        )
        self.wait(wait_time)

        # Key insight
        self.play(
            Write(key_text),
            Write(sun_note),
            run_time=0.4
        )
        self.wait(wait_time * 2)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def segment_04_reveal(self, timing):
        """Reveal: You're connected to EVERY mass in the universe!"""
        duration = timing['duration']

        total_anim = 0.6 + 0.6 + 0.8 + 0.5 + 0.5 + 0.4  # = 3.4s
        wait_time = max(0.1, (duration - total_anim) / 4)

        # Start with you on Earth
        earth = Circle(radius=0.5, color=EARTH_BLUE, fill_opacity=0.9, stroke_width=2)
        earth.move_to(ORIGIN)

        person_dot = Dot(UP * 0.6, color=FORCE_ORANGE, radius=0.1)
        you_label = Text("You", font_size=20, color=FORCE_ORANGE)
        you_label.next_to(person_dot, UP, buff=0.1)

        # Sun
        sun = Circle(radius=0.8, color=SUN_YELLOW, fill_opacity=0.9, stroke_width=2)
        sun.move_to(LEFT * 3 + UP * 2)
        sun_label = Text("Sun", font_size=18, color=SUN_YELLOW)
        sun_label.next_to(sun, DOWN, buff=0.1)

        # Distant stars
        stars = VGroup()
        star_positions = [
            (RIGHT * 3 + UP * 3, "#FFFFFF"),
            (RIGHT * 3.5 + DOWN * 1, "#FFD700"),
            (LEFT * 3.5 + DOWN * 2, "#ADD8E6"),
            (UP * 4 + LEFT * 1, "#FF69B4"),
            (DOWN * 4 + RIGHT * 1, "#98FB98"),
            (UP * 3.5 + RIGHT * 2, "#DDA0DD"),
        ]

        for pos, color in star_positions:
            star = Star(n=5, outer_radius=0.15, inner_radius=0.07, color=color, fill_opacity=1, stroke_width=0)
            star.move_to(pos)
            stars.add(star)

        # Gravity connections (dotted lines to everything)
        connections = VGroup()
        all_objects = [sun, *stars]
        for obj in all_objects:
            line = DashedLine(
                person_dot.get_center(),
                obj.get_center(),
                color=FORCE_ORANGE, stroke_width=1, dash_length=0.1, stroke_opacity=0.5
            )
            connections.add(line)

        # Mind blow text
        mind_blow = Text("MIND BLOW!", font_size=48, color=FLAME_CORE, weight=BOLD)
        mind_blow.move_to(UP * 5.5)

        reveal_text = Text("You're connected to EVERY star!", font_size=32, color=SUN_YELLOW, weight=BOLD)
        reveal_text.move_to(DOWN * 5)

        universe_text = Text("The ENTIRE universe is pulling you!", font_size=28, color=WHITE)
        universe_text.move_to(DOWN * 6)

        # Animations
        self.play(
            FadeIn(earth),
            FadeIn(person_dot), FadeIn(you_label),
            run_time=0.6
        )

        self.play(
            FadeIn(sun), FadeIn(sun_label),
            run_time=0.6
        )
        self.wait(wait_time)

        # Zoom out to show stars
        self.play(
            LaggedStart(*[FadeIn(s, scale=0.5) for s in stars], lag_ratio=0.1),
            run_time=0.8
        )
        self.wait(wait_time)

        # Show connections
        self.play(
            LaggedStart(*[Create(c) for c in connections], lag_ratio=0.05),
            Write(mind_blow),
            run_time=0.5
        )

        self.play(
            Write(reveal_text),
            run_time=0.5
        )
        self.wait(wait_time)

        self.play(Write(universe_text), run_time=0.4)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def segment_05_key_point(self, timing):
        """Key Point: 3 Golden Rules"""
        duration = timing['duration']

        total_anim = 0.5 + 0.5 + 0.5 + 0.5 + 0.5 + 0.4  # = 2.9s
        wait_time = max(0.1, (duration - total_anim) / 4)

        # Title
        title = Text("3 GOLDEN RULES", font_size=48, color=SUN_YELLOW, weight=BOLD)
        title.move_to(UP * 5)

        # Rule cards
        card_width = 6.5
        card_height = 1.8

        # Rule 1
        card1 = RoundedRectangle(
            width=card_width, height=card_height,
            corner_radius=0.2, color=FORMULA_GREEN,
            fill_opacity=0.2, stroke_width=3
        )
        rule1_num = Text("1", font_size=48, color=FORMULA_GREEN, weight=BOLD)
        rule1_text = Text("Every mass attracts EVERY mass", font_size=28, color=WHITE)
        rule1_num.move_to(card1.get_left() + RIGHT * 0.5)
        rule1_text.move_to(card1.get_center() + RIGHT * 0.5)
        rule1 = VGroup(card1, rule1_num, rule1_text)
        rule1.move_to(UP * 2.5)

        # Rule 2
        card2 = RoundedRectangle(
            width=card_width, height=card_height,
            corner_radius=0.2, color=PHYSICS_BLUE,
            fill_opacity=0.2, stroke_width=3
        )
        rule2_num = Text("2", font_size=48, color=PHYSICS_BLUE, weight=BOLD)
        rule2_text = Text("Force depends on BOTH masses", font_size=28, color=WHITE)
        rule2_num.move_to(card2.get_left() + RIGHT * 0.5)
        rule2_text.move_to(card2.get_center() + RIGHT * 0.5)
        rule2 = VGroup(card2, rule2_num, rule2_text)
        rule2.move_to(UP * 0)

        # Rule 3 (with emphasis on SQUARED)
        card3 = RoundedRectangle(
            width=card_width, height=card_height,
            corner_radius=0.2, color=ACCENT_PURPLE,
            fill_opacity=0.2, stroke_width=3
        )
        rule3_num = Text("3", font_size=48, color=ACCENT_PURPLE, weight=BOLD)
        rule3_text1 = Text("Distance ", font_size=28, color=WHITE)
        rule3_squared = Text("SQUARED", font_size=32, color=FORCE_ORANGE, weight=BOLD)
        rule3_text2 = Text(" kills the force", font_size=28, color=WHITE)
        rule3_text = VGroup(rule3_text1, rule3_squared, rule3_text2).arrange(RIGHT, buff=0.1)
        rule3_num.move_to(card3.get_left() + RIGHT * 0.5)
        rule3_text.move_to(card3.get_center() + RIGHT * 0.3)
        rule3 = VGroup(card3, rule3_num, rule3_text)
        rule3.move_to(DOWN * 2.5)

        # Animations
        self.play(Write(title), run_time=0.5)
        self.wait(wait_time)

        # Rule 1
        self.play(
            FadeIn(card1, shift=RIGHT),
            Write(rule1_num), Write(rule1_text),
            run_time=0.5
        )
        self.wait(wait_time)

        # Rule 2
        self.play(
            FadeIn(card2, shift=RIGHT),
            Write(rule2_num), Write(rule2_text),
            run_time=0.5
        )
        self.wait(wait_time)

        # Rule 3
        self.play(
            FadeIn(card3, shift=RIGHT),
            Write(rule3_num), Write(rule3_text),
            run_time=0.5
        )
        self.wait(wait_time)

        # Pulse the SQUARED
        self.play(
            rule3_squared.animate.scale(1.3).set_color(SUN_YELLOW),
            run_time=0.5
        )
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def segment_06_exam_tip(self, timing):
        """Exam Tip: JEE question - if Earth's radius doubled"""
        duration = timing['duration']

        total_anim = 0.5 + 0.6 + 0.6 + 0.6 + 0.5 + 0.5 + 0.5 + 0.4  # = 4.2s
        wait_time = max(0.1, (duration - total_anim) / 5)

        # JEE Question header
        jee_badge = VGroup()
        badge_bg = RoundedRectangle(width=2, height=0.8, corner_radius=0.2, color=FORCE_ORANGE, fill_opacity=0.9, stroke_width=0)
        badge_text = Text("JEE", font_size=32, color=WHITE, weight=BOLD)
        jee_badge.add(badge_bg, badge_text)
        jee_badge.move_to(UP * 5.5)

        # Question
        question = Text("If Earth's radius DOUBLES but mass stays same...", font_size=28, color=WHITE)
        question.move_to(UP * 4)

        sub_q = Text("What happens to YOUR weight?", font_size=32, color=SUN_YELLOW, weight=BOLD)
        sub_q.move_to(UP * 2.5)

        # Before and after Earths
        earth_before = Circle(radius=0.6, color=EARTH_BLUE, fill_opacity=0.9, stroke_width=2)
        earth_before.move_to(LEFT * 2.5 + UP * 0)
        before_label = Text("R", font_size=28, color=WHITE)
        before_label.next_to(earth_before, DOWN, buff=0.2)

        earth_after = Circle(radius=1.2, color=EARTH_BLUE, fill_opacity=0.6, stroke_width=2)
        earth_after.move_to(RIGHT * 2 + UP * 0)
        after_label = Text("2R", font_size=28, color=WHITE)
        after_label.next_to(earth_after, DOWN, buff=0.2)

        arrow = Arrow(LEFT * 1, RIGHT * 0.3, color=WHITE, stroke_width=3)
        arrow.move_to(UP * 0)

        # Derivation
        deriv1 = Text("g' = GM / (2R)²", font_size=36, color=HIGHLIGHT_TEAL)
        deriv1.move_to(DOWN * 2)

        deriv2 = Text("g' = GM / 4R²", font_size=36, color=HIGHLIGHT_TEAL)
        deriv2.move_to(DOWN * 3)

        deriv3 = Text("g' = g/4", font_size=48, color=FORMULA_GREEN, weight=BOLD)
        deriv3.move_to(DOWN * 4.5)

        # Answer
        answer = Text("You'd weigh 1/4th!", font_size=40, color=SUN_YELLOW, weight=BOLD)
        answer.move_to(DOWN * 6)

        # Animations
        self.play(FadeIn(jee_badge, scale=0.5), run_time=0.5)

        self.play(Write(question), run_time=0.6)

        self.play(Write(sub_q), run_time=0.6)
        self.wait(wait_time)

        # Show the Earths
        self.play(
            FadeIn(earth_before), Write(before_label),
            Create(arrow),
            FadeIn(earth_after), Write(after_label),
            run_time=0.6
        )
        self.wait(wait_time)

        # Derivation
        self.play(Write(deriv1), run_time=0.5)
        self.wait(wait_time)

        self.play(Transform(deriv1.copy(), deriv2), FadeIn(deriv2), run_time=0.5)
        self.wait(wait_time)

        self.play(Write(deriv3), run_time=0.5)
        self.wait(wait_time)

        self.play(Write(answer), run_time=0.4)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def segment_07_cta(self, timing):
        """CTA: Standard JeetLo CTA with physics branding"""
        duration = timing['duration']
        self.add_cta_slide_physics(duration)


if __name__ == "__main__":
    # For testing
    scene = GravityReel()
    scene.render()
