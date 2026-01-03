import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')
from manim import *
from jeetlo_style import JeetLoReelMixin, create_brand_watermark

from manim_edu.physics import FieldVisualizer, MechanicsSimulator
from manim_edu.formulas import Formula, Term, Op, Frac

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
        
        # Person (stick figure) standing
        head = Circle(radius=0.3, color=WHITE, fill_opacity=1).shift(UP * 2)
        body = Line(UP * 1.7, UP * 0.2, color=WHITE, stroke_width=4)
        left_leg = Line(UP * 0.2, DOWN * 0.8 + LEFT * 0.4, color=WHITE, stroke_width=4)
        right_leg = Line(UP * 0.2, DOWN * 0.8 + RIGHT * 0.4, color=WHITE, stroke_width=4)
        left_arm = Line(UP * 1.2, UP * 0.5 + LEFT * 0.5, color=WHITE, stroke_width=4)
        right_arm = Line(UP * 1.2, UP * 0.5 + RIGHT * 0.5, color=WHITE, stroke_width=4)
        person = VGroup(head, body, left_leg, right_leg, left_arm, right_arm)
        person.move_to(ORIGIN)
        
        # Earth below
        earth = Circle(radius=2.5, color=BLUE, fill_opacity=0.3, stroke_width=3)
        earth.shift(DOWN * 4.5)
        earth_label = Text("EARTH", font_size=28, color=BLUE).move_to(earth.get_center())
        
        # Gravity arrows pulling person down
        arrows = VGroup()
        for i in range(5):
            arrow = Arrow(
                start=person.get_bottom() + DOWN * 0.2 + LEFT * 0.8 + RIGHT * 0.4 * i,
                end=person.get_bottom() + DOWN * 1.5 + LEFT * 0.8 + RIGHT * 0.4 * i,
                color=RED, stroke_width=3, buff=0
            )
            arrows.add(arrow)
        
        # Hook text
        hook_text = Text("You're FALLING right now!", font_size=42, color=YELLOW)
        hook_text.to_edge(UP, buff=1)
        
        # Earth with heart eyes (clingy ex metaphor)
        left_eye = Text("<3", font_size=24, color=PINK).move_to(earth.get_center() + UP * 0.3 + LEFT * 0.5)
        right_eye = Text("<3", font_size=24, color=PINK).move_to(earth.get_center() + UP * 0.3 + RIGHT * 0.5)
        
        total_anim = 0.5 + 0.4 + 0.4 + 0.3 + 0.4
        wait_time = max(0.1, (duration - total_anim) / 3)
        
        self.play(FadeIn(person), run_time=0.5)
        self.play(FadeIn(earth), FadeIn(earth_label), run_time=0.4)
        self.wait(wait_time)
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.1), run_time=0.4)
        self.play(Write(hook_text), run_time=0.3)
        self.wait(wait_time)
        self.play(FadeIn(left_eye), FadeIn(right_eye), run_time=0.4)
        self.wait(wait_time)
        
        self.play(FadeOut(VGroup(person, earth, earth_label, arrows, hook_text, left_eye, right_eye)), run_time=0.3)

    def segment_02_setup(self, timing):
        duration = timing['duration']
        
        # Left side - Apple falling
        left_title = Text("Apple Falling", font_size=32, color=GREEN).shift(LEFT * 2.5 + UP * 4)
        apple = Circle(radius=0.3, color=RED, fill_opacity=1).shift(LEFT * 2.5 + UP * 2)
        ground = Line(LEFT * 4, LEFT * 1, color=GREEN, stroke_width=3).shift(DOWN * 2)
        
        # Right side - Moon orbiting
        right_title = Text("Moon Orbiting", font_size=32, color=TEAL).shift(RIGHT * 2.5 + UP * 4)
        small_earth = Circle(radius=0.4, color=BLUE, fill_opacity=0.5).shift(RIGHT * 2.5)
        moon = Circle(radius=0.2, color=GRAY, fill_opacity=1).shift(RIGHT * 2.5 + UP * 1.5)
        orbit_path = Circle(radius=1.5, color=WHITE, stroke_width=1, stroke_opacity=0.3).shift(RIGHT * 2.5)
        
        # Dividing line
        divider = Line(UP * 5, DOWN * 3, color=WHITE, stroke_width=2, stroke_opacity=0.5)
        
        # Question
        question = Text("Same Force?", font_size=48, color=YELLOW).shift(DOWN * 4)
        question_mark = Text("?", font_size=72, color=ORANGE).next_to(question, RIGHT)
        
        total_anim = 0.4 + 0.4 + 0.6 + 0.4 + 0.3
        wait_time = max(0.1, (duration - total_anim) / 3)
        
        self.play(Create(divider), run_time=0.4)
        self.play(Write(left_title), Write(right_title), run_time=0.4)
        self.wait(wait_time)
        
        # Apple falls
        self.play(FadeIn(apple), Create(ground), run_time=0.3)
        self.play(apple.animate.shift(DOWN * 3.7), run_time=0.3)
        
        # Moon orbits
        self.play(FadeIn(small_earth), FadeIn(moon), Create(orbit_path), run_time=0.4)
        
        self.wait(wait_time)
        self.play(Write(question), FadeIn(question_mark), run_time=0.4)
        self.wait(wait_time)
        
        self.play(FadeOut(VGroup(left_title, right_title, apple, ground, small_earth, moon, orbit_path, divider, question, question_mark)), run_time=0.3)

    def segment_03_content_part1(self, timing):
        duration = timing['duration']
        
        # Title
        title = Text("Universal Law of Gravitation", font_size=36, color=GOLD).to_edge(UP, buff=1)
        
        # Build formula piece by piece using atomic system
        f_term = Term("F", color=YELLOW, size=60)
        equals = Op("=", color=WHITE, size=60)
        g_term = Term("G", color=PURPLE, size=60)
        m1_term = Term("m", sub="1", color=BLUE, sub_color=TEAL, size=60)
        m2_term = Term("m", sub="2", color=GREEN, sub_color=TEAL, size=60)
        
        # Numerator
        numerator = VGroup(g_term, m1_term, m2_term).arrange(RIGHT, buff=0.1)
        
        # Denominator
        r_term = Term("r", color=ORANGE, size=60)
        squared = Text("2", font_size=36, color=ORANGE).next_to(r_term, UR, buff=0.05)
        denominator = VGroup(r_term, squared)
        
        # Fraction line
        frac_line = Line(LEFT * 1.2, RIGHT * 1.2, color=WHITE, stroke_width=3)
        
        # Assemble formula
        fraction = VGroup(numerator, frac_line, denominator).arrange(DOWN, buff=0.15)
        full_formula = VGroup(f_term, equals, fraction).arrange(RIGHT, buff=0.2)
        full_formula.move_to(ORIGIN)
        
        # Labels for each part
        g_label = Text("Universe's\nRelationship\nCounselor", font_size=20, color=PURPLE).next_to(g_term, DOWN, buff=1.5)
        m_label = Text("Both\nMasses", font_size=20, color=BLUE).next_to(m1_term, DOWN, buff=1.5)
        r_label = Text("Distance!", font_size=20, color=ORANGE).next_to(denominator, DOWN, buff=0.8)
        
        total_anim = 0.4 + 0.5 + 0.4 + 0.4 + 0.4 + 0.4 + 0.4 + 0.4
        wait_time = max(0.1, (duration - total_anim) / 4)
        
        self.play(Write(title), run_time=0.4)
        self.wait(wait_time)
        
        # Reveal formula piece by piece
        self.play(FadeIn(f_term), FadeIn(equals), run_time=0.5)
        self.play(FadeIn(g_term), run_time=0.4)
        self.play(FadeIn(g_label), run_time=0.4)
        self.wait(wait_time)
        
        self.play(FadeIn(m1_term), FadeIn(m2_term), run_time=0.4)
        self.play(FadeIn(m_label), run_time=0.4)
        self.wait(wait_time)
        
        self.play(Create(frac_line), FadeIn(denominator), run_time=0.4)
        self.play(FadeIn(r_label), run_time=0.4)
        self.wait(wait_time)
        
        self.play(FadeOut(VGroup(title, full_formula, g_label, m_label, r_label)), run_time=0.3)

    def segment_03_content_part2(self, timing):
        duration = timing['duration']
        
        # Ice rink scene
        rink = Rectangle(width=7, height=3, color=TEAL, fill_opacity=0.2, stroke_width=2)
        rink.shift(DOWN * 0.5)
        rink_label = Text("Ice Rink", font_size=24, color=TEAL).next_to(rink, UP, buff=0.3)
        
        # Big person (left)
        big_head = Circle(radius=0.4, color=WHITE, fill_opacity=1).shift(LEFT * 2 + UP * 0.5)
        big_body = Rectangle(width=0.8, height=1.2, color=BLUE, fill_opacity=0.8).next_to(big_head, DOWN, buff=0.1)
        big_person = VGroup(big_head, big_body)
        big_label = Text("BIG", font_size=24, color=BLUE).next_to(big_person, DOWN, buff=0.3)
        
        # Small person (right)
        small_head = Circle(radius=0.25, color=WHITE, fill_opacity=1).shift(RIGHT * 2 + UP * 0.3)
        small_body = Rectangle(width=0.5, height=0.8, color=GREEN, fill_opacity=0.8).next_to(small_head, DOWN, buff=0.1)
        small_person = VGroup(small_head, small_body)
        small_label = Text("SMALL", font_size=24, color=GREEN).next_to(small_person, DOWN, buff=0.3)
        
        # Force arrows (same size - same force!)
        force_left = Arrow(LEFT * 0.5, LEFT * 1.5, color=RED, stroke_width=4, buff=0).next_to(big_person, RIGHT, buff=0.1)
        force_right = Arrow(RIGHT * 0.5, RIGHT * 1.5, color=RED, stroke_width=4, buff=0).next_to(small_person, LEFT, buff=0.1)
        
        # Text explanations
        same_force = Text("SAME Force!", font_size=36, color=YELLOW).to_edge(UP, buff=1)
        diff_accel = Text("Different Acceleration!", font_size=36, color=ORANGE).to_edge(UP, buff=1)
        
        total_anim = 0.4 + 0.4 + 0.4 + 0.4 + 0.5 + 0.4 + 0.8 + 0.4
        wait_time = max(0.1, (duration - total_anim) / 4)
        
        self.play(FadeIn(rink), Write(rink_label), run_time=0.4)
        self.play(FadeIn(big_person), FadeIn(big_label), run_time=0.4)
        self.play(FadeIn(small_person), FadeIn(small_label), run_time=0.4)
        self.wait(wait_time)
        
        # Show same force
        self.play(Create(force_left), Create(force_right), run_time=0.4)
        self.play(Write(same_force), run_time=0.5)
        self.wait(wait_time)
        
        # Push happens - small person moves more!
        self.play(
            big_person.animate.shift(LEFT * 0.3),
            small_person.animate.shift(RIGHT * 1.5),
            big_label.animate.shift(LEFT * 0.3),
            small_label.animate.shift(RIGHT * 1.5),
            run_time=0.4
        )
        self.wait(wait_time)
        
        self.play(Transform(same_force, diff_accel), run_time=0.8)
        self.wait(wait_time)
        
        self.play(FadeOut(VGroup(rink, rink_label, big_person, small_person, big_label, small_label, force_left, force_right, same_force)), run_time=0.4)

    def segment_03_content_part3(self, timing):
        duration = timing['duration']
        
        title = Text("Distance Squared Magic", font_size=36, color=GOLD).to_edge(UP, buff=1)
        
        # Two masses
        mass1 = Circle(radius=0.5, color=BLUE, fill_opacity=0.8).shift(LEFT * 2.5)
        mass2 = Circle(radius=0.5, color=GREEN, fill_opacity=0.8).shift(RIGHT * 0.5)
        m1_label = Text("M1", font_size=24, color=WHITE).move_to(mass1)
        m2_label = Text("M2", font_size=24, color=WHITE).move_to(mass2)
        
        # Distance indicator
        distance_line = Line(LEFT * 2, RIGHT * 0, color=YELLOW, stroke_width=3)
        distance_line.shift(DOWN * 1.5)
        r_text = Text("r", font_size=32, color=YELLOW).next_to(distance_line, DOWN, buff=0.2)
        
        # Force arrows
        force_arrow = Arrow(mass1.get_right(), mass2.get_left(), color=RED, stroke_width=4, buff=0.1)
        force_label = Text("F", font_size=36, color=RED).next_to(force_arrow, UP, buff=0.2)
        
        total_anim = 0.4 + 0.4 + 0.4 + 0.6 + 0.4 + 0.4
        wait_time = max(0.1, (duration - total_anim) / 3)
        
        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(mass1), FadeIn(mass2), FadeIn(m1_label), FadeIn(m2_label), run_time=0.4)
        self.play(Create(distance_line), Write(r_text), run_time=0.4)
        self.play(Create(force_arrow), Write(force_label), run_time=0.6)
        self.wait(wait_time)
        
        # Double distance
        new_mass2 = mass2.copy().shift(RIGHT * 3)
        new_m2_label = m2_label.copy().shift(RIGHT * 3)
        new_distance = Line(LEFT * 2, RIGHT * 3, color=YELLOW, stroke_width=3).shift(DOWN * 1.5)
        new_r_text = Text("2r", font_size=32, color=YELLOW).next_to(new_distance, DOWN, buff=0.2)
        
        # Smaller force arrow (1/4)
        new_force = Arrow(mass1.get_right(), new_mass2.get_left(), color=ORANGE, stroke_width=2, buff=0.1, max_tip_length_to_length_ratio=0.15)
        new_force_label = Text("F/4", font_size=28, color=ORANGE).next_to(new_force, UP, buff=0.2)
        
        result_text = Text("Double Distance = Quarter Force!", font_size=32, color=YELLOW).shift(DOWN * 4)
        
        self.play(
            Transform(mass2, new_mass2),
            Transform(m2_label, new_m2_label),
            Transform(distance_line, new_distance),
            Transform(r_text, new_r_text),
            Transform(force_arrow, new_force),
            Transform(force_label, new_force_label),
            run_time=0.4
        )
        self.wait(wait_time)
        
        self.play(Write(result_text), run_time=0.4)
        self.wait(wait_time)
        
        self.play(FadeOut(VGroup(title, mass1, mass2, m1_label, m2_label, distance_line, r_text, force_arrow, force_label, result_text)), run_time=0.3)

    def segment_04_reveal(self, timing):
        duration = timing['duration']
        
        # Earth
        earth = Circle(radius=0.6, color=BLUE, fill_opacity=0.8).move_to(ORIGIN)
        earth_label = Text("Earth", font_size=20, color=BLUE).next_to(earth, DOWN, buff=0.2)
        
        # Sun
        sun = Circle(radius=0.8, color=YELLOW, fill_opacity=0.9).shift(LEFT * 3 + UP * 2)
        sun_label = Text("Sun", font_size=20, color=YELLOW).next_to(sun, DOWN, buff=0.2)
        
        # Distant stars
        stars = VGroup()
        star_positions = [
            RIGHT * 3 + UP * 3,
            RIGHT * 2.5 + DOWN * 2,
            LEFT * 2.5 + DOWN * 3,
            LEFT * 3.5 + UP * 4,
            RIGHT * 3.5 + UP * 0.5,
        ]
        for pos in star_positions:
            star = Star(n=5, outer_radius=0.15, inner_radius=0.07, color=WHITE, fill_opacity=1).move_to(pos)
            stars.add(star)
        
        # Gravity connections (lines)
        connections = VGroup()
        for star in stars:
            line = DashedLine(earth.get_center(), star.get_center(), color=PURPLE, stroke_width=1, stroke_opacity=0.6)
            connections.add(line)
        sun_connection = DashedLine(earth.get_center(), sun.get_center(), color=ORANGE, stroke_width=2)
        
        # Mind-blow text
        mind_blow = Text("You're Connected to EVERY Star!", font_size=32, color=GOLD).to_edge(UP, buff=1)
        universe_text = Text("Gravitationally Linked\nto the ENTIRE Universe", font_size=28, color=TEAL).shift(DOWN * 4.5)
        
        total_anim = 0.4 + 0.4 + 0.4 + 0.5 + 0.5 + 0.4
        wait_time = max(0.1, (duration - total_anim) / 3)
        
        self.play(FadeIn(earth), Write(earth_label), run_time=0.4)
        self.play(FadeIn(sun), Write(sun_label), Create(sun_connection), run_time=0.4)
        self.wait(wait_time)
        
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in stars], lag_ratio=0.1), run_time=0.4)
        self.play(LaggedStart(*[Create(c) for c in connections], lag_ratio=0.05), run_time=0.5)
        self.wait(wait_time)
        
        self.play(Write(mind_blow), run_time=0.5)
        self.play(Write(universe_text), run_time=0.4)
        self.wait(wait_time)
        
        self.play(FadeOut(VGroup(earth, earth_label, sun, sun_label, stars, connections, sun_connection, mind_blow, universe_text)), run_time=0.3)

    def segment_05_key_point(self, timing):
        duration = timing['duration']
        
        title = Text("3 Golden Rules", font_size=42, color=GOLD).to_edge(UP, buff=1)
        
        # Rule cards
        rule1_box = RoundedRectangle(width=6, height=1.2, corner_radius=0.2, color=BLUE, fill_opacity=0.3, stroke_width=2)
        rule1_text = Text("1. Every mass attracts\n    every mass", font_size=24, color=WHITE)
        rule1 = VGroup(rule1_box, rule1_text).arrange(ORIGIN).shift(UP * 2)
        
        rule2_box = RoundedRectangle(width=6, height=1.2, corner_radius=0.2, color=GREEN, fill_opacity=0.3, stroke_width=2)
        rule2_text = Text("2. Force depends on\n    BOTH masses", font_size=24, color=WHITE)
        rule2 = VGroup(rule2_box, rule2_text).arrange(ORIGIN).shift(ORIGIN)
        
        rule3_box = RoundedRectangle(width=6, height=1.2, corner_radius=0.2, color=ORANGE, fill_opacity=0.3, stroke_width=2)
        rule3_text = Text("3. Distance SQUARED\n    kills the force", font_size=24, color=WHITE)
        rule3 = VGroup(rule3_box, rule3_text).arrange(ORIGIN).shift(DOWN * 2)
        
        # Emphasis on SQUARED
        squared_highlight = Text("SQUARED", font_size=28, color=YELLOW)
        squared_highlight.move_to(rule3_text.get_center() + LEFT * 0.3 + UP * 0.15)
        
        total_anim = 0.4 + 0.5 + 0.5 + 0.5 + 0.6
        wait_time = max(0.1, (duration - total_anim) / 4)
        
        self.play(Write(title), run_time=0.4)
        self.wait(wait_time)
        
        self.play(FadeIn(rule1, shift=LEFT), run_time=0.5)
        self.wait(wait_time)
        
        self.play(FadeIn(rule2, shift=LEFT), run_time=0.5)
        self.wait(wait_time)
        
        self.play(FadeIn(rule3, shift=LEFT), run_time=0.5)
        self.wait(wait_time)
        
        # Pulse the squared
        self.play(
            squared_highlight.animate.scale(1.3).set_color(RED),
            rate_func=there_and_back,
            run_time=0.6
        )
        
        self.play(FadeOut(VGroup(title, rule1, rule2, rule3, squared_highlight)), run_time=0.3)

    def segment_06_exam_tip(self, timing):
        duration = timing['duration']
        
        # JEE question style
        jee_badge = Text("JEE Question", font_size=28, color=RED).to_edge(UP, buff=0.8)
        jee_box = SurroundingRectangle(jee_badge, color=RED, buff=0.15)
        
        question = Text("If Earth's radius doubles\nbut mass stays same...\nYour weight = ?", font_size=28, color=WHITE)
        question.shift(UP * 2.5)
        
        # Calculation steps
        step1 = Text("g' = GM / (2R)²", font_size=36, color=YELLOW)
        step2 = Text("g' = GM / 4R²", font_size=36, color=ORANGE)
        step3 = Text("g' = g / 4", font_size=42, color=GREEN)
        
        steps = VGroup(step1, step2, step3).arrange(DOWN, buff=0.5).shift(DOWN * 0.5)
        
        # Answer highlight
        answer_box = RoundedRectangle(width=5, height=1.5, corner_radius=0.2, color=GREEN, fill_opacity=0.3)
        answer_text = Text("You weigh 1/4th!", font_size=36, color=GREEN)
        answer = VGroup(answer_box, answer_text).arrange(ORIGIN).shift(DOWN * 4)
        
        total_anim = 0.4 + 0.5 + 0.5 + 0.5 + 0.5 + 0.5
        wait_time = max(0.1, (duration - total_anim) / 4)
        
        self.play(Write(jee_badge), Create(jee_box), run_time=0.4)
        self.play(Write(question), run_time=0.5)
        self.wait(wait_time)
        
        self.play(Write(step1), run_time=0.5)
        self.wait(wait_time)
        
        self.play(Write(step2), run_time=0.5)
        self.wait(wait_time)
        
        self.play(Write(step3), run_time=0.5)
        self.wait(wait_time)
        
        self.play(FadeIn(answer, scale=1.2), run_time=0.5)
        self.wait(wait_time)
        
        self.play(FadeOut(VGroup(jee_badge, jee_box, question, steps, answer)), run_time=0.3)

    def segment_07_cta(self, timing):
        duration = timing['duration']
        self.add_cta_slide_physics(duration)