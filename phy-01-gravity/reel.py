"""
JeetLo Physics Reel: Gravity - The Clingy Ex
=============================================
Topic: Newton's Law of Universal Gravitation
Duration: ~93 seconds
"""

import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')

from manim import *
from jeetlo_style import JeetLoReelMixin, create_brand_watermark
import numpy as np

# Import manim-edu components for physics
from manim_edu.physics import FieldVisualizer, MechanicsSimulator
from manim_edu.formulas import FormulaRenderer


class PhysicsReel(JeetLoReelMixin, Scene):
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
        """You're FALLING right now - Hook segment"""
        duration = timing['duration']

        # Title text - shocking reveal
        title = Text("You're FALLING", font_size=64, color=RED, weight=BOLD)
        title.move_to(UP * 3)

        subtitle = Text("Right Now!", font_size=52, color=YELLOW, weight=BOLD)
        subtitle.next_to(title, DOWN, buff=0.4)

        # Person sitting (simplified stick figure)
        person = VGroup()
        # Head
        head = Circle(radius=0.3, color=WHITE, fill_opacity=0.8, stroke_width=2)
        head.move_to(UP * 0.5)
        # Body
        body = Line(ORIGIN, DOWN * 1.2, color=WHITE, stroke_width=4)
        # Arms
        left_arm = Line(ORIGIN, LEFT * 0.6 + DOWN * 0.4, color=WHITE, stroke_width=3)
        right_arm = Line(ORIGIN, RIGHT * 0.6 + DOWN * 0.4, color=WHITE, stroke_width=3)
        # Legs
        left_leg = Line(DOWN * 1.2, DOWN * 2 + LEFT * 0.4, color=WHITE, stroke_width=3)
        right_leg = Line(DOWN * 1.2, DOWN * 2 + RIGHT * 0.4, color=WHITE, stroke_width=3)

        person.add(head, body, left_arm, right_arm, left_leg, right_leg)
        person.scale(0.6).move_to(ORIGIN)

        # Couch (simplified)
        couch = RoundedRectangle(width=2.5, height=0.8, corner_radius=0.2,
                                  color="#8B4513", fill_opacity=0.8, stroke_width=2)
        couch.move_to(DOWN * 1.5)

        # Earth below (partial circle at bottom)
        earth = Circle(radius=4, color=BLUE, fill_opacity=0.3, stroke_width=3)
        earth.move_to(DOWN * 7)

        # Big red arrow pointing down
        fall_arrow = Arrow(person.get_bottom() + DOWN * 0.3, DOWN * 4,
                          color=RED, stroke_width=8, max_tip_length_to_length_ratio=0.15)

        # Animation sequence
        self.play(FadeIn(person), FadeIn(couch), run_time=0.5)
        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(subtitle, scale=1.5), run_time=0.3)
        self.play(
            couch.animate.set_opacity(0.3),
            FadeIn(earth, shift=UP),
            run_time=0.5
        )
        self.play(Create(fall_arrow), run_time=0.4)

        # Pulse the arrow
        self.play(fall_arrow.animate.scale(1.1), run_time=0.2)
        self.play(fall_arrow.animate.scale(1/1.1), run_time=0.2)

        wait_time = duration - 2.5
        if wait_time > 0:
            self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_02_setup(self, timing):
        """Newton's apple and moon - same force!"""
        duration = timing['duration']

        # Split screen setup
        divider = Line(UP * 6, DOWN * 6, color=WHITE, stroke_width=2)

        # Left side - Apple falling
        left_title = Text("Apple", font_size=36, color=GREEN)
        left_title.move_to(LEFT * 2 + UP * 5)

        # Tree
        trunk = Rectangle(width=0.4, height=1.5, color="#8B4513",
                         fill_opacity=0.9, stroke_width=0)
        trunk.move_to(LEFT * 2.5 + UP * 0.5)
        leaves = Circle(radius=1, color=GREEN, fill_opacity=0.7, stroke_width=0)
        leaves.move_to(LEFT * 2.5 + UP * 2)
        tree = VGroup(trunk, leaves)

        # Apple
        apple = Circle(radius=0.2, color=RED, fill_opacity=1, stroke_width=0)
        apple.move_to(LEFT * 2 + UP * 1.5)

        # Arrow showing apple falling
        apple_arrow = Arrow(LEFT * 2 + UP * 1, LEFT * 2 + DOWN * 1,
                           color=YELLOW, stroke_width=4)

        # Right side - Moon orbiting Earth
        right_title = Text("Moon", font_size=36, color=TEAL)
        right_title.move_to(RIGHT * 2 + UP * 5)

        # Earth (small)
        mini_earth = Circle(radius=0.5, color=BLUE, fill_opacity=0.8, stroke_width=2)
        mini_earth.move_to(RIGHT * 2 + UP * 0.5)
        earth_label = Text("Earth", font_size=20, color=WHITE)
        earth_label.move_to(mini_earth)

        # Moon orbiting
        moon = Circle(radius=0.2, color="#C0C0C0", fill_opacity=0.9, stroke_width=2)
        moon.move_to(RIGHT * 2 + UP * 2.5)

        # Orbit path
        orbit = Circle(radius=2, color=WHITE, stroke_width=1, stroke_opacity=0.5)
        orbit.move_to(RIGHT * 2 + UP * 0.5)

        # Arrow showing moon falling toward Earth
        moon_arrow = Arrow(moon.get_center(), mini_earth.get_center(),
                          color=YELLOW, stroke_width=4, buff=0.3)

        # Question mark between them
        question = Text("?", font_size=72, color=YELLOW, weight=BOLD)
        question.move_to(DOWN * 2)

        # "SAME FORCE" reveal
        same_force = Text("SAME FORCE!", font_size=48, color=GOLD, weight=BOLD)
        same_force.move_to(DOWN * 2)

        # Glowing thread connecting apple and moon
        thread = Line(LEFT * 2 + DOWN * 1, RIGHT * 2 + UP * 2.5,
                     color=GOLD, stroke_width=3)

        # Animation
        self.play(FadeIn(divider), run_time=0.2)
        self.play(FadeIn(left_title), FadeIn(right_title), run_time=0.3)
        self.play(FadeIn(tree), FadeIn(apple), run_time=0.4)
        self.play(FadeIn(mini_earth), FadeIn(earth_label), FadeIn(orbit), FadeIn(moon), run_time=0.4)

        # Apple falls, moon "falls" toward Earth
        self.play(
            apple.animate.move_to(LEFT * 2 + DOWN * 0.5),
            Create(apple_arrow),
            Create(moon_arrow),
            run_time=0.6
        )

        self.play(FadeIn(question), run_time=0.3)
        self.play(Transform(question, same_force), run_time=0.4)

        # Connect with glowing thread
        self.play(Create(thread), run_time=0.4)
        self.play(thread.animate.set_color(YELLOW), run_time=0.2)

        wait_time = duration - 3.2
        if wait_time > 0:
            self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_03_content_part1(self, timing):
        """The Clingy Ex formula - F = Gm1m2/r^2"""
        duration = timing['duration']

        # Title: Earth as Clingy Ex
        title = Text("Earth = CLINGY EX", font_size=44, color=RED, weight=BOLD)
        title.move_to(UP * 5.5)

        # Earth with grabby hands (cartoon style)
        earth_face = VGroup()
        earth_body = Circle(radius=1.2, color=BLUE, fill_opacity=0.8, stroke_width=3)
        # Eyes
        left_eye = Dot(LEFT * 0.4 + UP * 0.3, color=WHITE, radius=0.15)
        right_eye = Dot(RIGHT * 0.4 + UP * 0.3, color=WHITE, radius=0.15)
        left_pupil = Dot(LEFT * 0.4 + UP * 0.3, color=BLACK, radius=0.07)
        right_pupil = Dot(RIGHT * 0.4 + UP * 0.3, color=BLACK, radius=0.07)
        # Heart eyes (for clingy ex effect)
        heart_l = Text("♥", font_size=20, color=RED).move_to(LEFT * 0.4 + UP * 0.3)
        heart_r = Text("♥", font_size=20, color=RED).move_to(RIGHT * 0.4 + UP * 0.3)
        # Mouth (smile)
        mouth = Arc(radius=0.4, start_angle=-PI, angle=PI, color=WHITE, stroke_width=3)
        mouth.move_to(DOWN * 0.2)

        earth_face.add(earth_body, left_eye, right_eye, left_pupil, right_pupil, mouth)
        earth_face.move_to(LEFT * 2.5 + UP * 1)

        # Grabby hands
        left_hand = VGroup()
        arm_l = Line(earth_body.get_right(), earth_body.get_right() + RIGHT * 1.5 + UP * 0.5,
                    color=BLUE, stroke_width=6)
        fingers_l = VGroup(*[Line(ORIGIN, UP * 0.3, color=BLUE, stroke_width=4).rotate(i * 0.3).shift(RIGHT * 2 + UP * 0.5)
                            for i in range(-2, 3)])
        left_hand.add(arm_l)
        left_hand.move_to(LEFT * 1 + UP * 1.5)

        right_hand = VGroup()
        arm_r = Line(earth_body.get_right(), earth_body.get_right() + RIGHT * 1.5 + DOWN * 0.5,
                    color=BLUE, stroke_width=6)
        right_hand.add(arm_r)
        right_hand.move_to(LEFT * 1 + UP * 0.5)

        # Formula using FormulaRenderer
        renderer = FormulaRenderer(scale=1.2, font_size=48)
        gravity_formula = renderer.gravity()
        gravity_formula.move_to(RIGHT * 1.5 + UP * 1)

        # Variable explanations (appearing one by one)
        g_explain = Text("G = Universe's constant", font_size=28, color=PURPLE)
        g_explain.move_to(DOWN * 1)

        m_explain = Text("m1, m2 = Mass (emotional baggage!)", font_size=28, color=GREEN)
        m_explain.move_to(DOWN * 2)

        r_explain = Text("r squared = Distance weakens grip!", font_size=28, color=RED)
        r_explain.move_to(DOWN * 3.5)

        # Animation
        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(earth_face), run_time=0.5)

        # Hands reaching out
        self.play(
            Create(arm_l),
            Create(arm_r),
            run_time=0.4
        )

        # Formula appears piece by piece
        self.play(Write(gravity_formula), run_time=1.0)

        # Explanations
        self.play(FadeIn(g_explain, shift=LEFT), run_time=0.5)
        self.play(FadeIn(m_explain, shift=LEFT), run_time=0.5)
        self.play(FadeIn(r_explain, shift=LEFT), run_time=0.5)

        # Highlight the r squared (distance)
        r_box = SurroundingRectangle(r_explain, color=YELLOW, buff=0.1)
        self.play(Create(r_box), run_time=0.3)

        wait_time = duration - 4.2
        if wait_time > 0:
            self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_03_content_part2(self, timing):
        """Gravity field visualization - spider web around Earth"""
        duration = timing['duration']

        # Title
        title = Text("Gravity Field", font_size=44, color=BLUE, weight=BOLD)
        title.move_to(UP * 5.5)

        # Earth at center
        earth = Circle(radius=0.8, color=BLUE, fill_opacity=0.8, stroke_width=3)
        earth.move_to(ORIGIN)
        earth_label = Text("Earth", font_size=24, color=WHITE)
        earth_label.move_to(earth)

        # Spider web field lines using FieldVisualizer concept
        field_lines = VGroup()
        num_lines = 12
        for i in range(num_lines):
            angle = 2 * PI * i / num_lines
            direction = np.array([np.cos(angle), np.sin(angle), 0])

            # Multiple arrows at different distances (denser near Earth)
            for dist in [1.2, 1.8, 2.5, 3.3]:
                start = direction * dist
                end = direction * (dist - 0.4)
                arrow = Arrow(start, end, color=GOLD, stroke_width=2,
                             buff=0, max_tip_length_to_length_ratio=0.3)
                arrow.set_opacity(1 - dist/4)  # Fade out with distance
                field_lines.add(arrow)

        # Person at close distance
        person_close = VGroup()
        pc_head = Circle(radius=0.15, color=GREEN, fill_opacity=0.8)
        pc_body = Line(ORIGIN, DOWN * 0.4, color=GREEN, stroke_width=3)
        person_close.add(pc_head, pc_body)
        person_close.move_to(RIGHT * 1.5 + UP * 0.3)

        close_label = Text("Close = STRONG pull!", font_size=24, color=GREEN)
        close_label.move_to(RIGHT * 2 + UP * 2)
        close_arrow = Arrow(close_label.get_bottom(), person_close.get_top(),
                           color=GREEN, stroke_width=2, buff=0.2)

        # Person at far distance
        person_far = VGroup()
        pf_head = Circle(radius=0.12, color=ORANGE, fill_opacity=0.8)
        pf_body = Line(ORIGIN, DOWN * 0.3, color=ORANGE, stroke_width=2)
        person_far.add(pf_head, pf_body)
        person_far.move_to(LEFT * 3 + DOWN * 2)

        far_label = Text("Far = weak pull", font_size=24, color=ORANGE)
        far_label.move_to(LEFT * 2.5 + DOWN * 4)
        far_arrow = Arrow(far_label.get_top(), person_far.get_bottom(),
                         color=ORANGE, stroke_width=2, buff=0.2)

        # Inverse square law badge
        law_badge = VGroup()
        badge_bg = RoundedRectangle(width=4, height=0.8, corner_radius=0.2,
                                    color=PURPLE, fill_opacity=0.3, stroke_width=2)
        badge_text = Text("Inverse Square Law!", font_size=28, color=PURPLE, weight=BOLD)
        law_badge.add(badge_bg, badge_text)
        law_badge.move_to(DOWN * 5)

        # Animation
        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(earth), FadeIn(earth_label), run_time=0.3)

        # Field lines appear like spider web
        self.play(LaggedStart(*[Create(arrow) for arrow in field_lines],
                              lag_ratio=0.02), run_time=1.0)

        # Close person with strong pull
        self.play(FadeIn(person_close), run_time=0.3)
        self.play(FadeIn(close_label), Create(close_arrow), run_time=0.4)

        # Far person with weak pull
        self.play(FadeIn(person_far), run_time=0.3)
        self.play(FadeIn(far_label), Create(far_arrow), run_time=0.4)

        # Law badge
        self.play(FadeIn(law_badge, scale=1.2), run_time=0.4)

        wait_time = duration - 3.5
        if wait_time > 0:
            self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_04_reveal(self, timing):
        """MIND BLOW: Orbiting IS falling!"""
        duration = timing['duration']

        # Title
        title = Text("MIND BLOW!", font_size=56, color=YELLOW, weight=BOLD)
        title.move_to(UP * 5.5)

        # Earth at center
        earth = Circle(radius=1, color=BLUE, fill_opacity=0.8, stroke_width=3)
        earth.move_to(ORIGIN)
        earth_label = Text("Earth", font_size=24, color=WHITE)
        earth_label.move_to(earth)

        # Moon
        moon = Circle(radius=0.3, color="#C0C0C0", fill_opacity=0.9, stroke_width=2)
        moon_start = RIGHT * 3 + UP * 1
        moon.move_to(moon_start)
        moon_label = Text("Moon", font_size=20, color=WHITE)
        moon_label.next_to(moon, UP, buff=0.1)

        # Arrow showing moon falling toward Earth
        fall_arrow = Arrow(moon.get_center(), earth.get_center(),
                          color=RED, stroke_width=4, buff=0.5)
        fall_label = Text("Falling!", font_size=24, color=RED, weight=BOLD)
        fall_label.next_to(fall_arrow, RIGHT, buff=0.2)

        # Arrow showing sideways motion
        sideways_arrow = Arrow(moon.get_center(), moon.get_center() + DOWN * 1.5 + LEFT * 0.5,
                              color=GREEN, stroke_width=4, buff=0)
        sideways_label = Text("Moving sideways!", font_size=24, color=GREEN)
        sideways_label.next_to(sideways_arrow, LEFT, buff=0.2)

        # Orbit path (dashed)
        orbit_path = Circle(radius=3.2, color=WHITE, stroke_width=2)
        orbit_path.move_to(ORIGIN)
        orbit_path.set_stroke(opacity=0.5)

        # Curved path showing "missing" Earth
        curve_points = [moon_start]
        for i in range(1, 30):
            angle = -i * 0.05
            r = 3.2
            curve_points.append(np.array([r * np.cos(angle + PI/6), r * np.sin(angle + PI/6), 0]))

        curved_path = VMobject()
        curved_path.set_points_smoothly([np.array(p) for p in curve_points])
        curved_path.set_stroke(color=TEAL, width=4)

        # Key insight text
        insight1 = Text("Orbiting = Perpetual Falling!", font_size=36, color=GOLD, weight=BOLD)
        insight1.move_to(DOWN * 3.5)

        insight2 = Text("You keep MISSING the ground!", font_size=32, color=PINK)
        insight2.move_to(DOWN * 4.5)

        # Mind explosion effect
        explosion_circles = VGroup(*[
            Circle(radius=0.5 + i*0.3, color=YELLOW, stroke_width=3-i*0.5, stroke_opacity=1-i*0.2)
            for i in range(5)
        ])
        explosion_circles.move_to(UP * 5.5)

        # Animation
        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(earth), FadeIn(earth_label), run_time=0.3)
        self.play(FadeIn(moon), FadeIn(moon_label), run_time=0.3)

        # Show falling toward Earth
        self.play(Create(fall_arrow), FadeIn(fall_label), run_time=0.5)
        self.wait(0.3)

        # But also moving sideways!
        self.play(Create(sideways_arrow), FadeIn(sideways_label), run_time=0.5)

        # Show the curved path
        self.play(FadeIn(orbit_path), run_time=0.3)
        self.play(Create(curved_path), run_time=0.8)

        # Move moon along the path a bit
        self.play(
            moon.animate.move_to(curve_points[15]),
            moon_label.animate.move_to(np.array(curve_points[15]) + UP * 0.4),
            run_time=0.6
        )

        # Key insight
        self.play(FadeIn(insight1, scale=1.3), run_time=0.4)
        self.play(FadeIn(insight2, shift=UP), run_time=0.4)

        # Mind explosion
        self.play(
            LaggedStart(*[Create(c) for c in explosion_circles], lag_ratio=0.1),
            title.animate.set_color(ORANGE),
            run_time=0.6
        )

        wait_time = duration - 4.4
        if wait_time > 0:
            self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_05_key_point(self, timing):
        """Inverse square relationship - distance doubles, force 1/4"""
        duration = timing['duration']

        # Title
        title = Text("The Key Formula", font_size=44, color=BLUE, weight=BOLD)
        title.move_to(UP * 5.5)

        # Visual demonstration
        # At distance 1x
        dist1_label = Text("Distance: 1x", font_size=28, color=WHITE)
        dist1_label.move_to(LEFT * 2.5 + UP * 3)

        # 4 weights representing force
        weights_1x = VGroup(*[
            Square(side_length=0.5, color=YELLOW, fill_opacity=0.8, stroke_width=2)
            for _ in range(4)
        ])
        weights_1x.arrange_in_grid(rows=2, cols=2, buff=0.1)
        weights_1x.move_to(LEFT * 2.5 + UP * 1)

        force1_label = Text("Force: 4 units", font_size=24, color=YELLOW)
        force1_label.next_to(weights_1x, DOWN, buff=0.3)

        # At distance 2x
        dist2_label = Text("Distance: 2x", font_size=28, color=WHITE)
        dist2_label.move_to(RIGHT * 2.5 + UP * 3)

        # 1 weight representing force (1/4)
        weight_2x = Square(side_length=0.5, color=YELLOW, fill_opacity=0.8, stroke_width=2)
        weight_2x.move_to(RIGHT * 2.5 + UP * 1)

        force2_label = Text("Force: 1 unit", font_size=24, color=YELLOW)
        force2_label.next_to(weight_2x, DOWN, buff=0.3)

        # Arrow showing the relationship
        relationship = VGroup()
        arrow = Arrow(LEFT * 0.5 + UP * 1, RIGHT * 1 + UP * 1, color=RED, stroke_width=4)
        arrow_label = Text("1/4", font_size=36, color=RED, weight=BOLD)
        arrow_label.next_to(arrow, UP, buff=0.1)
        relationship.add(arrow, arrow_label)

        # Key formula badge
        formula_text = Text("r squared in denominator!", font_size=32, color=GOLD, weight=BOLD)
        formula_text.move_to(DOWN * 2.5)

        # SQUARE IT emphasis
        square_it = Text("SQUARE IT!", font_size=48, color=RED, weight=BOLD)
        square_it.move_to(DOWN * 4)

        # Visual showing r^2 effect
        r_demo = VGroup()
        r1 = Text("r = 2", font_size=28, color=TEAL)
        r2 = Text("r squared = 4", font_size=28, color=ORANGE)
        r_demo.add(r1, r2)
        r_demo.arrange(DOWN, buff=0.3)
        r_demo.move_to(DOWN * 5.5)

        # Animation
        self.play(Write(title), run_time=0.4)

        # Show 1x distance with 4 weights
        self.play(FadeIn(dist1_label), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(w, scale=0.5) for w in weights_1x], lag_ratio=0.1), run_time=0.5)
        self.play(FadeIn(force1_label), run_time=0.3)

        # Show 2x distance with 1 weight
        self.play(FadeIn(dist2_label), run_time=0.3)
        self.play(FadeIn(weight_2x, scale=0.5), run_time=0.3)
        self.play(FadeIn(force2_label), run_time=0.3)

        # Relationship arrow
        self.play(Create(arrow), FadeIn(arrow_label), run_time=0.4)

        # Formula emphasis
        self.play(FadeIn(formula_text, shift=UP), run_time=0.4)

        # SQUARE IT!
        self.play(FadeIn(square_it, scale=1.5), run_time=0.3)
        self.play(square_it.animate.set_color(YELLOW), run_time=0.2)
        self.play(square_it.animate.set_color(RED), run_time=0.2)

        wait_time = duration - 3.5
        if wait_time > 0:
            self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_06_exam_tip(self, timing):
        """JEE favorite question - g = g0/4 at what height?"""
        duration = timing['duration']

        # Title
        title = Text("JEE Favorite!", font_size=44, color=PURPLE, weight=BOLD)
        title.move_to(UP * 5.5)

        jee_badge = VGroup()
        badge_bg = RoundedRectangle(width=2, height=0.8, corner_radius=0.2,
                                    color=ORANGE, fill_opacity=0.8, stroke_width=0)
        badge_text = Text("J.E.E.", font_size=28, color=WHITE, weight=BOLD)
        jee_badge.add(badge_bg, badge_text)
        jee_badge.move_to(UP * 5.5 + RIGHT * 2.5)

        # Question
        question = Text("Where is g = g0/4?", font_size=40, color=WHITE, weight=BOLD)
        question.move_to(UP * 3)

        # Diagram - Earth with height
        earth = Circle(radius=1.5, color=BLUE, fill_opacity=0.6, stroke_width=3)
        earth.move_to(DOWN * 1)

        earth_center = Dot(DOWN * 1, color=WHITE, radius=0.08)

        # Radius R
        radius_line = Line(DOWN * 1, DOWN * 1 + UP * 1.5, color=GREEN, stroke_width=3)
        r_label = Text("R", font_size=28, color=GREEN)
        r_label.next_to(radius_line, LEFT, buff=0.1)

        # Height above surface (another R)
        height_line = Line(DOWN * 1 + UP * 1.5, DOWN * 1 + UP * 3, color=YELLOW, stroke_width=3)
        h_label = Text("R", font_size=28, color=YELLOW)
        h_label.next_to(height_line, LEFT, buff=0.1)

        # Total distance from center = 2R
        total_line = DashedLine(DOWN * 1, DOWN * 1 + UP * 3, color=RED, stroke_width=2)
        total_label = Text("r = 2R", font_size=28, color=RED, weight=BOLD)
        total_label.next_to(total_line, RIGHT, buff=0.3)

        # Point at height
        point = Dot(DOWN * 1 + UP * 3, color=GOLD, radius=0.15)
        point_label = Text("g = g0/4", font_size=24, color=GOLD)
        point_label.next_to(point, RIGHT, buff=0.2)

        # Answer box
        answer_box = VGroup()
        ans_bg = RoundedRectangle(width=5, height=1.2, corner_radius=0.2,
                                  color=GREEN, fill_opacity=0.3, stroke_width=3)
        ans_text = Text("Answer: r = 2R", font_size=36, color=GREEN, weight=BOLD)
        ans_sub = Text("(One Earth radius above surface)", font_size=24, color=WHITE)
        answer_box.add(ans_bg, ans_text, ans_sub)
        ans_text.move_to(ans_bg.get_center() + UP * 0.2)
        ans_sub.move_to(ans_bg.get_center() + DOWN * 0.3)
        answer_box.move_to(DOWN * 4)

        # Common mistake
        mistake_box = VGroup()
        mistake_bg = RoundedRectangle(width=4.5, height=1, corner_radius=0.2,
                                      color=RED, fill_opacity=0.3, stroke_width=3)
        mistake_text = Text("NOT 4R from center!", font_size=28, color=RED, weight=BOLD)
        wrong_label = Text("WRONG!", font_size=20, color=RED)
        mistake_box.add(mistake_bg, mistake_text, wrong_label)
        mistake_text.move_to(mistake_bg.get_center())
        wrong_label.next_to(mistake_bg, LEFT, buff=0.2)
        mistake_box.move_to(DOWN * 5.8)

        # Animation
        self.play(Write(title), FadeIn(jee_badge), run_time=0.5)
        self.play(FadeIn(question), run_time=0.4)

        # Show Earth
        self.play(FadeIn(earth), FadeIn(earth_center), run_time=0.3)

        # Show radius
        self.play(Create(radius_line), FadeIn(r_label), run_time=0.4)

        # Show height
        self.play(Create(height_line), FadeIn(h_label), run_time=0.4)

        # Show total
        self.play(Create(total_line), FadeIn(total_label), run_time=0.4)

        # Show point
        self.play(FadeIn(point), FadeIn(point_label), run_time=0.3)

        # Answer
        self.play(FadeIn(answer_box, scale=1.1), run_time=0.5)

        # Common mistake warning
        self.play(FadeIn(mistake_box, shift=UP), run_time=0.4)
        self.play(
            mistake_box.animate.scale(1.05),
            run_time=0.2
        )
        self.play(mistake_box.animate.scale(1/1.05), run_time=0.2)

        wait_time = duration - 3.6
        if wait_time > 0:
            self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_07_cta(self, timing):
        """CTA - JeetLo Physics!"""
        duration = timing['duration']

        # Use the pre-built CTA slide from JeetLoReelMixin
        self.add_cta_slide_physics(duration)
