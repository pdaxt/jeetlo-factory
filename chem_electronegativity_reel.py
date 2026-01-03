"""
Electronegativity Reel - Chemistry
==================================
Tug-of-war analogy for understanding electronegativity, bond polarity, and ionic vs covalent bonds.
"""

import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')
from manim import *
from jeetlo_style import JeetLoReelMixin, create_brand_watermark
import json
import numpy as np

# Import manim-edu components for chemistry
from manim_edu.chemistry import MoleculeBuilder
from manim_edu.formulas import Term, Op, Formula, Char, CharSeq


class ChemistryReel(JeetLoReelMixin, Scene):
    subject = "chemistry"

    def construct(self):
        self.camera.background_color = '#0A2F1F'
        self.add(create_brand_watermark())

        # Load timings from file
        with open('audio/timings.json') as f:
            self.timings = json.load(f)

        # Call each segment
        for seg in self.timings:
            method_name = f"segment_{seg['id']}"
            method = getattr(self, method_name, None)
            if method:
                method(seg)

    def create_atom_circle(self, element: str, color: str, radius: float = 0.5,
                            show_label: bool = True, electronegativity: float = None) -> VGroup:
        """Create a styled atom circle with optional EN value."""
        group = VGroup()

        # Outer glow
        glow = Circle(radius=radius * 1.3, color=color, fill_opacity=0.2, stroke_width=0)
        group.add(glow)

        # Main circle
        circle = Circle(radius=radius, color=color, fill_opacity=0.8, stroke_width=3)
        circle.set_stroke(color=WHITE, width=2)
        group.add(circle)

        # Element label
        if show_label:
            label = Text(element, font_size=36, color=WHITE, weight=BOLD)
            group.add(label)

        # Electronegativity value
        if electronegativity is not None:
            en_text = Text(f"{electronegativity}", font_size=20, color=YELLOW)
            en_text.next_to(circle, DOWN, buff=0.15)
            group.add(en_text)

        return group

    def create_wrestler(self, element: str, color: str, power: float,
                        direction: str = "right", scale: float = 1.0) -> VGroup:
        """Create a wrestler representation of an atom with power level."""
        group = VGroup()

        # Body (circle)
        body_radius = 0.4 * scale * (0.5 + power / 8)  # Size based on power
        body = Circle(radius=body_radius, color=color, fill_opacity=0.9, stroke_width=3)
        body.set_stroke(WHITE, width=2)
        group.add(body)

        # Element label
        label = Text(element, font_size=int(32 * scale), color=WHITE, weight=BOLD)
        label.move_to(body.get_center())
        group.add(label)

        # Arms (lines extending for tug-of-war)
        arm_dir = RIGHT if direction == "right" else LEFT
        arm = Line(
            body.get_center() + arm_dir * body_radius,
            body.get_center() + arm_dir * (body_radius + 0.4 * scale),
            color=color, stroke_width=4
        )
        group.add(arm)

        # Power label
        power_text = Text(f"{power}", font_size=int(24 * scale), color=YELLOW, weight=BOLD)
        power_text.next_to(body, UP, buff=0.15)
        group.add(power_text)

        return group

    def create_rope(self, start: np.ndarray, end: np.ndarray, color: str = "#8B4513") -> Line:
        """Create a tug-of-war rope."""
        rope = Line(start, end, color=color, stroke_width=8)
        return rope

    def create_electron_cloud(self, center: np.ndarray, width: float, height: float,
                               color: str = BLUE, shift_amount: float = 0) -> VGroup:
        """Create an electron cloud visualization."""
        group = VGroup()

        # Main cloud (ellipse)
        cloud = Ellipse(width=width, height=height, color=color, fill_opacity=0.4, stroke_width=2)
        cloud.move_to(center + RIGHT * shift_amount)
        group.add(cloud)

        # Electron dots
        for _ in range(4):
            dot = Dot(radius=0.06, color=WHITE)
            angle = np.random.uniform(0, 2 * PI)
            r = np.random.uniform(0.1, min(width, height) / 3)
            dot.move_to(center + RIGHT * shift_amount + np.array([r * np.cos(angle), r * np.sin(angle), 0]))
            group.add(dot)

        return group

    def segment_01_hook(self, timing):
        """Fluorine as the greediest element - menacing wrestler."""
        duration = timing['duration']

        # Animation times
        anim_times = [0.5, 0.4, 0.4, 0.5, 0.4, 0.4, 0.3]
        total_anim = sum(anim_times)
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        # Title
        title = Text("The GREEDIEST Element...", font_size=42, color=RED, weight=BOLD)
        title.move_to(UP * 5.5)

        # Fluorine - the champion wrestler
        fluorine = self.create_wrestler("F", RED, 4.0, "left", scale=1.8)
        fluorine.move_to(ORIGIN)

        # Championship belt
        belt_text = Text("MOST ELECTRONEGATIVE", font_size=20, color=GOLD, weight=BOLD)
        belt_bg = RoundedRectangle(width=4.5, height=0.6, corner_radius=0.1,
                                    fill_color=GOLD, fill_opacity=0.3, stroke_color=GOLD)
        belt = VGroup(belt_bg, belt_text)
        belt.next_to(fluorine, DOWN, buff=0.8)

        # Other atoms looking nervous (smaller, to the sides)
        h_atom = self.create_atom_circle("H", BLUE, radius=0.25)
        h_atom.move_to(LEFT * 2.5 + DOWN * 1.5)

        na_atom = self.create_atom_circle("Na", PURPLE, radius=0.3)
        na_atom.move_to(RIGHT * 2.5 + DOWN * 1.5)

        o_atom = self.create_atom_circle("O", RED, radius=0.3)
        o_atom.move_to(LEFT * 1 + DOWN * 2.5)

        # Electrons flying toward F
        electrons = VGroup()
        for i in range(6):
            e = Dot(radius=0.08, color=TEAL)
            angle = i * PI / 3
            e.move_to(np.array([2.5 * np.cos(angle), 2.5 * np.sin(angle), 0]))
            electrons.add(e)

        # Animations
        self.play(FadeIn(title), run_time=anim_times[0])
        self.wait(wait_time)

        self.play(FadeIn(fluorine, scale=0.5), run_time=anim_times[1])
        self.play(FadeIn(belt, shift=UP), run_time=anim_times[2])
        self.wait(wait_time)

        self.play(
            FadeIn(h_atom), FadeIn(na_atom), FadeIn(o_atom),
            run_time=anim_times[3]
        )

        self.play(FadeIn(electrons), run_time=anim_times[4])

        # Electrons fly toward fluorine
        self.play(
            *[e.animate.move_to(fluorine.get_center() + np.array([
                0.3 * np.cos(i * PI/3), 0.3 * np.sin(i * PI/3), 0
            ])) for i, e in enumerate(electrons)],
            run_time=anim_times[5]
        )
        self.wait(wait_time)

        # Fluorine flexes (pulse)
        self.play(fluorine.animate.scale(1.15), run_time=anim_times[6] / 2)
        self.play(fluorine.animate.scale(1/1.15), run_time=anim_times[6] / 2)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_02_setup(self, timing):
        """Tug-of-war concept introduction with electronegativity."""
        duration = timing['duration']

        anim_times = [0.5, 0.4, 0.5, 0.4, 0.4]
        total_anim = sum(anim_times)
        num_waits = 3
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        # Title
        title = Text("Tug of War for Electrons!", font_size=40, color=TEAL, weight=BOLD)
        title.move_to(UP * 5.5)

        # Two wrestlers facing each other
        wrestler1 = self.create_wrestler("A", BLUE, 2.5, "right", scale=1.2)
        wrestler1.move_to(LEFT * 2.5)

        wrestler2 = self.create_wrestler("B", GREEN, 3.5, "left", scale=1.2)
        wrestler2.move_to(RIGHT * 2.5)

        # Rope between them
        rope = self.create_rope(LEFT * 1.3, RIGHT * 1.3)

        # Electron on rope
        electron = Dot(radius=0.15, color=YELLOW)
        electron.move_to(ORIGIN)
        electron_label = Text("e-", font_size=20, color=WHITE)
        electron_label.next_to(electron, UP, buff=0.1)
        electron_group = VGroup(electron, electron_label)

        # Electronegativity label
        en_title = Text("ELECTRONEGATIVITY", font_size=32, color=GOLD, weight=BOLD)
        en_title.move_to(DOWN * 2.5)

        en_subtitle = Text("= Electron pulling power!", font_size=28, color=WHITE)
        en_subtitle.next_to(en_title, DOWN, buff=0.3)

        # Stronger pulls toward itself
        arrow = Arrow(ORIGIN, RIGHT * 0.8, color=GREEN, stroke_width=6)
        arrow.move_to(DOWN * 1)

        # Animations
        self.add(create_brand_watermark())

        self.play(FadeIn(title), run_time=anim_times[0])
        self.wait(wait_time)

        self.play(FadeIn(wrestler1), FadeIn(wrestler2), run_time=anim_times[1])
        self.play(Create(rope), FadeIn(electron_group), run_time=anim_times[2])
        self.wait(wait_time)

        # B pulls electron toward itself
        self.play(
            electron_group.animate.shift(RIGHT * 0.5),
            run_time=anim_times[3]
        )

        self.play(FadeIn(en_title), FadeIn(en_subtitle), run_time=anim_times[4])
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_03_content_part1(self, timing):
        """H-H bond - equal tug of war, non-polar."""
        duration = timing['duration']

        anim_times = [0.5, 0.5, 0.6, 0.5, 0.4, 0.4]
        total_anim = sum(anim_times)
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        # Title
        title = Text("H-H Bond: Equal Match!", font_size=38, color=BLUE, weight=BOLD)
        title.move_to(UP * 5.5)

        # Two hydrogen wrestlers (same size/power)
        h1 = self.create_wrestler("H", BLUE, 2.1, "right", scale=1.2)
        h1.move_to(LEFT * 2.5 + UP * 1)

        h2 = self.create_wrestler("H", BLUE, 2.1, "left", scale=1.2)
        h2.move_to(RIGHT * 2.5 + UP * 1)

        # Rope
        rope = self.create_rope(LEFT * 1.3 + UP * 1, RIGHT * 1.3 + UP * 1)

        # Electron cloud centered
        cloud = self.create_electron_cloud(UP * 1, width=2.0, height=1.0, color=TEAL, shift_amount=0)

        # Equal sign
        equal = Text("=", font_size=60, color=WHITE)
        equal.move_to(UP * 1)

        # Labels
        label_en = Text("EN: 2.1 = 2.1", font_size=28, color=YELLOW, weight=BOLD)
        label_en.move_to(DOWN * 1)

        result = Text("Electrons in MIDDLE!", font_size=32, color=TEAL, weight=BOLD)
        result.move_to(DOWN * 2)

        bond_type = Text("NON-POLAR BOND", font_size=36, color=GREEN, weight=BOLD)
        bond_type.move_to(DOWN * 3.5)

        fair = Text("Fair Sharing!", font_size=28, color=WHITE)
        fair.next_to(bond_type, DOWN, buff=0.3)

        # Animations
        self.add(create_brand_watermark())

        self.play(FadeIn(title), run_time=anim_times[0])
        self.wait(wait_time)

        self.play(FadeIn(h1), FadeIn(h2), run_time=anim_times[1])
        self.play(Create(rope), run_time=anim_times[2])
        self.wait(wait_time)

        self.play(FadeIn(cloud), run_time=anim_times[3])
        self.play(FadeIn(label_en), run_time=anim_times[4])
        self.wait(wait_time)

        self.play(FadeIn(result), FadeIn(bond_type), FadeIn(fair), run_time=anim_times[5])
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_03_content_part2(self, timing):
        """H-F bond - unfair match, polar covalent."""
        duration = timing['duration']

        anim_times = [0.5, 0.5, 0.6, 0.8, 0.5, 0.5, 0.4, 0.4]
        total_anim = sum(anim_times)
        num_waits = 5
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        # Title
        title = Text("H-F Bond: Unfair Match!", font_size=38, color=ORANGE, weight=BOLD)
        title.move_to(UP * 5.5)

        # Tiny H vs massive F
        h = self.create_wrestler("H", BLUE, 2.1, "right", scale=0.8)
        h.move_to(LEFT * 2.5 + UP * 1)

        f = self.create_wrestler("F", RED, 4.0, "left", scale=1.5)
        f.move_to(RIGHT * 2 + UP * 1)

        # Rope
        rope = self.create_rope(LEFT * 1.5 + UP * 1, RIGHT * 0.8 + UP * 1)

        # Electron cloud SHIFTED toward F
        cloud = self.create_electron_cloud(UP * 1, width=2.0, height=1.0, color=TEAL, shift_amount=0.8)

        # Partial charges
        delta_plus = Text("δ+", font_size=32, color=BLUE, weight=BOLD)
        delta_plus.next_to(h, DOWN, buff=0.5)

        delta_minus = Text("δ-", font_size=32, color=RED, weight=BOLD)
        delta_minus.next_to(f, DOWN, buff=0.5)

        # Dipole arrow
        dipole_arrow = Arrow(LEFT * 1.5 + DOWN * 0.5, RIGHT * 1 + DOWN * 0.5,
                             color=YELLOW, stroke_width=5)
        dipole_label = Text("Dipole Moment", font_size=24, color=YELLOW)
        dipole_label.next_to(dipole_arrow, DOWN, buff=0.15)

        # EN difference
        en_diff = Text("EN: 4.0 - 2.1 = 1.9", font_size=28, color=ORANGE, weight=BOLD)
        en_diff.move_to(DOWN * 2.5)

        # Result
        result = Text("POLAR COVALENT BOND", font_size=34, color=ORANGE, weight=BOLD)
        result.move_to(DOWN * 3.8)

        unfair = Text("Unfair Sharing!", font_size=26, color=WHITE)
        unfair.next_to(result, DOWN, buff=0.3)

        # Animations
        self.add(create_brand_watermark())

        self.play(FadeIn(title), run_time=anim_times[0])
        self.wait(wait_time)

        self.play(FadeIn(h), FadeIn(f), run_time=anim_times[1])
        self.play(Create(rope), run_time=anim_times[2])
        self.wait(wait_time)

        # F yanks the rope - electron cloud shifts
        self.play(
            FadeIn(cloud),
            h.animate.shift(RIGHT * 0.3),
            run_time=anim_times[3]
        )
        self.wait(wait_time)

        self.play(FadeIn(delta_plus), FadeIn(delta_minus), run_time=anim_times[4])
        self.play(Create(dipole_arrow), FadeIn(dipole_label), run_time=anim_times[5])
        self.wait(wait_time)

        self.play(FadeIn(en_diff), run_time=anim_times[6])
        self.play(FadeIn(result), FadeIn(unfair), run_time=anim_times[7])
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_03_content_part3(self, timing):
        """Na-F bond - complete robbery, ionic bond."""
        duration = timing['duration']

        anim_times = [0.5, 0.5, 0.8, 0.6, 0.5, 0.4]
        total_anim = sum(anim_times)
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        # Title
        title = Text("Na-F: Complete Robbery!", font_size=38, color=PURPLE, weight=BOLD)
        title.move_to(UP * 5.5)

        # Na wrestler (weak)
        na = self.create_wrestler("Na", PURPLE, 0.9, "right", scale=0.7)
        na.move_to(LEFT * 2.5 + UP * 1)

        # F wrestler (super strong)
        f = self.create_wrestler("F", RED, 4.0, "left", scale=1.6)
        f.move_to(RIGHT * 1.5 + UP * 1)

        # Electron being stolen
        electron = Dot(radius=0.15, color=YELLOW)
        electron.move_to(LEFT * 1.5 + UP * 1)

        # After stealing - charges
        na_ion = self.create_atom_circle("Na", PURPLE, radius=0.4)
        na_ion.move_to(LEFT * 2.5 + UP * 1)
        na_charge = Text("+1", font_size=28, color=BLUE, weight=BOLD)
        na_charge.next_to(na_ion, UR, buff=0.1)

        f_ion = self.create_atom_circle("F", RED, radius=0.6)
        f_ion.move_to(RIGHT * 1.5 + UP * 1)
        f_charge = Text("-1", font_size=28, color=RED, weight=BOLD)
        f_charge.next_to(f_ion, UR, buff=0.1)

        # Result labels
        transfer = Text("Complete Electron TRANSFER!", font_size=30, color=YELLOW, weight=BOLD)
        transfer.move_to(DOWN * 1.5)

        result = Text("IONIC BOND", font_size=40, color=PURPLE, weight=BOLD)
        result.move_to(DOWN * 3)

        stealing = Text("Not sharing... STEALING!", font_size=28, color=RED, weight=BOLD)
        stealing.next_to(result, DOWN, buff=0.3)

        # Animations
        self.add(create_brand_watermark())

        self.play(FadeIn(title), run_time=anim_times[0])
        self.wait(wait_time)

        self.play(FadeIn(na), FadeIn(f), FadeIn(electron), run_time=anim_times[1])
        self.wait(wait_time)

        # F steals the electron completely
        self.play(
            electron.animate.move_to(f.get_center()),
            na.animate.shift(LEFT * 0.5),
            run_time=anim_times[2]
        )

        # Transform to ions
        self.play(
            ReplacementTransform(na, na_ion),
            FadeIn(na_charge),
            ReplacementTransform(VGroup(f, electron), f_ion),
            FadeIn(f_charge),
            run_time=anim_times[3]
        )
        self.wait(wait_time)

        self.play(FadeIn(transfer), run_time=anim_times[4])
        self.play(FadeIn(result), FadeIn(stealing), run_time=anim_times[5])
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_04_reveal(self, timing):
        """The 1.7 threshold - relationship status analogy."""
        duration = timing['duration']

        anim_times = [0.5, 0.5, 0.5, 0.5, 0.4, 0.4]
        total_anim = sum(anim_times)
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        # Title
        title = Text("The MAGIC Number", font_size=42, color=GOLD, weight=BOLD)
        title.move_to(UP * 5.5)

        # Big 1.7
        magic_number = Text("1.7", font_size=120, color=GOLD, weight=BOLD)
        magic_number.move_to(UP * 2.5)

        # Glow around 1.7
        glow = Circle(radius=1.5, color=GOLD, fill_opacity=0.2, stroke_width=4)
        glow.move_to(magic_number.get_center())

        # Scale/spectrum
        scale_line = Line(LEFT * 3.5, RIGHT * 3.5, color=WHITE, stroke_width=4)
        scale_line.move_to(DOWN * 0.5)

        # Threshold marker
        threshold = Line(DOWN * 0.2, DOWN * 0.8, color=GOLD, stroke_width=6)
        threshold.move_to(DOWN * 0.5)
        threshold_label = Text("1.7", font_size=24, color=GOLD)
        threshold_label.next_to(threshold, DOWN, buff=0.15)

        # Left side - Covalent
        covalent_label = Text("COVALENT", font_size=28, color=GREEN, weight=BOLD)
        covalent_label.move_to(LEFT * 2 + DOWN * 1.5)
        sharing = Text("Sharing!", font_size=22, color=WHITE)
        sharing.next_to(covalent_label, DOWN, buff=0.2)

        # Right side - Ionic
        ionic_label = Text("IONIC", font_size=28, color=PURPLE, weight=BOLD)
        ionic_label.move_to(RIGHT * 2 + DOWN * 1.5)
        stealing = Text("Stealing!", font_size=22, color=WHITE)
        stealing.next_to(ionic_label, DOWN, buff=0.2)

        # Arrows
        cov_arrow = Arrow(LEFT * 2 + DOWN * 0.5, LEFT * 3 + DOWN * 0.5, color=GREEN, stroke_width=4)
        ion_arrow = Arrow(RIGHT * 2 + DOWN * 0.5, RIGHT * 3 + DOWN * 0.5, color=PURPLE, stroke_width=4)

        # Less than / Greater than
        less_than = Text("< 1.7", font_size=26, color=GREEN)
        less_than.move_to(LEFT * 2.5 + DOWN * 2.5)

        greater_than = Text("> 1.7", font_size=26, color=PURPLE)
        greater_than.move_to(RIGHT * 2.5 + DOWN * 2.5)

        # Animations
        self.add(create_brand_watermark())

        self.play(FadeIn(title), run_time=anim_times[0])
        self.wait(wait_time)

        self.play(FadeIn(magic_number, scale=0.5), FadeIn(glow), run_time=anim_times[1])
        self.wait(wait_time)

        self.play(Create(scale_line), run_time=anim_times[2])
        self.play(
            Create(threshold), FadeIn(threshold_label),
            run_time=anim_times[3]
        )
        self.wait(wait_time)

        self.play(
            FadeIn(covalent_label), FadeIn(sharing),
            FadeIn(ionic_label), FadeIn(stealing),
            Create(cov_arrow), Create(ion_arrow),
            run_time=anim_times[4]
        )

        self.play(FadeIn(less_than), FadeIn(greater_than), run_time=anim_times[5])
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_05_key_point(self, timing):
        """Simple rule - bigger difference = more polar."""
        duration = timing['duration']

        anim_times = [0.5, 0.5, 0.6, 0.5, 0.4, 0.4]
        total_anim = sum(anim_times)
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        # Title
        title = Text("Simple Rule", font_size=40, color=TEAL, weight=BOLD)
        title.move_to(UP * 5.5)

        # Main rule
        rule = Text("Bigger Difference = More Polar!", font_size=36, color=YELLOW, weight=BOLD)
        rule.move_to(UP * 3.5)

        # Polarity meter
        meter_bg = RoundedRectangle(width=6, height=0.8, corner_radius=0.2,
                                     fill_color=GRAY, fill_opacity=0.3, stroke_color=WHITE)
        meter_bg.move_to(UP * 1.5)

        # Gradient bar
        meter_fill = Rectangle(width=5.5, height=0.5)
        meter_fill.set_color([GREEN, YELLOW, ORANGE, RED])
        meter_fill.move_to(UP * 1.5)

        # Labels on meter
        low = Text("0", font_size=20, color=GREEN)
        low.next_to(meter_bg, LEFT, buff=0.1)

        high = Text("3.3", font_size=20, color=RED)
        high.next_to(meter_bg, RIGHT, buff=0.1)

        meter_title = Text("EN Difference", font_size=24, color=WHITE)
        meter_title.next_to(meter_bg, UP, buff=0.2)

        # Examples
        ex1_text = Text("Zero diff = Equal sharing", font_size=26, color=GREEN)
        ex1_text.move_to(DOWN * 0.5)

        ex2_text = Text("Big diff = Electrons SHIFTED", font_size=26, color=ORANGE)
        ex2_text.move_to(DOWN * 1.5)

        # Visual examples
        equal_atoms = VGroup(
            self.create_atom_circle("H", BLUE, 0.3),
            self.create_atom_circle("H", BLUE, 0.3)
        ).arrange(RIGHT, buff=0.5)
        equal_atoms.move_to(DOWN * 3 + LEFT * 2)
        equal_label = Text("H-H: 0", font_size=20, color=GREEN)
        equal_label.next_to(equal_atoms, DOWN, buff=0.2)

        unequal_atoms = VGroup(
            self.create_atom_circle("H", BLUE, 0.25),
            self.create_atom_circle("F", RED, 0.4)
        ).arrange(RIGHT, buff=0.3)
        unequal_atoms.move_to(DOWN * 3 + RIGHT * 2)
        unequal_label = Text("H-F: 1.9", font_size=20, color=ORANGE)
        unequal_label.next_to(unequal_atoms, DOWN, buff=0.2)

        # Animations
        self.add(create_brand_watermark())

        self.play(FadeIn(title), run_time=anim_times[0])
        self.wait(wait_time)

        self.play(FadeIn(rule, shift=DOWN), run_time=anim_times[1])
        self.wait(wait_time)

        self.play(
            FadeIn(meter_bg), FadeIn(meter_fill),
            FadeIn(low), FadeIn(high), FadeIn(meter_title),
            run_time=anim_times[2]
        )

        self.play(FadeIn(ex1_text), FadeIn(ex2_text), run_time=anim_times[3])
        self.wait(wait_time)

        self.play(
            FadeIn(equal_atoms), FadeIn(equal_label),
            FadeIn(unequal_atoms), FadeIn(unequal_label),
            run_time=anim_times[4]
        )
        self.wait(wait_time)

        # Pulse the rule
        self.play(rule.animate.scale(1.1).set_color(GOLD), run_time=anim_times[5] / 2)
        self.play(rule.animate.scale(1/1.1).set_color(YELLOW), run_time=anim_times[5] / 2)
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_06_exam_tip(self, timing):
        """JEE trap question - HF vs HCl polarity."""
        duration = timing['duration']

        anim_times = [0.5, 0.5, 0.6, 0.5, 0.6, 0.5, 0.4, 0.3]
        total_anim = sum(anim_times)
        num_waits = 5
        wait_time = max(0.1, (duration - total_anim) / num_waits)

        # Title - JEE TRAP
        title = Text("JEE TRAP Question!", font_size=40, color=RED, weight=BOLD)
        title.move_to(UP * 5.5)

        # Question
        question = Text("Which is more polar: HF or HCl?", font_size=32, color=WHITE, weight=BOLD)
        question.move_to(UP * 3.5)

        # HF calculation
        hf_box = RoundedRectangle(width=3.2, height=2.5, corner_radius=0.15,
                                   fill_color=ORANGE, fill_opacity=0.2, stroke_color=ORANGE)
        hf_box.move_to(LEFT * 2 + UP * 0.5)

        hf_title = Text("H-F", font_size=32, color=ORANGE, weight=BOLD)
        hf_title.move_to(LEFT * 2 + UP * 1.3)

        hf_calc = VGroup(
            Text("F: 4.0", font_size=24, color=WHITE),
            Text("H: 2.1", font_size=24, color=WHITE),
            Text("─────", font_size=24, color=WHITE),
            Text("Δ = 1.9", font_size=28, color=ORANGE, weight=BOLD)
        ).arrange(DOWN, buff=0.15)
        hf_calc.move_to(LEFT * 2 + DOWN * 0.3)

        # HCl calculation
        hcl_box = RoundedRectangle(width=3.2, height=2.5, corner_radius=0.15,
                                    fill_color=TEAL, fill_opacity=0.2, stroke_color=TEAL)
        hcl_box.move_to(RIGHT * 2 + UP * 0.5)

        hcl_title = Text("H-Cl", font_size=32, color=TEAL, weight=BOLD)
        hcl_title.move_to(RIGHT * 2 + UP * 1.3)

        hcl_calc = VGroup(
            Text("Cl: 3.0", font_size=24, color=WHITE),
            Text("H: 2.1", font_size=24, color=WHITE),
            Text("─────", font_size=24, color=WHITE),
            Text("Δ = 0.9", font_size=28, color=TEAL, weight=BOLD)
        ).arrange(DOWN, buff=0.15)
        hcl_calc.move_to(RIGHT * 2 + DOWN * 0.3)

        # Comparison
        vs = Text("VS", font_size=36, color=WHITE, weight=BOLD)
        vs.move_to(UP * 0.5)

        # Winner
        winner = Text("HF WINS! (1.9 > 0.9)", font_size=36, color=GOLD, weight=BOLD)
        winner.move_to(DOWN * 2.5)

        # Exam note
        exam_note = Text("This comes in exams!", font_size=28, color=RED, weight=BOLD)
        exam_note.move_to(DOWN * 4)

        # Animations
        self.add(create_brand_watermark())

        self.play(FadeIn(title), run_time=anim_times[0])
        self.wait(wait_time)

        self.play(FadeIn(question), run_time=anim_times[1])
        self.wait(wait_time)

        self.play(FadeIn(hf_box), FadeIn(hf_title), run_time=anim_times[2])
        self.play(FadeIn(hf_calc), run_time=anim_times[3])
        self.wait(wait_time)

        self.play(FadeIn(vs), run_time=anim_times[4] / 2)
        self.play(FadeIn(hcl_box), FadeIn(hcl_title), run_time=anim_times[4] / 2)
        self.play(FadeIn(hcl_calc), run_time=anim_times[5])
        self.wait(wait_time)

        self.play(FadeIn(winner, scale=1.2), run_time=anim_times[6])
        self.play(FadeIn(exam_note), run_time=anim_times[7])
        self.wait(wait_time)

        # Clear
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_07_cta(self, timing):
        """CTA slide using JeetLo branding."""
        duration = timing['duration']
        # Use the pre-built CTA from JeetLoReelMixin
        self.add_cta_slide_chem(duration)
