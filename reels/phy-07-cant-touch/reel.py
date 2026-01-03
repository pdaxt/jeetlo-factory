import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')
from manim import *
from jeetlo_style import JeetLoReelMixin, create_brand_watermark

# Import manim-edu components for physics
from manim_edu.physics import FieldVisualizer
from manim_edu.layout import SafeText, safe_title, safe_body


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
            if seg['id'] == 'combined_audio':
                continue
            method_name = f"segment_{seg['id']}"
            method = getattr(self, method_name, None)
            if method:
                method(seg)

    def segment_01_hook(self, timing):
        duration = timing['duration']

        # Hook: Hand reaching toward table - freeze moment
        title = SafeText("You've NEVER touched ANYTHING", font_size=42, color=RED, weight=BOLD)
        title.move_to(UP * 4)

        subtitle = SafeText("Your entire life...", font_size=36, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.5)

        # Create hand and table visualization
        hand = VGroup()
        # Simplified hand shape
        palm = RoundedRectangle(width=1.5, height=2, corner_radius=0.2, color=ORANGE, fill_opacity=0.8)
        fingers = VGroup(*[
            RoundedRectangle(width=0.3, height=0.8, corner_radius=0.1, color=ORANGE, fill_opacity=0.8)
            for _ in range(4)
        ])
        fingers.arrange(RIGHT, buff=0.05)
        fingers.next_to(palm, UP, buff=0)
        thumb = RoundedRectangle(width=0.3, height=0.6, corner_radius=0.1, color=ORANGE, fill_opacity=0.8)
        thumb.next_to(palm, LEFT, buff=0).shift(UP * 0.3)
        hand.add(palm, fingers, thumb)
        hand.move_to(UP * 0.5)

        # Table surface
        table = Rectangle(width=6, height=0.3, color=TEAL, fill_opacity=0.9)
        table.move_to(DOWN * 1.5)

        # Gap indicator
        gap_line = DashedLine(
            hand.get_bottom() + DOWN * 0.1,
            table.get_top() + UP * 0.1,
            color=YELLOW,
            dash_length=0.1
        )

        big_x = SafeText("X", font_size=120, color=RED, weight=BOLD)
        big_x.move_to(RIGHT * 2 + UP * 0.5)

        never_text = SafeText("NEVER happens!", font_size=32, color=RED)
        never_text.next_to(big_x, DOWN, buff=0.3)

        # Timing calculation
        total_anim_time = 0.5 + 0.4 + 0.5 + 0.3 + 0.4 + 0.3
        num_waits = 3
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(subtitle), run_time=0.4)
        self.wait(wait_time)

        self.play(FadeIn(hand), FadeIn(table), run_time=0.5)
        self.play(Create(gap_line), run_time=0.3)
        self.wait(wait_time)

        self.play(FadeIn(big_x, scale=1.5), run_time=0.4)
        self.play(Write(never_text), run_time=0.3)
        self.wait(wait_time)

        self.play(*[FadeOut(m) for m in self.mobjects if m != self.mobjects[0]])

    def segment_02_setup(self, timing):
        duration = timing['duration']

        # Zoom into atomic level
        title = SafeText("At the ATOMIC level...", font_size=40, color=TEAL, weight=BOLD)
        title.move_to(UP * 5)

        question = SafeText("What ACTUALLY happens?", font_size=36, color=YELLOW)
        question.next_to(title, DOWN, buff=0.5)

        # Create two atoms approaching
        atom1 = VGroup()
        nucleus1 = Circle(radius=0.3, color=RED, fill_opacity=0.9)
        cloud1 = Circle(radius=1.0, color=BLUE, fill_opacity=0.2, stroke_opacity=0.5)
        atom1.add(cloud1, nucleus1)
        atom1.move_to(LEFT * 2.5)

        atom2 = VGroup()
        nucleus2 = Circle(radius=0.3, color=RED, fill_opacity=0.9)
        cloud2 = Circle(radius=1.0, color=BLUE, fill_opacity=0.2, stroke_opacity=0.5)
        atom2.add(cloud2, nucleus2)
        atom2.move_to(RIGHT * 2.5)

        label1 = SafeText("Finger atom", font_size=24, color=ORANGE)
        label1.next_to(atom1, DOWN, buff=0.3)

        label2 = SafeText("Table atom", font_size=24, color=TEAL)
        label2.next_to(atom2, DOWN, buff=0.3)

        zoom_text = SafeText("ZOOM IN", font_size=32, color=WHITE)
        zoom_text.move_to(DOWN * 4)

        # Timing
        total_anim_time = 0.4 + 0.3 + 0.5 + 0.4 + 0.5 + 0.3
        num_waits = 3
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.play(Write(title), run_time=0.4)
        self.play(Write(question), run_time=0.3)
        self.wait(wait_time)

        self.play(FadeIn(atom1), FadeIn(atom2), run_time=0.5)
        self.play(Write(label1), Write(label2), run_time=0.4)
        self.wait(wait_time)

        self.play(Write(zoom_text), run_time=0.5)
        # Move atoms closer
        self.play(
            atom1.animate.shift(RIGHT * 0.8),
            atom2.animate.shift(LEFT * 0.8),
            label1.animate.shift(RIGHT * 0.8),
            label2.animate.shift(LEFT * 0.8),
            run_time=0.3
        )
        self.wait(wait_time)

        self.play(*[FadeOut(m) for m in self.mobjects if m != self.mobjects[0]])

    def segment_03_content_part1(self, timing):
        duration = timing['duration']

        # Electron clouds repelling like bouncers
        title = SafeText("Electron Clouds REPEL", font_size=38, color=YELLOW, weight=BOLD)
        title.move_to(UP * 5)

        # Two atoms with electron clouds
        atom1 = VGroup()
        nucleus1 = Circle(radius=0.25, color=RED, fill_opacity=0.9)
        cloud1 = Circle(radius=0.9, color=BLUE, fill_opacity=0.25, stroke_color=BLUE, stroke_width=3)
        atom1.add(cloud1, nucleus1)
        atom1.move_to(LEFT * 1.8 + UP * 1)

        atom2 = VGroup()
        nucleus2 = Circle(radius=0.25, color=RED, fill_opacity=0.9)
        cloud2 = Circle(radius=0.9, color=BLUE, fill_opacity=0.25, stroke_color=BLUE, stroke_width=3)
        atom2.add(cloud2, nucleus2)
        atom2.move_to(RIGHT * 1.8 + UP * 1)

        # Repulsion arrows
        repel_arrow1 = Arrow(
            start=atom1.get_right() + LEFT * 0.2,
            end=atom1.get_right() + LEFT * 1.2,
            color=YELLOW,
            buff=0,
            stroke_width=6
        )
        repel_arrow2 = Arrow(
            start=atom2.get_left() + RIGHT * 0.2,
            end=atom2.get_left() + RIGHT * 1.2,
            color=YELLOW,
            buff=0,
            stroke_width=6
        )

        repel_label = SafeText("PUSH!", font_size=36, color=YELLOW, weight=BOLD)
        repel_label.move_to(UP * 1)

        # Bouncer analogy section
        bouncer_title = SafeText("Like Club Bouncers", font_size=32, color=ORANGE)
        bouncer_title.move_to(DOWN * 1.5)

        # Two bouncers (stick figures)
        bouncer1 = VGroup()
        b1_head = Circle(radius=0.2, color=ORANGE, fill_opacity=0.8)
        b1_body = Line(b1_head.get_bottom(), b1_head.get_bottom() + DOWN * 0.6, color=ORANGE, stroke_width=5)
        b1_arms = Line(LEFT * 0.4, RIGHT * 0.4, color=ORANGE, stroke_width=5)
        b1_arms.move_to(b1_body.get_center() + UP * 0.1)
        bouncer1.add(b1_head, b1_body, b1_arms)
        bouncer1.move_to(LEFT * 1.5 + DOWN * 3)

        bouncer2 = VGroup()
        b2_head = Circle(radius=0.2, color=ORANGE, fill_opacity=0.8)
        b2_body = Line(b2_head.get_bottom(), b2_head.get_bottom() + DOWN * 0.6, color=ORANGE, stroke_width=5)
        b2_arms = Line(LEFT * 0.4, RIGHT * 0.4, color=ORANGE, stroke_width=5)
        b2_arms.move_to(b2_body.get_center() + UP * 0.1)
        bouncer2.add(b2_head, b2_body, b2_arms)
        bouncer2.move_to(RIGHT * 1.5 + DOWN * 3)

        no_entry = SafeText("NO ENTRY!", font_size=28, color=RED, weight=BOLD)
        no_entry.move_to(DOWN * 3)

        same_charge = SafeText("Same charge = REPEL", font_size=30, color=TEAL)
        same_charge.move_to(DOWN * 5)

        # Timing
        total_anim_time = 0.5 + 0.5 + 0.4 + 0.4 + 0.5 + 0.4 + 0.5 + 0.4 + 0.4 + 0.4
        num_waits = 5
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(atom1), FadeIn(atom2), run_time=0.5)
        self.wait(wait_time)

        # Atoms approach
        self.play(
            atom1.animate.shift(RIGHT * 0.5),
            atom2.animate.shift(LEFT * 0.5),
            run_time=0.4
        )

        self.play(Create(repel_arrow1), Create(repel_arrow2), run_time=0.4)
        self.play(FadeIn(repel_label, scale=1.3), run_time=0.5)
        self.wait(wait_time)

        # Bouncer analogy
        self.play(Write(bouncer_title), run_time=0.4)
        self.play(FadeIn(bouncer1), FadeIn(bouncer2), run_time=0.5)
        self.wait(wait_time)

        self.play(
            bouncer1.animate.shift(RIGHT * 0.3),
            bouncer2.animate.shift(LEFT * 0.3),
            run_time=0.4
        )
        self.play(FadeIn(no_entry, scale=1.2), run_time=0.4)
        self.wait(wait_time)

        self.play(Write(same_charge), run_time=0.4)
        self.wait(wait_time)

        self.play(*[FadeOut(m) for m in self.mobjects if m != self.mobjects[0]])

    def segment_03_content_part2(self, timing):
        duration = timing['duration']

        # Exponential force graph
        title = SafeText("Force vs Distance", font_size=38, color=TEAL, weight=BOLD)
        title.move_to(UP * 5)

        # Create axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=5,
            y_length=4,
            axis_config={"color": WHITE, "include_tip": True},
        ).move_to(UP * 0.5)

        x_label = SafeText("Distance", font_size=24, color=WHITE)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)

        y_label = SafeText("Force", font_size=24, color=WHITE)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3)

        # Exponential curve (1/r^2 behavior)
        curve = axes.plot(
            lambda x: 1 / (x + 0.1) ** 2 if x > 0.05 else 100,
            x_range=[0.3, 4.5],
            color=YELLOW,
            stroke_width=4
        )

        # Annotation for steep rise
        steep_label = SafeText("SKYROCKETS!", font_size=28, color=RED, weight=BOLD)
        steep_label.move_to(LEFT * 1 + UP * 2.5)

        arrow_steep = Arrow(
            steep_label.get_bottom(),
            axes.c2p(0.5, 4),
            color=RED,
            buff=0.1
        )

        # Distance annotation
        distance_text = SafeText("10^-10 meters", font_size=32, color=ORANGE)
        distance_text.move_to(DOWN * 2.5)

        wall_text = SafeText("= INFINITE WALL", font_size=36, color=RED, weight=BOLD)
        wall_text.next_to(distance_text, DOWN, buff=0.3)

        # Timing
        total_anim_time = 0.4 + 0.5 + 0.5 + 0.4 + 0.4 + 0.4 + 0.4
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.play(Write(title), run_time=0.4)
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=0.5)
        self.wait(wait_time)

        self.play(Create(curve), run_time=0.5)
        self.wait(wait_time)

        self.play(Write(steep_label), run_time=0.4)
        self.play(Create(arrow_steep), run_time=0.4)
        self.wait(wait_time)

        self.play(Write(distance_text), run_time=0.4)
        self.play(FadeIn(wall_text, scale=1.2), run_time=0.4)
        self.wait(wait_time)

        self.play(*[FadeOut(m) for m in self.mobjects if m != self.mobjects[0]])

    def segment_04_reveal(self, timing):
        duration = timing['duration']

        # Mind-blowing reveal
        title = SafeText("You're FLOATING", font_size=44, color=YELLOW, weight=BOLD)
        title.move_to(UP * 5)

        distance = SafeText("0.1 nanometers above EVERYTHING", font_size=32, color=TEAL)
        distance.next_to(title, DOWN, buff=0.4)

        # Person sitting on chair - with gap
        chair = VGroup()
        seat = Rectangle(width=1.5, height=0.2, color=ORANGE, fill_opacity=0.8)
        back = Rectangle(width=0.2, height=1.2, color=ORANGE, fill_opacity=0.8)
        back.next_to(seat, UP, buff=0).align_to(seat, LEFT)
        legs = VGroup(
            Line(seat.get_corner(DL), seat.get_corner(DL) + DOWN * 0.8, color=ORANGE, stroke_width=4),
            Line(seat.get_corner(DR), seat.get_corner(DR) + DOWN * 0.8, color=ORANGE, stroke_width=4)
        )
        chair.add(seat, back, legs)
        chair.move_to(LEFT * 2.5 + DOWN * 1)

        # Stick figure person (floating above chair)
        person = VGroup()
        head = Circle(radius=0.2, color=BLUE, fill_opacity=0.8)
        body = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.8, color=BLUE, stroke_width=5)
        person.add(head, body)
        person.next_to(seat, UP, buff=0.15)  # Gap!

        float_label1 = SafeText("FLOATING!", font_size=24, color=YELLOW)
        float_label1.next_to(person, RIGHT, buff=0.3)

        # Walking person
        walker = VGroup()
        w_head = Circle(radius=0.2, color=GREEN, fill_opacity=0.8)
        w_body = Line(w_head.get_bottom(), w_head.get_bottom() + DOWN * 0.8, color=GREEN, stroke_width=5)
        walker.add(w_head, w_body)
        walker.move_to(RIGHT * 0.5 + DOWN * 0.5)

        ground = Line(LEFT * 1, RIGHT * 2, color=TEAL, stroke_width=3)
        ground.move_to(RIGHT * 0.5 + DOWN * 1.4)

        float_label2 = SafeText("FLOATING!", font_size=24, color=YELLOW)
        float_label2.next_to(walker, RIGHT, buff=0.3)

        # Phone holding
        phone = Rectangle(width=0.5, height=0.9, color=PURPLE, fill_opacity=0.8)
        phone.move_to(RIGHT * 3 + DOWN * 0.5)

        hand_rect = Rectangle(width=0.8, height=0.4, color=ORANGE, fill_opacity=0.7)
        hand_rect.next_to(phone, DOWN, buff=0.08)  # Gap!

        float_label3 = SafeText("FLOATING!", font_size=24, color=YELLOW)
        float_label3.next_to(phone, UP, buff=0.3)

        # Final revelation
        never_touched = SafeText("You've NEVER truly touched anything!", font_size=32, color=RED, weight=BOLD)
        never_touched.move_to(DOWN * 4)

        # Timing
        total_anim_time = 0.5 + 0.4 + 0.5 + 0.3 + 0.5 + 0.3 + 0.5 + 0.3 + 0.5
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.play(Write(title), run_time=0.5)
        self.play(Write(distance), run_time=0.4)
        self.wait(wait_time)

        self.play(FadeIn(chair), FadeIn(person), run_time=0.5)
        self.play(Write(float_label1), run_time=0.3)
        self.wait(wait_time)

        self.play(FadeIn(walker), Create(ground), run_time=0.5)
        self.play(Write(float_label2), run_time=0.3)
        self.wait(wait_time)

        self.play(FadeIn(phone), FadeIn(hand_rect), run_time=0.5)
        self.play(Write(float_label3), run_time=0.3)
        self.wait(wait_time)

        self.play(FadeIn(never_touched, scale=1.2), run_time=0.5)

        self.play(*[FadeOut(m) for m in self.mobjects if m != self.mobjects[0]])

    def segment_05_key_point(self, timing):
        duration = timing['duration']

        # Key point: Electromagnetic repulsion
        title = SafeText("KEY CONCEPT", font_size=40, color=ORANGE, weight=BOLD)
        title.move_to(UP * 5)

        concept = SafeText("Electromagnetic Repulsion", font_size=36, color=YELLOW)
        concept.next_to(title, DOWN, buff=0.5)

        # Formula display
        formula_text = SafeText("F ~ 1/r^2", font_size=48, color=WHITE, weight=BOLD)
        formula_text.move_to(UP * 1.5)

        explanation = SafeText("Closer = STRONGER pushback", font_size=30, color=TEAL)
        explanation.next_to(formula_text, DOWN, buff=0.4)

        # Magnet analogy
        magnet_title = SafeText("Like magnets:", font_size=28, color=WHITE)
        magnet_title.move_to(DOWN * 1)

        # Two magnets with same poles
        magnet1 = VGroup()
        m1_n = Rectangle(width=0.8, height=0.5, color=RED, fill_opacity=0.9)
        m1_n_label = SafeText("N", font_size=20, color=WHITE).move_to(m1_n)
        m1_s = Rectangle(width=0.8, height=0.5, color=BLUE, fill_opacity=0.9)
        m1_s.next_to(m1_n, LEFT, buff=0)
        m1_s_label = SafeText("S", font_size=20, color=WHITE).move_to(m1_s)
        magnet1.add(m1_s, m1_n, m1_s_label, m1_n_label)
        magnet1.move_to(LEFT * 2 + DOWN * 2.5)

        magnet2 = VGroup()
        m2_n = Rectangle(width=0.8, height=0.5, color=RED, fill_opacity=0.9)
        m2_n_label = SafeText("N", font_size=20, color=WHITE).move_to(m2_n)
        m2_s = Rectangle(width=0.8, height=0.5, color=BLUE, fill_opacity=0.9)
        m2_s.next_to(m2_n, RIGHT, buff=0)
        m2_s_label = SafeText("S", font_size=20, color=WHITE).move_to(m2_s)
        magnet2.add(m2_n, m2_s, m2_n_label, m2_s_label)
        magnet2.move_to(RIGHT * 2 + DOWN * 2.5)

        repel_arrows = VGroup(
            Arrow(magnet1.get_right(), magnet1.get_right() + LEFT * 0.8, color=YELLOW, buff=0.1),
            Arrow(magnet2.get_left(), magnet2.get_left() + RIGHT * 0.8, color=YELLOW, buff=0.1)
        )

        never_touch_label = SafeText("NEVER TOUCH", font_size=28, color=RED, weight=BOLD)
        never_touch_label.move_to(DOWN * 4.5)

        # Timing
        total_anim_time = 0.4 + 0.4 + 0.5 + 0.4 + 0.4 + 0.5 + 0.4 + 0.4
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.play(Write(title), run_time=0.4)
        self.play(Write(concept), run_time=0.4)
        self.wait(wait_time)

        self.play(FadeIn(formula_text, scale=1.2), run_time=0.5)
        self.play(Write(explanation), run_time=0.4)
        self.wait(wait_time)

        self.play(Write(magnet_title), run_time=0.4)
        self.play(FadeIn(magnet1), FadeIn(magnet2), run_time=0.5)
        self.wait(wait_time)

        self.play(Create(repel_arrows[0]), Create(repel_arrows[1]), run_time=0.4)
        self.play(Write(never_touch_label), run_time=0.4)
        self.wait(wait_time)

        self.play(*[FadeOut(m) for m in self.mobjects if m != self.mobjects[0]])

    def segment_06_exam_tip(self, timing):
        duration = timing['duration']

        # Exam connection
        title = SafeText("JEE & NEET", font_size=44, color=GOLD, weight=BOLD)
        title.move_to(UP * 5)

        principle = SafeText("Pauli Exclusion Principle", font_size=36, color=YELLOW)
        principle.next_to(title, DOWN, buff=0.5)

        # Question format
        question_box = RoundedRectangle(
            width=6, height=2.5, corner_radius=0.2,
            color=TEAL, fill_opacity=0.2, stroke_width=3
        )
        question_box.move_to(UP * 0.5)

        q_text = SafeText("Why can't 2 electrons occupy", font_size=26, color=WHITE)
        q_text2 = SafeText("the SAME quantum state?", font_size=26, color=WHITE)
        q_group = VGroup(q_text, q_text2).arrange(DOWN, buff=0.2)
        q_group.move_to(question_box)

        # Answer
        answer = SafeText("SAME REASON!", font_size=32, color=GREEN, weight=BOLD)
        answer.move_to(DOWN * 1.8)

        explanation = SafeText("Electron clouds can't overlap", font_size=28, color=TEAL)
        explanation.next_to(answer, DOWN, buff=0.3)

        # Visual: Two electrons repelling
        e1 = VGroup()
        e1_circle = Circle(radius=0.3, color=BLUE, fill_opacity=0.8)
        e1_minus = SafeText("-", font_size=30, color=WHITE)
        e1_minus.move_to(e1_circle)
        e1.add(e1_circle, e1_minus)
        e1.move_to(LEFT * 1.5 + DOWN * 4)

        e2 = VGroup()
        e2_circle = Circle(radius=0.3, color=BLUE, fill_opacity=0.8)
        e2_minus = SafeText("-", font_size=30, color=WHITE)
        e2_minus.move_to(e2_circle)
        e2.add(e2_circle, e2_minus)
        e2.move_to(RIGHT * 1.5 + DOWN * 4)

        repel_symbol = SafeText("<-->", font_size=36, color=RED)
        repel_symbol.move_to(DOWN * 4)

        # Timing
        total_anim_time = 0.4 + 0.4 + 0.5 + 0.4 + 0.4 + 0.4 + 0.5 + 0.4
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.play(Write(title), run_time=0.4)
        self.play(Write(principle), run_time=0.4)
        self.wait(wait_time)

        self.play(Create(question_box), run_time=0.5)
        self.play(Write(q_group), run_time=0.4)
        self.wait(wait_time)

        self.play(FadeIn(answer, scale=1.2), run_time=0.4)
        self.play(Write(explanation), run_time=0.4)
        self.wait(wait_time)

        self.play(FadeIn(e1), FadeIn(e2), run_time=0.5)
        self.play(Write(repel_symbol), run_time=0.4)
        self.wait(wait_time)

        self.play(*[FadeOut(m) for m in self.mobjects if m != self.mobjects[0]])

    def segment_07_cta(self, timing):
        duration = timing['duration']
        self.add_cta_slide_physics(duration)