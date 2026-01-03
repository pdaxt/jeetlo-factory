"""
JeetLo Physics Reel: You've NEVER Touched Anything
===================================================
VIRAL CONCEPT: You've never touched anything in your entire life!
At the atomic level, electron clouds repel each other with electromagnetic force.
You're always floating 0.1 nanometers above everything.

Animation Focus:
- Hand reaching toward table - FREEZE - "This NEVER happens"
- Zoom to atomic level showing electron clouds
- Bouncer analogy for electromagnetic repulsion
- Repulsion force graph going exponential
- Mind-blow reveal: sitting, walking, phone - all floating!
- Formula F ~ 1/r^2
- JEE/NEET: Pauli Exclusion Principle
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
    from manim_edu.physics import FieldVisualizer
    from manim_edu.primitives.atoms import Atom
    from manim_edu.primitives.transitions import RippleEffect, PulseGlow
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
        data = json.load(f)
        # Filter out combined_audio entry
        return {t['id']: t for t in data if t['id'] != 'combined_audio'}


class PhysicsReel(JeetLoReelMixin, Scene):
    """Physics reel explaining electromagnetic repulsion - you've never touched anything!"""
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
        """Hook: You've never touched anything in your life! (6.912s)"""
        duration = timing['duration']

        # Animation timing
        total_anim_time = 0.5 + 0.6 + 0.4 + 0.5 + 0.4 + 0.3
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        # Create hand reaching toward table
        hand = VGroup()
        # Palm
        palm = RoundedRectangle(
            width=1.2, height=0.8, corner_radius=0.2,
            fill_color='#F5D0C5', fill_opacity=1, stroke_width=2, stroke_color='#D4A69A'
        )
        # Fingers
        for i in range(4):
            finger = RoundedRectangle(
                width=0.25, height=0.6, corner_radius=0.1,
                fill_color='#F5D0C5', fill_opacity=1, stroke_width=1, stroke_color='#D4A69A'
            )
            finger.next_to(palm, UP, buff=0.02)
            finger.shift(RIGHT * (i - 1.5) * 0.28)
            hand.add(finger)
        # Thumb
        thumb = RoundedRectangle(
            width=0.5, height=0.25, corner_radius=0.1,
            fill_color='#F5D0C5', fill_opacity=1, stroke_width=1, stroke_color='#D4A69A'
        )
        thumb.next_to(palm, LEFT, buff=0.02).shift(DOWN * 0.1)
        hand.add(palm, thumb)
        hand.move_to(UP * 2)

        # Table surface
        table = Rectangle(
            width=6, height=0.4, fill_color='#8B4513', fill_opacity=1,
            stroke_color='#5D2E0C', stroke_width=3
        )
        table.move_to(DOWN * 0.5)

        # Table top shine
        table_shine = Line(
            table.get_left() + UP * 0.15, table.get_right() + UP * 0.15,
            color='#A0522D', stroke_width=4
        )

        self.play(FadeIn(table), FadeIn(table_shine), run_time=0.5)
        self.play(FadeIn(hand, shift=DOWN), run_time=0.6)
        self.wait(wait_time)

        # Hand moves down toward table
        self.play(hand.animate.shift(DOWN * 1.8), run_time=0.4)

        # FREEZE - Big red X
        freeze_x = VGroup(
            Line(LEFT + UP, RIGHT + DOWN, color=RED, stroke_width=12),
            Line(LEFT + DOWN, RIGHT + UP, color=RED, stroke_width=12)
        ).scale(0.8).move_to(hand.get_center())

        never_text = Text("This NEVER happens", font_size=48, color=RED, weight=BOLD)
        never_text.move_to(UP * 4.5)

        self.play(Create(freeze_x), run_time=0.5)
        self.play(Write(never_text), run_time=0.4)
        self.wait(wait_time)

        # Show tiny gap
        gap_indicator = VGroup()
        gap_line1 = Line(ORIGIN, RIGHT * 0.5, color=YELLOW, stroke_width=3)
        gap_line2 = Line(ORIGIN, RIGHT * 0.5, color=YELLOW, stroke_width=3)
        gap_text = Text("0.1 nm gap!", font_size=28, color=YELLOW)
        gap_line1.next_to(hand, DOWN, buff=0.05)
        gap_line2.next_to(table, UP, buff=0.05)
        gap_text.next_to(gap_line1, RIGHT, buff=0.3)
        gap_indicator.add(gap_line1, gap_line2, gap_text)

        self.play(FadeIn(gap_indicator), run_time=0.3)
        self.wait(wait_time)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_02_setup(self, timing):
        """Setup: What happens at atomic level? (6.6s)"""
        duration = timing['duration']

        total_anim_time = 0.5 + 0.5 + 0.6 + 0.4 + 0.3
        num_waits = 3
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        # Title
        title = Text("Atomic Level", font_size=52, color=BLUE, weight=BOLD)
        title.move_to(UP * 5)

        self.play(Write(title), run_time=0.5)
        self.wait(wait_time)

        # Zoom effect - finger zooming in
        zoom_circle = Circle(radius=2, color=WHITE, stroke_width=3)
        zoom_circle.move_to(ORIGIN)

        # Inside zoom: show atoms
        finger_atom = VGroup()
        fa_core = Circle(radius=0.4, color=TEAL, fill_opacity=0.9, stroke_width=2)
        fa_label = Text("C", font_size=24, color=WHITE, weight=BOLD)
        fa_label.move_to(fa_core)
        finger_atom.add(fa_core, fa_label)
        finger_atom.move_to(LEFT * 1.2 + UP * 0.5)

        table_atom = VGroup()
        ta_core = Circle(radius=0.4, color=ORANGE, fill_opacity=0.9, stroke_width=2)
        ta_label = Text("Fe", font_size=24, color=WHITE, weight=BOLD)
        ta_label.move_to(ta_core)
        table_atom.add(ta_core, ta_label)
        table_atom.move_to(RIGHT * 1.2 + DOWN * 0.5)

        # Electron clouds (fuzzy spheres)
        cloud1 = Circle(radius=0.9, color=BLUE, fill_opacity=0.15, stroke_color=BLUE, stroke_width=2)
        cloud1.move_to(finger_atom.get_center())
        cloud2 = Circle(radius=0.9, color=BLUE, fill_opacity=0.15, stroke_color=BLUE, stroke_width=2)
        cloud2.move_to(table_atom.get_center())

        # Labels
        finger_label = Text("Finger atom", font_size=24, color=TEAL)
        finger_label.next_to(finger_atom, UP, buff=0.6)
        table_label = Text("Table atom", font_size=24, color=ORANGE)
        table_label.next_to(table_atom, DOWN, buff=0.6)

        self.play(Create(zoom_circle), run_time=0.5)
        self.play(
            FadeIn(finger_atom), FadeIn(table_atom),
            FadeIn(cloud1), FadeIn(cloud2),
            run_time=0.6
        )
        self.wait(wait_time)

        # Question mark
        question = Text("What happens here?", font_size=40, color=YELLOW, weight=BOLD)
        question.move_to(DOWN * 3.5)

        self.play(Write(question), run_time=0.4)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_03_content_part1(self, timing):
        """Content Part 1: Electron clouds repel like bouncers (15.096s)"""
        duration = timing['duration']

        total_anim_time = 0.5 + 0.6 + 0.8 + 0.5 + 0.6 + 0.5 + 0.6 + 0.5 + 0.5 + 0.3
        num_waits = 6
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        # Title
        title = Text("Electron Cloud Repulsion", font_size=44, color=TEAL, weight=BOLD)
        title.move_to(UP * 5.5)
        self.play(Write(title), run_time=0.5)

        # Two atoms approaching
        atom1_core = Circle(radius=0.35, color=TEAL, fill_opacity=0.9, stroke_width=2)
        atom1_label = Text("C", font_size=20, color=WHITE, weight=BOLD)
        atom1_label.move_to(atom1_core)
        atom1 = VGroup(atom1_core, atom1_label)
        atom1.move_to(LEFT * 3 + UP * 1.5)

        atom2_core = Circle(radius=0.35, color=ORANGE, fill_opacity=0.9, stroke_width=2)
        atom2_label = Text("Fe", font_size=20, color=WHITE, weight=BOLD)
        atom2_label.move_to(atom2_core)
        atom2 = VGroup(atom2_core, atom2_label)
        atom2.move_to(RIGHT * 3 + UP * 1.5)

        # Electron clouds with glow
        cloud1 = Circle(radius=1.0, color=BLUE, fill_opacity=0.15, stroke_color=BLUE, stroke_width=2)
        cloud1.move_to(atom1.get_center())
        cloud2 = Circle(radius=1.0, color=BLUE, fill_opacity=0.15, stroke_color=BLUE, stroke_width=2)
        cloud2.move_to(atom2.get_center())

        atoms_group = VGroup(atom1, cloud1, atom2, cloud2)

        self.play(FadeIn(atoms_group), run_time=0.6)
        self.wait(wait_time)

        # Move atoms closer - clouds start repelling
        self.play(
            atom1.animate.shift(RIGHT * 1.5),
            cloud1.animate.shift(RIGHT * 1.5),
            atom2.animate.shift(LEFT * 1.5),
            cloud2.animate.shift(LEFT * 1.5),
            run_time=0.8
        )
        self.wait(wait_time)

        # Show repulsion arrows between clouds
        repulsion_arrows = VGroup()
        for i in range(5):
            y_offset = (i - 2) * 0.4
            arrow1 = Arrow(
                cloud1.get_right() + UP * y_offset,
                cloud1.get_right() + LEFT * 0.5 + UP * y_offset,
                color=RED, stroke_width=3, buff=0
            )
            arrow2 = Arrow(
                cloud2.get_left() + UP * y_offset,
                cloud2.get_left() + RIGHT * 0.5 + UP * y_offset,
                color=RED, stroke_width=3, buff=0
            )
            repulsion_arrows.add(arrow1, arrow2)

        repulsion_label = Text("PUSH!", font_size=36, color=RED, weight=BOLD)
        repulsion_label.move_to(UP * 1.5)

        self.play(
            LaggedStart(*[Create(a) for a in repulsion_arrows], lag_ratio=0.05),
            run_time=0.5
        )
        self.play(Write(repulsion_label), run_time=0.6)
        self.wait(wait_time)

        # Clear atoms, show bouncer analogy
        self.play(FadeOut(atoms_group, repulsion_arrows, repulsion_label), run_time=0.5)

        # Bouncer analogy
        analogy_title = Text("Bouncer Analogy", font_size=40, color=GOLD, weight=BOLD)
        analogy_title.move_to(UP * 4)

        # Two bouncers (rectangles with arms)
        bouncer1 = VGroup()
        body1 = RoundedRectangle(width=1, height=1.8, corner_radius=0.2, fill_color='#2C3E50', fill_opacity=1)
        head1 = Circle(radius=0.35, fill_color='#F5D0C5', fill_opacity=1, stroke_width=1)
        head1.next_to(body1, UP, buff=-0.1)
        arm1 = Line(body1.get_right() + UP * 0.4, body1.get_right() + RIGHT * 0.8 + UP * 0.4, stroke_width=8, color='#F5D0C5')
        bouncer1.add(body1, head1, arm1)
        bouncer1.move_to(LEFT * 2 + DOWN * 0.5)

        bouncer2 = VGroup()
        body2 = RoundedRectangle(width=1, height=1.8, corner_radius=0.2, fill_color='#2C3E50', fill_opacity=1)
        head2 = Circle(radius=0.35, fill_color='#F5D0C5', fill_opacity=1, stroke_width=1)
        head2.next_to(body2, UP, buff=-0.1)
        arm2 = Line(body2.get_left() + UP * 0.4, body2.get_left() + LEFT * 0.8 + UP * 0.4, stroke_width=8, color='#F5D0C5')
        bouncer2.add(body2, head2, arm2)
        bouncer2.move_to(RIGHT * 2 + DOWN * 0.5)

        # Push effect in middle
        push_text = Text("PUSH", font_size=32, color=RED, weight=BOLD)
        push_text.move_to(DOWN * 0.5)

        # Club door
        door = Rectangle(width=0.8, height=2, fill_color='#8B0000', fill_opacity=0.8, stroke_color=GOLD, stroke_width=3)
        door.move_to(ORIGIN + DOWN * 0.5)

        self.play(Write(analogy_title), run_time=0.6)
        self.play(FadeIn(bouncer1, shift=RIGHT), FadeIn(bouncer2, shift=LEFT), run_time=0.5)
        self.wait(wait_time)

        self.play(FadeIn(door), Write(push_text), run_time=0.6)
        self.wait(wait_time)

        # Label: electrons same charge
        charge_text = Text("Same charge = REPEL", font_size=36, color=YELLOW, weight=BOLD)
        charge_text.move_to(DOWN * 3.5)
        self.play(Write(charge_text), run_time=0.5)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_03_content_part2(self, timing):
        """Content Part 2: Repulsion force increases exponentially (9.312s)"""
        duration = timing['duration']

        total_anim_time = 0.5 + 0.6 + 1.0 + 0.5 + 0.4 + 0.3
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        # Title
        title = Text("Repulsion Force", font_size=48, color=ORANGE, weight=BOLD)
        title.move_to(UP * 5.5)
        self.play(Write(title), run_time=0.5)

        # Create axes for graph
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=5,
            y_length=4,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=False
        ).move_to(LEFT * 0.5 + UP * 0.5)

        x_label = Text("Distance", font_size=24, color=WHITE)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("Force", font_size=24, color=WHITE)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3)

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=0.6)
        self.wait(wait_time)

        # Draw exponential curve (1/r^2 behavior, goes to infinity at small r)
        graph = axes.plot(
            lambda x: min(9.5, 0.5 / max(0.1, x - 0.3)**2) if x > 0.35 else 9.5,
            x_range=[0.4, 5],
            color=RED,
            stroke_width=4
        )

        self.play(Create(graph), run_time=1.0)
        self.wait(wait_time)

        # Label the curve going vertical
        infinite_label = Text("INFINITE WALL", font_size=32, color=RED, weight=BOLD)
        infinite_label.move_to(RIGHT * 2 + UP * 2)

        arrow_to_curve = Arrow(
            infinite_label.get_left(), axes.c2p(0.5, 8),
            color=YELLOW, stroke_width=3
        )

        self.play(Write(infinite_label), Create(arrow_to_curve), run_time=0.5)
        self.wait(wait_time)

        # Distance label
        distance_text = Text("10^-10 meters", font_size=36, color=TEAL, weight=BOLD)
        distance_text.move_to(DOWN * 3)
        self.play(Write(distance_text), run_time=0.4)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_04_reveal(self, timing):
        """Reveal: You're floating 0.1 nanometer above EVERYTHING (11.808s)"""
        duration = timing['duration']

        total_anim_time = 0.5 + 0.6 + 0.5 + 0.5 + 0.5 + 0.5 + 0.6 + 0.3
        num_waits = 5
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        # Big reveal text
        reveal_text = Text("YOU'RE FLOATING!", font_size=56, color=GOLD, weight=BOLD)
        reveal_text.move_to(UP * 5)

        self.play(Write(reveal_text), run_time=0.5)
        self.wait(wait_time)

        # Person sitting on chair
        # Chair
        chair_seat = Rectangle(width=1.5, height=0.2, fill_color='#8B4513', fill_opacity=1)
        chair_back = Rectangle(width=0.15, height=1.2, fill_color='#8B4513', fill_opacity=1)
        chair_back.next_to(chair_seat, LEFT, buff=0).shift(UP * 0.5)
        chair_legs = VGroup(
            Line(chair_seat.get_corner(DL), chair_seat.get_corner(DL) + DOWN * 0.8),
            Line(chair_seat.get_corner(DR), chair_seat.get_corner(DR) + DOWN * 0.8)
        ).set_color('#8B4513').set_stroke(width=5)
        chair = VGroup(chair_seat, chair_back, chair_legs)
        chair.move_to(LEFT * 2 + DOWN * 1)

        # Stick figure person
        person_head = Circle(radius=0.25, fill_color='#F5D0C5', fill_opacity=1, stroke_width=2)
        person_body = Line(ORIGIN, DOWN * 0.8, stroke_width=5, color='#333333')
        person_legs = VGroup(
            Line(ORIGIN, DOWN * 0.5 + LEFT * 0.3, stroke_width=5, color='#333333'),
            Line(ORIGIN, DOWN * 0.5 + RIGHT * 0.3, stroke_width=5, color='#333333')
        )
        person_body.next_to(person_head, DOWN, buff=0)
        person_legs.move_to(person_body.get_end())

        person = VGroup(person_head, person_body, person_legs)
        person.move_to(chair_seat.get_center() + UP * 0.8)

        self.play(FadeIn(chair), FadeIn(person), run_time=0.6)
        self.wait(wait_time)

        # Gap indicator
        gap_line = DashedLine(
            chair_seat.get_top() + LEFT * 0.5,
            chair_seat.get_top() + RIGHT * 0.5,
            color=YELLOW, stroke_width=3, dash_length=0.1
        )
        gap_line.shift(UP * 0.1)

        gap_label = Text("0.1 nm", font_size=28, color=YELLOW, weight=BOLD)
        gap_label.next_to(gap_line, RIGHT, buff=0.2)

        self.play(Create(gap_line), Write(gap_label), run_time=0.5)
        self.wait(wait_time)

        # Walking person
        walking_person = VGroup()
        w_head = Circle(radius=0.2, fill_color='#F5D0C5', fill_opacity=1, stroke_width=2)
        w_body = Line(ORIGIN, DOWN * 0.6, stroke_width=4, color='#333333')
        w_leg1 = Line(ORIGIN, DOWN * 0.4 + LEFT * 0.2, stroke_width=4, color='#333333')
        w_leg2 = Line(ORIGIN, DOWN * 0.4 + RIGHT * 0.2, stroke_width=4, color='#333333')
        w_body.next_to(w_head, DOWN, buff=0)
        w_leg1.move_to(w_body.get_end())
        w_leg2.move_to(w_body.get_end())
        walking_person.add(w_head, w_body, w_leg1, w_leg2)
        walking_person.move_to(RIGHT * 2 + DOWN * 0.5)

        # Ground
        ground = Line(LEFT * 1 + DOWN * 1.5, RIGHT * 3.5 + DOWN * 1.5, color='#654321', stroke_width=6)

        walk_label = Text("Walking = Floating", font_size=28, color=TEAL, weight=BOLD)
        walk_label.next_to(walking_person, UP, buff=0.5)

        self.play(FadeIn(walking_person), FadeIn(ground), run_time=0.5)
        self.play(Write(walk_label), run_time=0.5)
        self.wait(wait_time)

        # Phone holding
        phone = RoundedRectangle(width=0.4, height=0.7, corner_radius=0.05, fill_color='#1a1a2e', fill_opacity=1, stroke_color=WHITE, stroke_width=2)
        phone.move_to(LEFT * 2 + DOWN * 3.5)
        phone_label = Text("Phone = Floating", font_size=28, color=PURPLE, weight=BOLD)
        phone_label.next_to(phone, RIGHT, buff=0.3)

        self.play(FadeIn(phone), Write(phone_label), run_time=0.5)
        self.wait(wait_time)

        # Mind blown finale
        mind_blown = Text("Never TRULY touched!", font_size=42, color=RED, weight=BOLD)
        mind_blown.move_to(DOWN * 5)

        self.play(Write(mind_blown), run_time=0.6)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_05_key_point(self, timing):
        """Key Point: Electromagnetic repulsion, F proportional to 1/r^2 (12.696s)"""
        duration = timing['duration']

        total_anim_time = 0.5 + 0.6 + 0.5 + 0.6 + 0.5 + 0.5 + 0.4 + 0.3
        num_waits = 5
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        # Title
        title = Text("KEY POINT", font_size=48, color=GOLD, weight=BOLD)
        title.move_to(UP * 5.5)
        self.play(Write(title), run_time=0.5)

        # Main concept box
        concept_box = RoundedRectangle(
            width=6.5, height=1.4, corner_radius=0.2,
            fill_color='#1a2744', fill_opacity=0.8,
            stroke_color=BLUE, stroke_width=3
        )
        concept_box.move_to(UP * 3)

        concept_text = Text("Electromagnetic Repulsion", font_size=36, color=TEAL, weight=BOLD)
        concept_text.move_to(concept_box.get_center())

        self.play(Create(concept_box), Write(concept_text), run_time=0.6)
        self.wait(wait_time)

        # Formula: F proportional to 1/r^2
        formula_text = Text("F  ~  1 / r", font_size=48, color=WHITE)
        formula_text.move_to(UP * 0.5)

        # Superscript 2
        superscript = Text("2", font_size=28, color=WHITE)
        superscript.next_to(formula_text, UR, buff=0.05).shift(DOWN * 0.3)

        formula_group = VGroup(formula_text, superscript)

        self.play(Write(formula_group), run_time=0.5)
        self.wait(wait_time)

        # Explanation
        explanation = VGroup(
            Text("Closer distance", font_size=32, color=YELLOW),
            Text("=", font_size=32, color=WHITE),
            Text("STRONGER pushback", font_size=32, color=RED, weight=BOLD)
        ).arrange(RIGHT, buff=0.3)
        explanation.move_to(DOWN * 1.5)

        self.play(Write(explanation), run_time=0.6)
        self.wait(wait_time)

        # Magnet analogy
        magnet_analogy = Text("Like same poles of magnets", font_size=34, color=PURPLE, weight=BOLD)
        magnet_analogy.move_to(DOWN * 3)

        # Two magnets pushing each other
        magnet1 = VGroup()
        m1_north = Rectangle(width=1, height=0.6, fill_color=RED, fill_opacity=0.9, stroke_width=2)
        m1_south = Rectangle(width=1, height=0.6, fill_color=BLUE, fill_opacity=0.9, stroke_width=2)
        m1_south.next_to(m1_north, LEFT, buff=0)
        m1_n_label = Text("N", font_size=24, color=WHITE, weight=BOLD).move_to(m1_north)
        m1_s_label = Text("S", font_size=24, color=WHITE, weight=BOLD).move_to(m1_south)
        magnet1.add(m1_north, m1_south, m1_n_label, m1_s_label)
        magnet1.move_to(LEFT * 2 + DOWN * 5)

        magnet2 = VGroup()
        m2_north = Rectangle(width=1, height=0.6, fill_color=RED, fill_opacity=0.9, stroke_width=2)
        m2_south = Rectangle(width=1, height=0.6, fill_color=BLUE, fill_opacity=0.9, stroke_width=2)
        m2_north.next_to(m2_south, LEFT, buff=0)
        m2_n_label = Text("N", font_size=24, color=WHITE, weight=BOLD).move_to(m2_north)
        m2_s_label = Text("S", font_size=24, color=WHITE, weight=BOLD).move_to(m2_south)
        magnet2.add(m2_north, m2_south, m2_n_label, m2_s_label)
        magnet2.move_to(RIGHT * 2 + DOWN * 5)

        # Repulsion arrows between magnets
        repel_arrow1 = Arrow(ORIGIN + DOWN * 5 + LEFT * 0.2, LEFT * 0.8 + DOWN * 5, color=YELLOW, stroke_width=4)
        repel_arrow2 = Arrow(ORIGIN + DOWN * 5 + RIGHT * 0.2, RIGHT * 0.8 + DOWN * 5, color=YELLOW, stroke_width=4)

        self.play(Write(magnet_analogy), run_time=0.5)
        self.play(FadeIn(magnet1), FadeIn(magnet2), run_time=0.5)
        self.play(Create(repel_arrow1), Create(repel_arrow2), run_time=0.4)
        self.wait(wait_time)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_06_exam_tip(self, timing):
        """Exam tip: JEE/NEET - Pauli Exclusion Principle (11.064s)"""
        duration = timing['duration']

        total_anim_time = 0.5 + 0.6 + 0.5 + 0.6 + 0.5 + 0.5 + 0.3
        num_waits = 5
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        # Exam badge
        exam_badge = RoundedRectangle(
            width=5, height=1, corner_radius=0.2,
            fill_color='#FF6B35', fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=2
        )
        exam_badge.move_to(UP * 5.5)

        exam_text = Text("JEE & NEET", font_size=40, color=WHITE, weight=BOLD)
        exam_text.move_to(exam_badge.get_center())

        self.play(FadeIn(exam_badge), Write(exam_text), run_time=0.5)

        # Principle name
        principle_box = RoundedRectangle(
            width=6.5, height=1.2, corner_radius=0.15,
            fill_color='#1a2744', fill_opacity=0.9,
            stroke_color=GOLD, stroke_width=3
        )
        principle_box.move_to(UP * 3)

        principle_text = Text("Pauli Exclusion Principle", font_size=38, color=GOLD, weight=BOLD)
        principle_text.move_to(principle_box.get_center())

        self.play(Create(principle_box), Write(principle_text), run_time=0.6)
        self.wait(wait_time)

        # Question format
        question_box = Rectangle(
            width=6.5, height=2, fill_color='#0d1117', fill_opacity=0.9,
            stroke_color=TEAL, stroke_width=2
        )
        question_box.move_to(UP * 0.3)

        question_text = Text("Why can't two electrons", font_size=30, color=WHITE)
        question_text2 = Text("be in the same state?", font_size=30, color=WHITE)
        question_group = VGroup(question_text, question_text2).arrange(DOWN, buff=0.2)
        question_group.move_to(question_box.get_center())

        self.play(Create(question_box), run_time=0.5)
        self.play(Write(question_group), run_time=0.6)
        self.wait(wait_time)

        # Answer
        answer_text = Text("SAME REASON!", font_size=42, color=YELLOW, weight=BOLD)
        answer_text.move_to(DOWN * 2)

        self.play(Write(answer_text), run_time=0.5)
        self.wait(wait_time)

        # Explanation
        explanation = Text("Electron clouds can't overlap", font_size=34, color=TEAL, weight=BOLD)
        explanation.move_to(DOWN * 3.5)

        self.play(Write(explanation), run_time=0.5)
        self.wait(wait_time)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(Group(*[m for m in self.mobjects if m != self.watermark])), run_time=0.3)

    def segment_07_cta(self, timing):
        """CTA: JeetLo Physics! - Use pre-built CTA slide (7.056s)"""
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
