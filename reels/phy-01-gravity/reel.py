import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')
from manim import *
from jeetlo_style import JeetLoReelMixin, create_brand_watermark

from manim_edu.physics import FieldVisualizer, MechanicsSimulator
from manim_edu.formulas import Formula, Term, Op, Frac, FormulaRenderer

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

        # Person sitting - simple stick figure on couch
        couch = RoundedRectangle(width=2.5, height=0.8, corner_radius=0.2, color=ORANGE, fill_opacity=0.8)
        couch.move_to(DOWN * 0.5)

        # Stick figure
        head = Circle(radius=0.25, color=WHITE, fill_opacity=1).move_to(UP * 1.2)
        body = Line(UP * 0.95, DOWN * 0.1, color=WHITE, stroke_width=4)
        arms = Line(LEFT * 0.5 + UP * 0.6, RIGHT * 0.5 + UP * 0.6, color=WHITE, stroke_width=4)
        legs = VGroup(
            Line(DOWN * 0.1, DOWN * 0.5 + LEFT * 0.3, color=WHITE, stroke_width=4),
            Line(DOWN * 0.1, DOWN * 0.5 + RIGHT * 0.3, color=WHITE, stroke_width=4)
        )
        person = VGroup(head, body, arms, legs)

        # Earth below
        earth = Circle(radius=2.5, color=BLUE, fill_opacity=0.6).move_to(DOWN * 5)
        earth_label = Text("EARTH", font_size=36, color=WHITE, weight=BOLD).move_to(DOWN * 5)

        # Big red arrow pointing down
        fall_arrow = Arrow(UP * 2.5, DOWN * 1.5, color=RED, stroke_width=8, buff=0)

        # Text
        hook_text = Text("You're FALLING right now!", font_size=42, color=YELLOW, weight=BOLD)
        hook_text.move_to(UP * 4)

        total_anim = 0.5 + 0.4 + 0.5 + 0.5 + 0.3
        num_waits = 3
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        self.play(FadeIn(couch), FadeIn(person), run_time=0.5)
        self.wait(wait_time)
        self.play(FadeIn(earth), FadeIn(earth_label), run_time=0.4)
        self.play(Create(fall_arrow), run_time=0.5)
        self.wait(wait_time)
        self.play(Write(hook_text), run_time=0.5)
        self.wait(wait_time)
        self.play(FadeOut(VGroup(couch, person, earth, earth_label, fall_arrow, hook_text)), run_time=0.3)

    def segment_02_setup(self, timing):
        duration = timing['duration']

        # Left side - Apple falling
        tree = VGroup(
            Rectangle(width=0.3, height=1.5, color=ORANGE, fill_opacity=0.8).move_to(LEFT * 2.5 + DOWN * 1),
            Circle(radius=1, color=GREEN, fill_opacity=0.7).move_to(LEFT * 2.5 + UP * 0.5)
        )
        apple = Circle(radius=0.2, color=RED, fill_opacity=1).move_to(LEFT * 2.5 + UP * 0.3)

        # Right side - Moon orbiting Earth
        small_earth = Circle(radius=0.6, color=BLUE, fill_opacity=0.7).move_to(RIGHT * 2.5)
        moon = Circle(radius=0.2, color=GRAY, fill_opacity=0.8).move_to(RIGHT * 2.5 + UP * 1.5)
        orbit_path = Circle(radius=1.5, color=WHITE, stroke_opacity=0.3).move_to(RIGHT * 2.5)

        # Question mark in center
        question = Text("?", font_size=80, color=YELLOW, weight=BOLD).move_to(ORIGIN + UP * 0.5)

        # Labels
        left_label = Text("Apple Falls", font_size=28, color=WHITE).move_to(LEFT * 2.5 + DOWN * 3)
        right_label = Text("Moon Orbits", font_size=28, color=WHITE).move_to(RIGHT * 2.5 + DOWN * 3)

        # Same force text
        same_force = Text("SAME FORCE!", font_size=48, color=GOLD, weight=BOLD).move_to(UP * 4)

        # Glowing thread connecting them
        thread = Line(LEFT * 2.5, RIGHT * 2.5, color=YELLOW, stroke_width=3)

        total_anim = 0.5 + 0.5 + 0.4 + 0.5 + 0.5 + 0.4 + 0.3
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        self.play(FadeIn(tree), run_time=0.5)
        self.play(apple.animate.move_to(LEFT * 2.5 + DOWN * 2), run_time=0.5)
        self.wait(wait_time)
        self.play(FadeIn(small_earth), FadeIn(orbit_path), FadeIn(moon), run_time=0.4)
        self.play(Write(left_label), Write(right_label), run_time=0.5)
        self.wait(wait_time)
        self.play(Write(question), run_time=0.5)
        self.wait(wait_time)
        self.play(Create(thread), Write(same_force), run_time=0.4)
        self.wait(wait_time)
        self.play(FadeOut(VGroup(tree, apple, small_earth, moon, orbit_path, question, left_label, right_label, same_force, thread)), run_time=0.3)

    def segment_03_content_part1(self, timing):
        duration = timing['duration']

        # Earth as clingy ex - cartoon face on Earth
        earth = Circle(radius=1.5, color=BLUE, fill_opacity=0.7).move_to(LEFT * 2 + DOWN * 1)
        # Eyes
        left_eye = Circle(radius=0.15, color=WHITE, fill_opacity=1).move_to(LEFT * 2.3 + DOWN * 0.7)
        right_eye = Circle(radius=0.15, color=WHITE, fill_opacity=1).move_to(LEFT * 1.7 + DOWN * 0.7)
        left_pupil = Circle(radius=0.07, color=BLACK, fill_opacity=1).move_to(LEFT * 2.3 + DOWN * 0.7)
        right_pupil = Circle(radius=0.07, color=BLACK, fill_opacity=1).move_to(LEFT * 1.7 + DOWN * 0.7)
        # Grabby hands
        left_hand = VGroup(
            Line(LEFT * 3.5 + DOWN * 1, LEFT * 3 + DOWN * 0.5, color=ORANGE, stroke_width=4),
            Line(LEFT * 3 + DOWN * 0.5, LEFT * 2.8 + DOWN * 0.3, color=ORANGE, stroke_width=3),
            Line(LEFT * 3 + DOWN * 0.5, LEFT * 2.9 + DOWN * 0.2, color=ORANGE, stroke_width=3),
        )
        right_hand = VGroup(
            Line(LEFT * 0.5 + DOWN * 1, LEFT * 1 + DOWN * 0.5, color=ORANGE, stroke_width=4),
            Line(LEFT * 1 + DOWN * 0.5, LEFT * 1.2 + DOWN * 0.3, color=ORANGE, stroke_width=3),
        )

        clingy_earth = VGroup(earth, left_eye, right_eye, left_pupil, right_pupil, left_hand, right_hand)

        # Title
        title = Text("CLINGY EX = GRAVITY", font_size=36, color=YELLOW, weight=BOLD).move_to(UP * 5)

        # Formula parts - using manim-edu
        formula_title = Text("F = G m1 m2 / r squared", font_size=32, color=WHITE).move_to(UP * 3)

        # Variable explanations
        g_label = Text("G = Universe's constant", font_size=24, color=TEAL).move_to(RIGHT * 1.5 + UP * 1.5)
        m_label = Text("m1 m2 = Mass (emotional baggage!)", font_size=22, color=PINK).move_to(RIGHT * 1 + UP * 0.5)
        r_label = Text("r squared = Distance squared", font_size=22, color=GREEN).move_to(RIGHT * 1 + DOWN * 0.5)
        weak_label = Text("Distance up = Grip DOWN!", font_size=24, color=RED).move_to(RIGHT * 1 + DOWN * 1.5)

        total_anim = 0.6 + 0.5 + 0.6 + 0.5 + 0.5 + 0.5 + 0.5 + 0.4
        num_waits = 5
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        self.play(FadeIn(clingy_earth), run_time=0.6)
        self.play(Write(title), run_time=0.5)
        self.wait(wait_time)
        self.play(Write(formula_title), run_time=0.6)
        self.wait(wait_time)
        self.play(Write(g_label), run_time=0.5)
        self.wait(wait_time)
        self.play(Write(m_label), run_time=0.5)
        self.wait(wait_time)
        self.play(Write(r_label), run_time=0.5)
        self.play(Write(weak_label), run_time=0.5)
        self.wait(wait_time)
        self.play(FadeOut(VGroup(clingy_earth, title, formula_title, g_label, m_label, r_label, weak_label)), run_time=0.4)

    def segment_03_content_part2(self, timing):
        duration = timing['duration']

        # Earth in center
        earth = Circle(radius=0.8, color=BLUE, fill_opacity=0.8).move_to(ORIGIN)
        earth_label = Text("Earth", font_size=24, color=WHITE).move_to(ORIGIN)

        # Field lines - spider web pattern
        field_lines = VGroup()
        for angle in range(0, 360, 30):
            rad = angle * PI / 180
            line = Line(
                ORIGIN,
                np.array([3.5 * np.cos(rad), 3.5 * np.sin(rad), 0]),
                color=PURPLE,
                stroke_width=2,
                stroke_opacity=0.6
            )
            field_lines.add(line)

        # Concentric circles for web effect
        web_circles = VGroup()
        for r in [1.2, 1.8, 2.5, 3.2]:
            circ = Circle(radius=r, color=PURPLE, stroke_width=1, stroke_opacity=0.4)
            web_circles.add(circ)

        # Person close - strong pull
        person_close = Circle(radius=0.2, color=ORANGE, fill_opacity=1).move_to(RIGHT * 1.5)
        close_label = Text("CLOSE = STRONG", font_size=24, color=RED, weight=BOLD).move_to(RIGHT * 1.5 + UP * 1)

        # Person far - weak pull
        person_far = Circle(radius=0.15, color=GREEN, fill_opacity=1).move_to(LEFT * 3 + UP * 2)
        far_label = Text("FAR = WEAK", font_size=24, color=GREEN).move_to(LEFT * 3 + UP * 3)

        # Title
        title = Text("Inverse Square Law", font_size=36, color=GOLD, weight=BOLD).move_to(UP * 5.5)

        total_anim = 0.5 + 0.6 + 0.5 + 0.5 + 0.5 + 0.5 + 0.3
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        self.play(FadeIn(earth), FadeIn(earth_label), run_time=0.5)
        self.play(LaggedStart(*[Create(line) for line in field_lines], lag_ratio=0.05), run_time=0.6)
        self.play(FadeIn(web_circles), run_time=0.5)
        self.wait(wait_time)
        self.play(FadeIn(person_close), Write(close_label), run_time=0.5)
        self.wait(wait_time)
        self.play(FadeIn(person_far), Write(far_label), run_time=0.5)
        self.wait(wait_time)
        self.play(Write(title), run_time=0.5)
        self.wait(wait_time)
        self.play(FadeOut(VGroup(earth, earth_label, field_lines, web_circles, person_close, close_label, person_far, far_label, title)), run_time=0.3)

    def segment_04_reveal(self, timing):
        duration = timing['duration']

        # Earth
        earth = Circle(radius=1.2, color=BLUE, fill_opacity=0.8).move_to(ORIGIN)
        earth_label = Text("Earth", font_size=28, color=WHITE).move_to(ORIGIN)

        # Moon
        moon = Circle(radius=0.3, color=GRAY, fill_opacity=0.9).move_to(RIGHT * 3 + UP * 1)

        # Orbit path
        orbit = Circle(radius=3.2, color=WHITE, stroke_width=2, stroke_opacity=0.4).move_to(ORIGIN)

        # Arrow showing Moon falling toward Earth
        fall_arrow = Arrow(RIGHT * 3 + UP * 1, RIGHT * 1.5 + DOWN * 0.5, color=RED, stroke_width=5, buff=0.1)
        fall_label = Text("FALLING!", font_size=28, color=RED, weight=BOLD).move_to(RIGHT * 2 + DOWN * 1.5)

        # Sideways motion arrow
        side_arrow = Arrow(RIGHT * 3 + UP * 1, RIGHT * 3.5 + UP * 2.5, color=GREEN, stroke_width=5, buff=0.1)
        side_label = Text("Moving sideways", font_size=24, color=GREEN).move_to(RIGHT * 2 + UP * 3.5)

        # Mind blow text
        mind_blow = Text("ORBIT = PERPETUAL FALLING!", font_size=32, color=YELLOW, weight=BOLD).move_to(UP * 5.5)

        # Miss text
        miss_text = Text("Keep MISSING the ground!", font_size=28, color=TEAL).move_to(DOWN * 4)

        total_anim = 0.5 + 0.4 + 0.5 + 0.5 + 0.5 + 0.6 + 0.5 + 0.4
        num_waits = 5
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        self.play(FadeIn(earth), FadeIn(earth_label), run_time=0.5)
        self.play(FadeIn(orbit), FadeIn(moon), run_time=0.4)
        self.wait(wait_time)
        self.play(Create(fall_arrow), run_time=0.5)
        self.play(Write(fall_label), run_time=0.5)
        self.wait(wait_time)
        self.play(Create(side_arrow), run_time=0.5)
        self.play(Write(side_label), run_time=0.6)
        self.wait(wait_time)
        self.play(Write(mind_blow), run_time=0.5)
        self.wait(wait_time)
        self.play(Write(miss_text), run_time=0.4)
        self.wait(wait_time)
        self.play(FadeOut(VGroup(earth, earth_label, orbit, moon, fall_arrow, fall_label, side_arrow, side_label, mind_blow, miss_text)), run_time=0.3)

    def segment_05_key_point(self, timing):
        duration = timing['duration']

        # Title
        title = Text("INVERSE SQUARE LAW", font_size=40, color=GOLD, weight=BOLD).move_to(UP * 5)

        # Visual demonstration
        # At 1x distance - 4 weights
        dist1_label = Text("Distance = 1R", font_size=28, color=WHITE).move_to(LEFT * 2 + UP * 2.5)
        weights_1x = VGroup(*[
            Square(side_length=0.5, color=RED, fill_opacity=0.8).move_to(LEFT * 2 + UP * 1 + RIGHT * i * 0.6)
            for i in range(4)
        ])
        force_1x = Text("Force = 4 units", font_size=24, color=RED).move_to(LEFT * 2 + DOWN * 0.5)

        # At 2x distance - 1 weight
        dist2_label = Text("Distance = 2R", font_size=28, color=WHITE).move_to(RIGHT * 2 + UP * 2.5)
        weight_2x = Square(side_length=0.5, color=GREEN, fill_opacity=0.8).move_to(RIGHT * 2 + UP * 1)
        force_2x = Text("Force = 1 unit", font_size=24, color=GREEN).move_to(RIGHT * 2 + DOWN * 0.5)

        # Arrow between them
        arrow = Arrow(LEFT * 0.5 + UP * 1, RIGHT * 0.8 + UP * 1, color=YELLOW, stroke_width=4)
        arrow_label = Text("2x distance = 1/4 force!", font_size=26, color=YELLOW, weight=BOLD).move_to(DOWN * 2.5)

        # Bottom emphasis
        square_it = Text("SQUARE that r!", font_size=36, color=TEAL, weight=BOLD).move_to(DOWN * 4.5)

        total_anim = 0.5 + 0.5 + 0.4 + 0.5 + 0.4 + 0.5 + 0.5 + 0.3
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        self.play(Write(title), run_time=0.5)
        self.wait(wait_time)
        self.play(Write(dist1_label), FadeIn(weights_1x), run_time=0.5)
        self.play(Write(force_1x), run_time=0.4)
        self.wait(wait_time)
        self.play(Write(dist2_label), FadeIn(weight_2x), run_time=0.5)
        self.play(Write(force_2x), run_time=0.4)
        self.wait(wait_time)
        self.play(Create(arrow), Write(arrow_label), run_time=0.5)
        self.play(Write(square_it), run_time=0.5)
        self.wait(wait_time)
        self.play(FadeOut(VGroup(title, dist1_label, weights_1x, force_1x, dist2_label, weight_2x, force_2x, arrow, arrow_label, square_it)), run_time=0.3)

    def segment_06_exam_tip(self, timing):
        duration = timing['duration']

        # JEE Question box
        jee_box = RoundedRectangle(width=7, height=2.5, corner_radius=0.2, color=PURPLE, fill_opacity=0.3)
        jee_box.move_to(UP * 3)
        jee_label = Text("JEE FAVOURITE", font_size=28, color=PURPLE, weight=BOLD).move_to(UP * 4.5)

        question = Text("Where is g = g0/4 ?", font_size=32, color=WHITE).move_to(UP * 3)

        # Answer box
        answer_box = RoundedRectangle(width=6, height=1.5, corner_radius=0.2, color=GREEN, fill_opacity=0.4)
        answer_box.move_to(UP * 0.5)
        answer = Text("r = 2R (One Earth radius above surface)", font_size=24, color=GREEN, weight=BOLD).move_to(UP * 0.5)

        # Common mistake
        mistake_box = RoundedRectangle(width=6, height=1.5, corner_radius=0.2, color=RED, fill_opacity=0.3)
        mistake_box.move_to(DOWN * 2)
        mistake_label = Text("COMMON MISTAKE", font_size=24, color=RED, weight=BOLD).move_to(DOWN * 1.3)
        mistake = Text("NOT 4R from center!", font_size=26, color=RED).move_to(DOWN * 2.3)

        # X mark
        x_mark = Text("X", font_size=60, color=RED, weight=BOLD).move_to(DOWN * 2 + RIGHT * 2.5)

        # Tip
        tip = Text("Height from surface, not from center!", font_size=22, color=YELLOW).move_to(DOWN * 4.5)

        total_anim = 0.4 + 0.5 + 0.5 + 0.5 + 0.5 + 0.4 + 0.4 + 0.3
        num_waits = 5
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        self.play(FadeIn(jee_box), Write(jee_label), run_time=0.4)
        self.play(Write(question), run_time=0.5)
        self.wait(wait_time)
        self.play(FadeIn(answer_box), Write(answer), run_time=0.5)
        self.wait(wait_time)
        self.play(FadeIn(mistake_box), Write(mistake_label), run_time=0.5)
        self.wait(wait_time)
        self.play(Write(mistake), run_time=0.5)
        self.play(FadeIn(x_mark), run_time=0.4)
        self.wait(wait_time)
        self.play(Write(tip), run_time=0.4)
        self.wait(wait_time)
        self.play(FadeOut(VGroup(jee_box, jee_label, question, answer_box, answer, mistake_box, mistake_label, mistake, x_mark, tip)), run_time=0.3)

    def segment_07_cta(self, timing):
        duration = timing['duration']
        self.add_cta_slide_physics(duration)