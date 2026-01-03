import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')
from manim import *
from jeetlo_style import JeetLoReelMixin, create_brand_watermark

from manim_edu.physics import FieldVisualizer, MechanicsSimulator
from manim_edu.primitives import GrowingArrow, RippleEffect, PulseGlow

class PhysicsReel(JeetLoReelMixin, Scene):
    subject = "physics"

    def construct(self):
        self.camera.background_color = '#0A1A3F'
        self.add(create_brand_watermark())

        import json
        with open('audio/timings.json') as f:
            self.timings = json.load(f)

        for seg in self.timings:
            method_name = f"segment_{seg['id']}"
            method = getattr(self, method_name, None)
            if method:
                method(seg)

    def segment_01_hook(self, timing):
        duration = timing['duration']
        
        # Person sitting (simple representation)
        person = VGroup(
            Circle(radius=0.3, color=WHITE, fill_opacity=1),  # Head
            Line(ORIGIN, DOWN * 0.8, color=WHITE, stroke_width=4),  # Body
            Line(DOWN * 0.3, DOWN * 0.3 + LEFT * 0.4, color=WHITE, stroke_width=4),  # Left arm
            Line(DOWN * 0.3, DOWN * 0.3 + RIGHT * 0.4, color=WHITE, stroke_width=4),  # Right arm
            Line(DOWN * 0.8, DOWN * 0.8 + DL * 0.4, color=WHITE, stroke_width=4),  # Left leg
            Line(DOWN * 0.8, DOWN * 0.8 + DR * 0.4, color=WHITE, stroke_width=4),  # Right leg
        ).move_to(ORIGIN).scale(0.8)
        
        # Chair
        chair = VGroup(
            Line(LEFT * 0.5 + DOWN * 0.5, RIGHT * 0.5 + DOWN * 0.5, color=GOLD, stroke_width=5),  # Seat
            Line(RIGHT * 0.5 + DOWN * 0.5, RIGHT * 0.5 + UP * 0.3, color=GOLD, stroke_width=5),  # Back
        ).move_to(DOWN * 0.8)
        
        person_group = VGroup(person, chair).move_to(ORIGIN)
        
        # Earth below
        earth = Circle(radius=1.5, color=BLUE, fill_opacity=0.3, stroke_width=3)
        earth.move_to(DOWN * 4)
        earth_label = Text("EARTH", font_size=28, color=BLUE).move_to(earth.get_center())
        
        # Moon
        moon = Circle(radius=0.4, color=GRAY, fill_opacity=0.5, stroke_width=2)
        moon.move_to(UP * 4 + RIGHT * 3)
        moon_label = Text("Moon", font_size=20, color=GRAY).next_to(moon, UP, buff=0.1)
        
        # Sun
        sun = Circle(radius=0.6, color=YELLOW, fill_opacity=0.6, stroke_width=2)
        sun.move_to(UP * 5 + LEFT * 2.5)
        sun_label = Text("Sun", font_size=20, color=YELLOW).next_to(sun, UP, buff=0.1)
        
        # Arrows pulling toward person from all directions
        arrow_earth = Arrow(DOWN * 2.5, DOWN * 0.5, color=RED, stroke_width=6, buff=0)
        arrow_moon = Arrow(moon.get_center(), person.get_center() + UP * 0.5 + RIGHT * 0.5, color=TEAL, stroke_width=3, buff=0.3)
        arrow_sun = Arrow(sun.get_center(), person.get_center() + UP * 0.5 + LEFT * 0.3, color=ORANGE, stroke_width=4, buff=0.3)
        
        # Main text
        title = Text("You're FALLING right now!", font_size=42, color=RED)
        title.to_edge(UP, buff=1)
        
        # Animate
        self.play(FadeIn(person_group), run_time=0.5)
        self.play(
            FadeIn(earth), FadeIn(earth_label),
            FadeIn(moon), FadeIn(moon_label),
            FadeIn(sun), FadeIn(sun_label),
            run_time=0.8
        )
        self.play(
            Create(arrow_earth),
            Create(arrow_moon),
            Create(arrow_sun),
            run_time=0.8
        )
        self.play(Write(title), run_time=0.6)
        
        # Vibration effect
        for _ in range(3):
            self.play(
                person_group.animate.shift(UP * 0.05),
                run_time=0.1
            )
            self.play(
                person_group.animate.shift(DOWN * 0.05),
                run_time=0.1
            )
        
        wait_time = duration - 3.5
        self.wait(max(0.1, wait_time))
        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_02_setup(self, timing):
        duration = timing['duration']
        
        # Left side - Apple falling
        tree = VGroup(
            Rectangle(width=0.3, height=1.5, color=MAROON, fill_opacity=0.8),  # Trunk
            Circle(radius=1, color=GREEN, fill_opacity=0.6).shift(UP * 1.5),  # Leaves
        ).move_to(LEFT * 2.5 + DOWN * 1)
        
        apple = Circle(radius=0.15, color=RED, fill_opacity=1)
        apple.move_to(LEFT * 2.5 + UP * 1)
        
        apple_arrow = Arrow(apple.get_center(), apple.get_center() + DOWN * 1.5, color=YELLOW, stroke_width=4, buff=0)
        
        left_label = Text("Apple Falls", font_size=28, color=YELLOW)
        left_label.move_to(LEFT * 2.5 + DOWN * 3.5)
        
        # Right side - Moon orbiting Earth
        earth_r = Circle(radius=0.6, color=BLUE, fill_opacity=0.5)
        earth_r.move_to(RIGHT * 2.5)
        earth_r_label = Text("Earth", font_size=20, color=BLUE).next_to(earth_r, DOWN, buff=0.2)
        
        moon_r = Circle(radius=0.2, color=GRAY, fill_opacity=0.8)
        moon_r.move_to(RIGHT * 2.5 + UP * 2)
        
        orbit = DashedVMobject(Circle(radius=2, color=WHITE).move_to(RIGHT * 2.5), num_dashes=20)
        
        moon_arrow = Arrow(moon_r.get_center(), earth_r.get_center(), color=TEAL, stroke_width=4, buff=0.3)
        
        right_label = Text("Moon Orbits", font_size=28, color=TEAL)
        right_label.move_to(RIGHT * 2.5 + DOWN * 3.5)
        
        # Dividing line
        divider = DashedLine(UP * 4, DOWN * 4, color=WHITE, stroke_width=2)
        
        # Question text
        question = Text("SAME FORCE?", font_size=48, color=GOLD)
        question.to_edge(UP, buff=0.8)
        
        # Newton silhouette
        newton = VGroup(
            Circle(radius=0.25, color=WHITE, fill_opacity=0.8),
            Line(ORIGIN, DOWN * 0.5, color=WHITE, stroke_width=3),
        ).move_to(DOWN * 5)
        newton_label = Text("Newton", font_size=24, color=WHITE).next_to(newton, DOWN, buff=0.1)
        
        # Animate
        self.play(FadeIn(tree), FadeIn(apple), run_time=0.5)
        self.play(
            apple.animate.shift(DOWN * 2),
            Create(apple_arrow),
            run_time=0.6
        )
        self.play(Write(left_label), run_time=0.4)
        
        self.play(Create(divider), run_time=0.3)
        
        self.play(
            FadeIn(earth_r), FadeIn(earth_r_label),
            FadeIn(moon_r), Create(orbit),
            run_time=0.6
        )
        self.play(Create(moon_arrow), run_time=0.4)
        self.play(Write(right_label), run_time=0.4)
        
        self.play(Write(question), run_time=0.5)
        
        # Pulse the question
        self.play(question.animate.scale(1.1), run_time=0.3)
        self.play(question.animate.scale(1/1.1), run_time=0.3)
        
        self.play(FadeIn(newton), Write(newton_label), run_time=0.5)
        
        # Connect with dotted line
        connect_line = DashedLine(
            left_label.get_right() + RIGHT * 0.2,
            right_label.get_left() + LEFT * 0.2,
            color=GOLD, stroke_width=3
        ).shift(DOWN * 0.5)
        self.play(Create(connect_line), run_time=0.5)
        
        wait_time = duration - 5.0
        self.wait(max(0.1, wait_time))
        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_03_content_part1(self, timing):
        duration = timing['duration']
        
        # Title
        title = Text("Gravity Formula", font_size=40, color=GOLD)
        title.to_edge(UP, buff=0.8)
        
        # Build formula piece by piece using Text
        f_text = Text("F", font_size=60, color=RED)
        equals = Text("=", font_size=50, color=WHITE)
        g_text = Text("G", font_size=50, color=TEAL)
        
        # Fraction representation
        m1_text = Text("M", font_size=45, color=BLUE)
        m1_sub = Text("1", font_size=30, color=BLUE)
        m2_text = Text("M", font_size=45, color=GREEN)
        m2_sub = Text("2", font_size=30, color=GREEN)
        times_sign = Text("×", font_size=35, color=WHITE)
        
        r_text = Text("r", font_size=50, color=ORANGE)
        r_sq = Text("2", font_size=30, color=ORANGE)
        
        frac_line = Line(LEFT * 1.2, RIGHT * 1.2, color=WHITE, stroke_width=3)
        
        # Position formula
        f_text.move_to(LEFT * 2.5 + UP * 1)
        equals.next_to(f_text, RIGHT, buff=0.3)
        g_text.next_to(equals, RIGHT, buff=0.3)
        
        # Numerator
        m1_text.next_to(g_text, RIGHT, buff=0.4)
        m1_sub.next_to(m1_text, DR, buff=0.02).shift(UP * 0.1)
        times_sign.next_to(m1_sub, RIGHT, buff=0.15)
        m2_text.next_to(times_sign, RIGHT, buff=0.15)
        m2_sub.next_to(m2_text, DR, buff=0.02).shift(UP * 0.1)
        
        numerator = VGroup(m1_text, m1_sub, times_sign, m2_text, m2_sub)
        numerator.move_to(RIGHT * 1 + UP * 1.5)
        
        # Fraction line
        frac_line.move_to(RIGHT * 1 + UP * 0.8)
        
        # Denominator
        r_text.move_to(RIGHT * 0.8 + UP * 0.2)
        r_sq.next_to(r_text, UR, buff=0.02)
        
        denominator = VGroup(r_text, r_sq)
        
        # Reposition for better layout
        formula_group = VGroup(f_text, equals, g_text)
        formula_group.move_to(UP * 1.5)
        
        numerator.next_to(formula_group, RIGHT, buff=0.3).shift(UP * 0.3)
        frac_line.next_to(numerator, DOWN, buff=0.1)
        denominator.next_to(frac_line, DOWN, buff=0.1)
        
        # G value
        g_value = Text("G = 6.67 × 10⁻¹¹", font_size=32, color=TEAL)
        g_value.move_to(DOWN * 1)
        
        g_label = Text("Universe's WEAKNESS constant!", font_size=28, color=YELLOW)
        g_label.move_to(DOWN * 2)
        
        weak_text = Text("Gravity is the WEAKEST force!", font_size=36, color=RED)
        weak_text.move_to(DOWN * 3.5)
        
        # Animate
        self.play(Write(title), run_time=0.5)
        self.play(Write(f_text), run_time=0.4)
        self.play(Write(equals), run_time=0.2)
        self.play(Write(g_text), run_time=0.4)
        
        self.play(
            Write(m1_text), Write(m1_sub),
            Write(times_sign),
            Write(m2_text), Write(m2_sub),
            run_time=0.6
        )
        self.play(Create(frac_line), run_time=0.3)
        self.play(Write(r_text), Write(r_sq), run_time=0.5)
        
        self.play(Write(g_value), run_time=0.6)
        self.play(Write(g_label), run_time=0.5)
        
        # Highlight the tiny number
        self.play(g_value.animate.set_color(PINK).scale(1.2), run_time=0.4)
        self.play(g_value.animate.set_color(TEAL).scale(1/1.2), run_time=0.3)
        
        self.play(Write(weak_text), run_time=0.5)
        
        # Pulse weak text
        self.play(weak_text.animate.scale(1.15), run_time=0.3)
        self.play(weak_text.animate.scale(1/1.15), run_time=0.3)
        
        wait_time = duration - 5.5
        self.wait(max(0.1, wait_time))
        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_03_content_part2(self, timing):
        duration = timing['duration']
        
        # Title
        title = Text("Inverse Square Law", font_size=40, color=GOLD)
        title.to_edge(UP, buff=0.8)
        
        # Two scenarios side by side
        # Scenario A: Double mass
        scenario_a_title = Text("Double Mass", font_size=28, color=BLUE)
        scenario_a_title.move_to(LEFT * 2 + UP * 3)
        
        mass1_a = Circle(radius=0.4, color=BLUE, fill_opacity=0.7)
        mass1_a.move_to(LEFT * 3 + UP * 1)
        
        mass2_a = Circle(radius=0.8, color=BLUE, fill_opacity=0.7)  # Double size
        mass2_a.move_to(LEFT * 3 + DOWN * 1.5)
        
        arrow_a1 = Arrow(LEFT * 3 + UP * 0.5, LEFT * 3 + DOWN * 0.5, color=RED, stroke_width=4, buff=0)
        arrow_a2 = Arrow(LEFT * 3 + UP * 0.5, LEFT * 3 + DOWN * 1, color=RED, stroke_width=8, buff=0)  # Thicker
        
        result_a = Text("Force DOUBLES!", font_size=24, color=GREEN)
        result_a.move_to(LEFT * 2 + DOWN * 3.5)
        
        # Scenario B: Double distance - Flashlight analogy
        scenario_b_title = Text("Double Distance", font_size=28, color=ORANGE)
        scenario_b_title.move_to(RIGHT * 2 + UP * 3)
        
        # Flashlight representation
        flashlight = VGroup(
            Polygon(
                RIGHT * 1.5 + UP * 0.3,
                RIGHT * 1.5 + DOWN * 0.3,
                RIGHT * 2 + DOWN * 0.1,
                RIGHT * 2 + UP * 0.1,
                color=YELLOW, fill_opacity=0.8
            ),
        ).move_to(RIGHT * 1 + UP * 1)
        
        # Light spreading
        light_near = Polygon(
            RIGHT * 2.2 + UP * 0.2,
            RIGHT * 2.2 + DOWN * 0.2,
            RIGHT * 2.8 + DOWN * 0.5,
            RIGHT * 2.8 + UP * 0.5,
            color=YELLOW, fill_opacity=0.5
        ).move_to(RIGHT * 2.2 + UP * 1)
        
        light_far = Polygon(
            RIGHT * 2.8 + UP * 0.5,
            RIGHT * 2.8 + DOWN * 0.5,
            RIGHT * 3.5 + DOWN * 1,
            RIGHT * 3.5 + UP * 1,
            color=YELLOW, fill_opacity=0.2
        ).move_to(RIGHT * 3 + UP * 1)
        
        result_b = Text("Force becomes 1/4!", font_size=24, color=RED)
        result_b.move_to(RIGHT * 2 + DOWN * 0.5)
        
        # Calculator showing values
        calc_box = Rectangle(width=3.5, height=2, color=WHITE, stroke_width=2)
        calc_box.move_to(DOWN * 2.5)
        
        calc_text1 = Text("2× distance = 1/4 force", font_size=22, color=TEAL)
        calc_text2 = Text("3× distance = 1/9 force", font_size=22, color=TEAL)
        calc_text1.move_to(DOWN * 2.2)
        calc_text2.move_to(DOWN * 2.8)
        
        # Animate
        self.play(Write(title), run_time=0.5)
        
        # Scenario A
        self.play(Write(scenario_a_title), run_time=0.4)
        self.play(FadeIn(mass1_a), run_time=0.3)
        self.play(Create(arrow_a1), run_time=0.3)
        self.play(
            Transform(mass1_a, mass2_a),
            Transform(arrow_a1, arrow_a2),
            run_time=0.6
        )
        self.play(Write(result_a), run_time=0.4)
        
        # Scenario B
        self.play(Write(scenario_b_title), run_time=0.4)
        self.play(FadeIn(flashlight), run_time=0.3)
        self.play(FadeIn(light_near), run_time=0.3)
        self.play(FadeIn(light_far), run_time=0.3)
        self.play(Write(result_b), run_time=0.4)
        
        # Calculator
        self.play(Create(calc_box), run_time=0.3)
        self.play(Write(calc_text1), run_time=0.4)
        self.play(Write(calc_text2), run_time=0.4)
        
        # Highlight inverse square
        self.play(
            calc_text1.animate.set_color(YELLOW),
            calc_text2.animate.set_color(YELLOW),
            run_time=0.4
        )
        
        wait_time = duration - 5.5
        self.wait(max(0.1, wait_time))
        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_04_reveal(self, timing):
        duration = timing['duration']
        
        # Phone in hand
        phone = Rectangle(width=0.8, height=1.4, color=WHITE, fill_opacity=0.9)
        phone.move_to(ORIGIN)
        phone_screen = Rectangle(width=0.7, height=1.2, color=BLUE_E, fill_opacity=1)
        phone_screen.move_to(phone.get_center())
        
        hand = VGroup(
            Ellipse(width=1.2, height=0.6, color=GOLD_E, fill_opacity=0.7),
        ).move_to(DOWN * 0.9)
        
        phone_group = VGroup(phone, phone_screen, hand)
        
        # Multiple arrows from everywhere
        earth_arrow = Arrow(DOWN * 4, DOWN * 1.5, color=RED, stroke_width=8, buff=0)
        earth_label = Text("Earth", font_size=20, color=RED).move_to(DOWN * 4.5)
        
        moon_arrow = Arrow(UP * 5 + RIGHT * 3, UP * 1 + RIGHT * 0.5, color=GRAY, stroke_width=2, buff=0.3)
        moon_label = Text("Moon", font_size=16, color=GRAY).move_to(UP * 5.5 + RIGHT * 3)
        
        sun_arrow = Arrow(UP * 5 + LEFT * 2.5, UP * 1 + LEFT * 0.3, color=YELLOW, stroke_width=4, buff=0.3)
        sun_label = Text("Sun", font_size=18, color=YELLOW).move_to(UP * 5.5 + LEFT * 2.5)
        
        # Person next to you (microscopic arrow)
        person_arrow = Arrow(RIGHT * 3, RIGHT * 1, color=PINK, stroke_width=1, buff=0.3)
        person_label = Text("Person nearby!", font_size=14, color=PINK).move_to(RIGHT * 3.5)
        
        # More distant objects
        star_arrow1 = Arrow(LEFT * 3.5 + UP * 3, LEFT * 0.5 + UP * 0.5, color=TEAL, stroke_width=1, buff=0.3)
        star_arrow2 = Arrow(RIGHT * 2 + DOWN * 3, RIGHT * 0.3 + DOWN * 0.5, color=PURPLE, stroke_width=1, buff=0.3)
        
        # Title
        title = Text("EVERYTHING Pulls EVERYTHING!", font_size=36, color=GOLD)
        title.to_edge(UP, buff=0.8)
        
        subtitle = Text("Always. Forever.", font_size=28, color=WHITE)
        subtitle.move_to(DOWN * 5.5)
        
        # Animate
        self.play(FadeIn(phone_group), run_time=0.5)
        
        # Arrows appear one by one
        self.play(Create(earth_arrow), Write(earth_label), run_time=0.5)
        self.play(Create(moon_arrow), Write(moon_label), run_time=0.4)
        self.play(Create(sun_arrow), Write(sun_label), run_time=0.4)
        self.play(Create(person_arrow), Write(person_label), run_time=0.4)
        self.play(
            Create(star_arrow1),
            Create(star_arrow2),
            run_time=0.4
        )
        
        self.play(Write(title), run_time=0.6)
        
        # Mind explosion effect - ripples
        for i in range(3):
            ripple = Circle(radius=0.5 + i * 0.5, color=GOLD, stroke_width=3 - i)
            ripple.move_to(ORIGIN)
            self.play(
                Create(ripple),
                ripple.animate.scale(2).set_opacity(0),
                run_time=0.3
            )
            self.remove(ripple)
        
        self.play(Write(subtitle), run_time=0.5)
        
        wait_time = duration - 4.5
        self.wait(max(0.1, wait_time))
        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_05_key_point(self, timing):
        duration = timing['duration']
        
        # Title
        title = Text("Weak but RELENTLESS!", font_size=40, color=GOLD)
        title.to_edge(UP, buff=0.8)
        
        # Two arm wrestlers - EM vs Gravity
        # EM force - Hulk sized
        em_body = VGroup(
            Circle(radius=0.5, color=PURPLE, fill_opacity=0.8),
            Rectangle(width=1, height=1.5, color=PURPLE, fill_opacity=0.8).shift(DOWN * 1),
        ).move_to(LEFT * 2 + UP * 0.5)
        em_label = Text("Electromagnetic", font_size=20, color=PURPLE)
        em_label.next_to(em_body, DOWN, buff=0.3)
        em_size = Text("HUGE!", font_size=28, color=PURPLE)
        em_size.next_to(em_label, DOWN, buff=0.2)
        
        # Gravity - ant sized
        grav_body = VGroup(
            Circle(radius=0.15, color=RED, fill_opacity=0.8),
            Rectangle(width=0.3, height=0.4, color=RED, fill_opacity=0.8).shift(DOWN * 0.3),
        ).move_to(RIGHT * 2 + UP * 0.5)
        grav_label = Text("Gravity", font_size=20, color=RED)
        grav_label.next_to(grav_body, DOWN, buff=0.3)
        grav_size = Text("tiny...", font_size=20, color=RED)
        grav_size.next_to(grav_label, DOWN, buff=0.2)
        
        # VS text
        vs_text = Text("VS", font_size=48, color=WHITE)
        vs_text.move_to(UP * 0.5)
        
        # Magnet beating Earth's gravity
        magnet_text = Text("A tiny magnet beats", font_size=26, color=TEAL)
        magnet_text.move_to(DOWN * 2)
        earth_text = Text("Earth's ENTIRE gravity!", font_size=26, color=BLUE)
        earth_text.move_to(DOWN * 2.6)
        
        # But gravity wins at cosmic scale
        but_text = Text("BUT...", font_size=36, color=YELLOW)
        but_text.move_to(DOWN * 3.5)
        
        win_text = Text("Gravity shapes GALAXIES!", font_size=32, color=GOLD)
        win_text.move_to(DOWN * 4.3)
        
        reason = Text("Never gives up, never repels!", font_size=28, color=GREEN)
        reason.move_to(DOWN * 5.2)
        
        # Animate
        self.play(Write(title), run_time=0.5)
        
        self.play(FadeIn(em_body), Write(em_label), run_time=0.4)
        self.play(Write(em_size), run_time=0.3)
        
        self.play(Write(vs_text), run_time=0.3)
        
        self.play(FadeIn(grav_body), Write(grav_label), run_time=0.4)
        self.play(Write(grav_size), run_time=0.3)
        
        self.play(Write(magnet_text), run_time=0.4)
        self.play(Write(earth_text), run_time=0.4)
        
        self.play(Write(but_text), run_time=0.3)
        self.play(
            but_text.animate.scale(1.2).set_color(RED),
            run_time=0.3
        )
        
        self.play(Write(win_text), run_time=0.5)
        self.play(Write(reason), run_time=0.5)
        
        # Gravity grows to show it wins
        self.play(
            grav_body.animate.scale(3).set_color(GOLD),
            run_time=0.6
        )
        
        wait_time = duration - 5.2
        self.wait(max(0.1, wait_time))
        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_06_exam_tip(self, timing):
        duration = timing['duration']
        
        # JEE TRAP alert
        alert = Text("JEE TRAP ALERT!", font_size=44, color=RED)
        alert.to_edge(UP, buff=0.8)
        
        # Problem statement
        problem = Text("If Earth's mass DOUBLES", font_size=28, color=WHITE)
        problem.move_to(UP * 3)
        problem2 = Text("and radius DOUBLES...", font_size=28, color=WHITE)
        problem2.move_to(UP * 2.4)
        question = Text("What happens to g?", font_size=32, color=YELLOW)
        question.move_to(UP * 1.6)
        
        # Formula
        formula_text = Text("g = GM / R²", font_size=40, color=TEAL)
        formula_text.move_to(UP * 0.3)
        
        # Analysis box
        analysis_box = Rectangle(width=6, height=3.5, color=WHITE, stroke_width=2)
        analysis_box.move_to(DOWN * 2)
        
        # Step by step
        step1 = Text("Mass doubles: ×2 in numerator", font_size=24, color=BLUE)
        step1.move_to(DOWN * 0.8)
        
        step2 = Text("R doubles: R² = ×4 in denominator", font_size=24, color=ORANGE)
        step2.move_to(DOWN * 1.5)
        
        step3 = Text("Result: 2/4 = 1/2", font_size=28, color=GREEN)
        step3.move_to(DOWN * 2.3)
        
        answer = Text("g becomes HALF!", font_size=36, color=GOLD)
        answer.move_to(DOWN * 3.3)
        
        # Key reminder
        reminder = Text("R² in denominator!", font_size=32, color=RED)
        reminder.move_to(DOWN * 4.5)
        
        # Circle around R²
        r_circle = Circle(radius=0.6, color=RED, stroke_width=4)
        r_circle.move_to(formula_text.get_right() + LEFT * 0.4)
        
        # Animate
        self.play(Write(alert), run_time=0.5)
        self.play(alert.animate.set_color(YELLOW), run_time=0.2)
        self.play(alert.animate.set_color(RED), run_time=0.2)
        
        self.play(Write(problem), run_time=0.4)
        self.play(Write(problem2), run_time=0.4)
        self.play(Write(question), run_time=0.4)
        
        self.play(Write(formula_text), run_time=0.5)
        
        self.play(Create(analysis_box), run_time=0.3)
        self.play(Write(step1), run_time=0.5)
        
        # Highlight numerator
        self.play(step1.animate.set_color(TEAL), run_time=0.3)
        
        self.play(Write(step2), run_time=0.5)
        
        # Highlight denominator - this is the trap!
        self.play(
            step2.animate.set_color(RED).scale(1.1),
            run_time=0.4
        )
        self.play(step2.animate.scale(1/1.1), run_time=0.2)
        
        self.play(Write(step3), run_time=0.5)
        self.play(Write(answer), run_time=0.5)
        
        # Pulse answer
        self.play(answer.animate.scale(1.15), run_time=0.3)
        self.play(answer.animate.scale(1/1.15), run_time=0.3)
        
        self.play(Write(reminder), run_time=0.4)
        self.play(Create(r_circle), run_time=0.3)
        
        # Flash the circle
        for _ in range(2):
            self.play(r_circle.animate.set_color(YELLOW), run_time=0.2)
            self.play(r_circle.animate.set_color(RED), run_time=0.2)
        
        wait_time = duration - 7.0
        self.wait(max(0.1, wait_time))
        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_07_cta(self, timing):
        duration = timing['duration']
        self.add_cta_slide_physics(duration)