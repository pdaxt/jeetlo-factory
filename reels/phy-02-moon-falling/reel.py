import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')
from manim import *
from jeetlo_style import JeetLoReelMixin, create_brand_watermark

from manim_edu.physics import FieldVisualizer, MechanicsSimulator
from manim_edu.primitives import TraceTrail, GrowingArrow

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

        earth = Circle(radius=1.2, color=BLUE, fill_opacity=0.8)
        earth.set_fill(BLUE, opacity=0.6)
        earth.move_to(DOWN * 1)

        moon = Circle(radius=0.3, color=GRAY, fill_opacity=0.9)
        moon.set_fill(WHITE, opacity=0.7)
        moon.move_to(UP * 4)

        gravity_arrow = Arrow(
            moon.get_center() + DOWN * 0.4,
            earth.get_center() + UP * 1.3,
            color=RED,
            stroke_width=4,
            buff=0.1
        )

        title = Text("FALLING... RIGHT NOW!", font_size=42, color=YELLOW)
        title.to_edge(UP, buff=0.8)

        wrong_text = Text("WRONG!", font_size=56, color=RED, weight=BOLD)
        wrong_text.move_to(UP * 2)

        self.play(FadeIn(earth), FadeIn(moon), run_time=0.8)
        self.play(Create(gravity_arrow), run_time=0.6)

        self.play(
            moon.animate.shift(DOWN * 0.15),
            rate_func=there_and_back,
            run_time=0.5
        )

        self.play(Write(wrong_text), run_time=0.5)
        self.wait(0.3)
        self.play(FadeOut(wrong_text), run_time=0.3)

        self.play(Write(title), run_time=0.6)

        self.play(
            moon.animate.shift(DOWN * 0.1),
            rate_func=there_and_back,
            run_time=0.4
        )

        critical_text = Text("JEE CRITICAL!", font_size=36, color=ORANGE)
        critical_text.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(critical_text, scale=1.2), run_time=0.5)

        remaining = duration - 4.5
        self.wait(max(0.1, remaining))

        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_02_setup(self, timing):
        duration = timing['duration']

        ground = Line(LEFT * 3.5, RIGHT * 0.5, color=GREEN, stroke_width=3)
        ground.move_to(DOWN * 3)

        tree_trunk = Rectangle(width=0.3, height=1.5, color=ORANGE, fill_opacity=0.8)
        tree_trunk.set_fill("#8B4513", opacity=0.9)
        tree_trunk.move_to(DOWN * 2.25 + LEFT * 1)

        tree_top = Circle(radius=0.8, color=GREEN, fill_opacity=0.8)
        tree_top.set_fill("#228B22", opacity=0.9)
        tree_top.move_to(DOWN * 1 + LEFT * 1)

        newton = VGroup(
            Circle(radius=0.25, color=WHITE, fill_opacity=0.8),
            Line(ORIGIN, DOWN * 0.8, color=WHITE, stroke_width=3),
            Line(DOWN * 0.8, DOWN * 1.2 + LEFT * 0.3, color=WHITE, stroke_width=3),
            Line(DOWN * 0.8, DOWN * 1.2 + RIGHT * 0.3, color=WHITE, stroke_width=3),
        )
        newton.move_to(DOWN * 2 + RIGHT * 0.5)

        apple = Circle(radius=0.12, color=RED, fill_opacity=1)
        apple.move_to(tree_top.get_center() + DOWN * 0.5 + RIGHT * 0.3)

        moon_small = Circle(radius=0.25, color=GRAY, fill_opacity=0.8)
        moon_small.move_to(UP * 4 + RIGHT * 2)

        thought_bubble = VGroup(
            RoundedRectangle(width=3, height=1.2, corner_radius=0.3, color=WHITE, fill_opacity=0.1),
            Circle(radius=0.1, color=WHITE, fill_opacity=0.3).move_to(DOWN * 0.8 + LEFT * 0.5),
            Circle(radius=0.15, color=WHITE, fill_opacity=0.3).move_to(DOWN * 0.5 + LEFT * 0.3),
        )
        thought_bubble.move_to(UP * 1.5 + RIGHT * 1.5)

        question = Text("If apple falls...\nwhy not Moon?", font_size=28, color=WHITE)
        question.move_to(thought_bubble[0].get_center())

        self.play(
            FadeIn(ground),
            FadeIn(tree_trunk),
            FadeIn(tree_top),
            FadeIn(newton),
            run_time=0.8
        )

        self.play(FadeIn(apple), run_time=0.3)
        self.play(
            apple.animate.move_to(ground.get_center() + UP * 0.2),
            run_time=0.6,
            rate_func=rate_functions.ease_in_quad
        )

        self.play(FadeIn(moon_small), run_time=0.4)

        self.play(FadeIn(thought_bubble), Write(question), run_time=1.0)

        question_mark = Text("?", font_size=72, color=YELLOW)
        question_mark.move_to(UP * 4 + LEFT * 2)
        self.play(Write(question_mark), run_time=0.4)

        remaining = duration - 4.5
        self.wait(max(0.1, remaining))

        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_03_content_part1(self, timing):
        duration = timing['duration']

        mountain = Polygon(
            LEFT * 3 + DOWN * 3,
            LEFT * 1 + UP * 2,
            RIGHT * 1 + DOWN * 3,
            color=GREEN,
            fill_opacity=0.6
        )
        mountain.set_fill("#2F4F4F", opacity=0.7)

        cannon_body = Rectangle(width=0.8, height=0.4, color=GRAY, fill_opacity=0.9)
        cannon_body.set_fill("#4A4A4A", opacity=1)
        cannon_body.move_to(LEFT * 1 + UP * 2.2)
        cannon_body.rotate(-20 * DEGREES)

        cannon_barrel = Rectangle(width=0.6, height=0.2, color=GRAY, fill_opacity=0.9)
        cannon_barrel.set_fill("#3A3A3A", opacity=1)
        cannon_barrel.next_to(cannon_body, RIGHT, buff=0)
        cannon_barrel.rotate(-20 * DEGREES, about_point=cannon_body.get_center())

        cannon = VGroup(cannon_body, cannon_barrel)

        earth_curve = Arc(radius=8, angle=PI/3, color=BLUE, stroke_width=3)
        earth_curve.move_to(DOWN * 6)

        title = Text("Newton's Cannon", font_size=40, color=YELLOW)
        title.to_edge(UP, buff=0.5)

        self.play(FadeIn(mountain), FadeIn(cannon), run_time=0.6)
        self.play(Write(title), run_time=0.5)

        ball1 = Circle(radius=0.15, color=ORANGE, fill_opacity=1)
        start_pos = cannon_barrel.get_right() + RIGHT * 0.2
        ball1.move_to(start_pos)

        path1 = ArcBetweenPoints(
            start_pos,
            start_pos + RIGHT * 1.5 + DOWN * 2,
            angle=-PI/4
        )

        label1 = Text("Slow", font_size=28, color=RED)
        label1.move_to(RIGHT * 2 + DOWN * 0.5)

        self.play(FadeIn(ball1), run_time=0.2)
        self.play(MoveAlongPath(ball1, path1), run_time=0.8)
        self.play(Write(label1), run_time=0.3)

        ball2 = Circle(radius=0.15, color=YELLOW, fill_opacity=1)
        ball2.move_to(start_pos)

        path2 = ArcBetweenPoints(
            start_pos,
            start_pos + RIGHT * 3 + DOWN * 2.5,
            angle=-PI/5
        )

        label2 = Text("Faster", font_size=28, color=YELLOW)
        label2.move_to(RIGHT * 3.5 + UP * 0.5)

        self.play(FadeIn(ball2), run_time=0.2)
        self.play(MoveAlongPath(ball2, path2), run_time=0.7)
        self.play(Write(label2), run_time=0.3)

        self.play(FadeIn(earth_curve), run_time=0.5)

        ball3 = Circle(radius=0.15, color=GREEN, fill_opacity=1)
        ball3.move_to(start_pos)

        path3 = ArcBetweenPoints(
            start_pos,
            start_pos + RIGHT * 2 + DOWN * 5,
            angle=-PI/2.5
        )

        label3 = Text("FAST - halfway!", font_size=28, color=GREEN)
        label3.move_to(DOWN * 2 + RIGHT * 1)

        self.play(FadeIn(ball3), run_time=0.2)
        self.play(MoveAlongPath(ball3, path3), run_time=1.0)
        self.play(Write(label3), run_time=0.4)

        remaining = duration - 6.0
        self.wait(max(0.1, remaining))

        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_03_content_part2(self, timing):
        duration = timing['duration']

        earth = Circle(radius=1.8, color=BLUE, fill_opacity=0.5)
        earth.set_fill(BLUE, opacity=0.4)
        earth.move_to(ORIGIN)

        earth_label = Text("Earth", font_size=24, color=WHITE)
        earth_label.move_to(earth.get_center())

        cannon = Triangle(color=GRAY, fill_opacity=0.8)
        cannon.scale(0.3)
        cannon.move_to(earth.point_at_angle(PI/2) + UP * 0.2)

        self.play(FadeIn(earth), Write(earth_label), FadeIn(cannon), run_time=0.8)

        ball = Circle(radius=0.2, color=GOLD, fill_opacity=1)
        ball.move_to(cannon.get_center() + UP * 0.3)

        orbit_path = Circle(radius=2.5, color=TEAL, stroke_width=2, stroke_opacity=0.5)

        title = Text("PERFECT Speed = ORBIT!", font_size=36, color=YELLOW)
        title.to_edge(UP, buff=0.5)

        self.play(FadeIn(ball), run_time=0.3)
        self.play(Write(title), run_time=0.5)
        self.play(Create(orbit_path), run_time=0.6)

        velocity_arrow = Arrow(
            ball.get_center(),
            ball.get_center() + RIGHT * 1.2,
            color=GREEN,
            stroke_width=4,
            buff=0
        )
        v_label = Text("v", font_size=24, color=GREEN)
        v_label.next_to(velocity_arrow, UP, buff=0.1)

        gravity_arrow = Arrow(
            ball.get_center(),
            ball.get_center() + DOWN * 0.8,
            color=RED,
            stroke_width=4,
            buff=0
        )
        g_label = Text("g", font_size=24, color=RED)
        g_label.next_to(gravity_arrow, LEFT, buff=0.1)

        self.play(Create(velocity_arrow), Write(v_label), run_time=0.4)
        self.play(Create(gravity_arrow), Write(g_label), run_time=0.4)

        self.play(
            FadeOut(velocity_arrow), FadeOut(v_label),
            FadeOut(gravity_arrow), FadeOut(g_label),
            run_time=0.3
        )

        angle_tracker = ValueTracker(PI/2)

        def update_ball(mob):
            angle = angle_tracker.get_value()
            mob.move_to(np.array([
                2.5 * np.cos(angle),
                2.5 * np.sin(angle),
                0
            ]))

        ball.add_updater(update_ball)

        self.play(
            angle_tracker.animate.set_value(PI/2 - 2*PI),
            run_time=3.0,
            rate_func=linear
        )

        ball.remove_updater(update_ball)

        moon = Circle(radius=0.25, color=GRAY, fill_opacity=0.9)
        moon.move_to(ball.get_center())

        self.play(Transform(ball, moon), run_time=0.4)

        orbit_text = Text("This is ORBIT!", font_size=32, color=TEAL)
        orbit_text.to_edge(DOWN, buff=1)
        self.play(Write(orbit_text), run_time=0.5)

        remaining = duration - 7.2
        self.wait(max(0.1, remaining))

        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_04_reveal(self, timing):
        duration = timing['duration']

        divider = Line(UP * 6, DOWN * 6, color=WHITE, stroke_width=2)

        left_title = Text("Person Falling", font_size=28, color=WHITE)
        left_title.move_to(LEFT * 2 + UP * 5)

        right_title = Text("Moon Falling", font_size=28, color=WHITE)
        right_title.move_to(RIGHT * 2 + UP * 5)

        ground_left = Line(LEFT * 4 + DOWN * 4, ORIGIN + DOWN * 4, color=GREEN, stroke_width=3)

        person = VGroup(
            Circle(radius=0.2, color=ORANGE, fill_opacity=0.8),
            Line(ORIGIN, DOWN * 0.6, color=ORANGE, stroke_width=3),
            Line(DOWN * 0.6, DOWN * 1 + LEFT * 0.2, color=ORANGE, stroke_width=3),
            Line(DOWN * 0.6, DOWN * 1 + RIGHT * 0.2, color=ORANGE, stroke_width=3),
        )
        person.move_to(LEFT * 2 + UP * 2)

        earth_right = Circle(radius=1.2, color=BLUE, fill_opacity=0.5)
        earth_right.move_to(RIGHT * 2 + DOWN * 2)

        moon = Circle(radius=0.25, color=GRAY, fill_opacity=0.9)
        moon.move_to(RIGHT * 2 + UP * 3)

        self.play(
            Create(divider),
            Write(left_title), Write(right_title),
            FadeIn(ground_left),
            FadeIn(person),
            FadeIn(earth_right), FadeIn(moon),
            run_time=1.0
        )

        fall_arrow_left = Arrow(
            person.get_center() + DOWN * 0.5,
            person.get_center() + DOWN * 1.5,
            color=RED,
            stroke_width=4
        )

        fall_arrow_right = Arrow(
            moon.get_center(),
            moon.get_center() + (earth_right.get_center() - moon.get_center()) * 0.4,
            color=RED,
            stroke_width=4
        )

        self.play(Create(fall_arrow_left), Create(fall_arrow_right), run_time=0.5)

        self.play(
            person.animate.shift(DOWN * 2),
            run_time=0.8
        )

        orbit_arc = Arc(
            radius=2.5,
            start_angle=PI/2,
            angle=-PI/2,
            color=TEAL,
            stroke_width=3
        )
        orbit_arc.move_to(RIGHT * 2 + DOWN * 0.5)

        self.play(
            moon.animate.move_to(RIGHT * 4 + DOWN * 0.5),
            Create(orbit_arc),
            run_time=1.0
        )

        both_fall = Text("Both are FALLING!", font_size=36, color=YELLOW)
        both_fall.move_to(UP * 3)
        self.play(Write(both_fall), run_time=0.5)

        difference = Text("Moon's speed = MISSES Earth!", font_size=30, color=GREEN)
        difference.move_to(DOWN * 5)
        self.play(Write(difference), run_time=0.6)

        reveal_text = Text("Orbit = Falling + MISSING!", font_size=40, color=GOLD)
        reveal_text.move_to(ORIGIN)

        box = SurroundingRectangle(reveal_text, color=GOLD, buff=0.3)

        self.play(
            FadeOut(both_fall), FadeOut(difference),
            Write(reveal_text), Create(box),
            run_time=0.8
        )

        remaining = duration - 5.2
        self.wait(max(0.1, remaining))

        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_05_key_point(self, timing):
        duration = timing['duration']

        title = Text("Orbital Velocity Formula", font_size=36, color=YELLOW)
        title.to_edge(UP, buff=0.8)

        v_text = Text("v", font_size=56, color=GREEN, slant=ITALIC)
        equals = Text("=", font_size=48, color=WHITE)
        sqrt_symbol = Text("√", font_size=56, color=WHITE)

        frac_line = Line(LEFT * 0.8, RIGHT * 0.8, color=WHITE, stroke_width=3)

        g_text = Text("G", font_size=40, color=ORANGE)
        m_text = Text("M", font_size=40, color=BLUE)

        r_text = Text("r", font_size=40, color=PURPLE, slant=ITALIC)

        numerator = VGroup(g_text, m_text).arrange(RIGHT, buff=0.1)
        fraction = VGroup(numerator, frac_line, r_text).arrange(DOWN, buff=0.15)

        formula = VGroup(v_text, equals, sqrt_symbol, fraction).arrange(RIGHT, buff=0.2)
        formula.move_to(UP * 1)

        self.play(Write(title), run_time=0.5)
        self.play(Write(formula), run_time=1.2)

        g_label = Text("G = Gravity constant", font_size=24, color=ORANGE)
        m_label = Text("M = Earth's mass", font_size=24, color=BLUE)
        r_label = Text("r = Distance from center", font_size=24, color=PURPLE)

        labels = VGroup(g_label, m_label, r_label).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        labels.move_to(DOWN * 1.5)

        self.play(Write(labels), run_time=0.8)

        speedometer = VGroup()
        arc = Arc(radius=1.2, start_angle=PI, angle=-PI, color=WHITE, stroke_width=3)
        speedometer.add(arc)

        for i, (label, color) in enumerate([("CRASH", RED), ("ORBIT", GREEN), ("ESCAPE", BLUE)]):
            angle = PI - i * PI/2.5
            pos = arc.get_center() + 1.5 * np.array([np.cos(angle), np.sin(angle), 0])
            text = Text(label, font_size=18, color=color)
            text.move_to(pos)
            speedometer.add(text)

        needle = Arrow(
            arc.get_center(),
            arc.get_center() + UP * 0.8 + LEFT * 0.3,
            color=YELLOW,
            stroke_width=4
        )
        speedometer.add(needle)
        speedometer.move_to(DOWN * 4 + RIGHT * 2)

        self.play(FadeIn(speedometer), run_time=0.6)

        goldilocks = Text("Goldilocks Speed = Perfect Orbit!", font_size=28, color=GOLD)
        goldilocks.move_to(DOWN * 5.5)
        self.play(Write(goldilocks), run_time=0.5)

        remaining = duration - 4.6
        self.wait(max(0.1, remaining))

        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_06_exam_tip(self, timing):
        duration = timing['duration']

        title = Text("JEE EXAM TIP!", font_size=42, color=RED)
        title.to_edge(UP, buff=0.5)

        box = SurroundingRectangle(title, color=RED, buff=0.2)

        self.play(Write(title), Create(box), run_time=0.5)

        tip_text = Text(
            "Orbital velocity depends on r",
            font_size=32,
            color=WHITE
        )
        tip_text.move_to(UP * 2)

        r_highlight = Text("r", font_size=40, color=PURPLE, slant=ITALIC)
        r_highlight.next_to(tip_text, RIGHT, buff=0.2)

        self.play(Write(tip_text), run_time=0.6)

        not_text = Text("NOT on satellite mass!", font_size=32, color=YELLOW)
        not_text.move_to(UP * 0.5)
        self.play(Write(not_text), run_time=0.5)

        common_mistake = Text("Common Mistake", font_size=36, color=RED)
        common_mistake.move_to(DOWN * 1)

        x_mark = Text("✗", font_size=72, color=RED)
        x_mark.move_to(DOWN * 2.5)

        wrong_thought = Text("mass affects orbit speed", font_size=28, color=GRAY)
        wrong_thought.move_to(DOWN * 3.5)

        strike = Line(
            wrong_thought.get_left() + LEFT * 0.2,
            wrong_thought.get_right() + RIGHT * 0.2,
            color=RED,
            stroke_width=4
        )

        self.play(Write(common_mistake), run_time=0.4)
        self.play(Write(x_mark), Write(wrong_thought), run_time=0.5)
        self.play(Create(strike), run_time=0.3)

        correct = Text("v = √(GM/r) - no 'm' of satellite!", font_size=28, color=GREEN)
        correct.move_to(DOWN * 5)

        check = Text("✓", font_size=48, color=GREEN)
        check.next_to(correct, LEFT, buff=0.3)

        self.play(Write(correct), Write(check), run_time=0.6)

        remaining = duration - 3.4
        self.wait(max(0.1, remaining))

        self.play(FadeOut(Group(*self.mobjects[1:])), run_time=0.3)

    def segment_07_cta(self, timing):
        duration = timing['duration']
        self.add_cta_slide_physics(duration)