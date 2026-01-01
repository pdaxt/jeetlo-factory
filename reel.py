"""
JeetLo Chemistry Reel: Molarity - The REAL Understanding
=========================================================
CREATIVE BRIEF:
- Core Analogy: Molarity = Party crowd density. Room (1L) with guests (molecules).
  Rasna analogy - same powder, different water = different concentration!
- Visual Style: Volumetric flasks, animated molecules, formula builds
- Duration: ~103 seconds (7 segments)

Topic: Molarity - What it REALLY means!
Source: NCERT Class 11 Chemistry, Chapter on Solutions

KEY CONCEPT: M = n/V (moles per liter). Volume is the DENOMINATOR!
"""

import sys
sys.path.insert(0, '/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')

from jeetlo_style import *
from manim_edu.chemistry import MoleculeBuilder
from manim_edu.primitives.colors import SUBJECT_COLORS, ATOM_COLORS

import json
import os
import numpy as np

# Config for vertical reel (9:16)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8
config.frame_height = 14.22
config.background_color = "#0A2F1F"

# Color scheme - Chemistry (Green)
PRIMARY = "#00CC66"
CYAN = "#00FFFF"
YELLOW = "#FCD34D"
ORANGE = "#FF6B35"
PINK = "#FF69B4"
PURPLE = "#9B59B6"
BLUE = "#3498DB"
RED_ACCENT = "#FF4757"

# Molecule colors for variety
MOLECULE_COLORS = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD"]


def calc_wait(duration, anim_times, num_waits, buffer=0.2):
    """Calculate wait time to fill segment duration with buffer."""
    fixed_time = sum(anim_times) if isinstance(anim_times, list) else anim_times
    remaining = duration - fixed_time + buffer
    return max(0.1, remaining / num_waits)


class MolarityReel(JeetLoReelMixin, Scene):
    """Molarity reel with Rasna analogy and volumetric flask visuals."""

    subject = "chemistry"

    def construct(self):
        self.set_subject_background("chemistry")
        watermark = create_brand_watermark(opacity=0.6)
        self.add(watermark)

        timings = self.load_timings()

        # Run all 7 segments
        self.segment_01_hook(timings[0])
        self.segment_02_setup(timings[1])
        self.segment_03_content(timings[2])
        self.segment_04_reveal(timings[3])
        self.segment_05_key_point(timings[4])
        self.segment_06_exam_tip(timings[5])
        self.segment_07_cta(timings[6])

    def load_timings(self):
        """Load audio timings from JSON file."""
        try:
            timings_path = os.path.join(os.path.dirname(__file__), 'audio', 'timings.json')
            with open(timings_path, 'r') as f:
                return json.load(f)
        except:
            # Fallback timings from creative brief
            return [
                {'duration': 6.6, 'id': '01_hook'},
                {'duration': 10.104, 'id': '02_setup'},
                {'duration': 34.296, 'id': '03_content'},
                {'duration': 13.848, 'id': '04_reveal'},
                {'duration': 12.216, 'id': '05_key_point'},
                {'duration': 20.76, 'id': '06_exam_tip'},
                {'duration': 5.304, 'id': '07_cta'}
            ]

    # ========================================
    # SEGMENT 01: HOOK (6.6s)
    # ========================================
    def segment_01_hook(self, timing):
        """Hook: Molarity calculate karna aata hai? WRONG!"""
        duration = timing.get('duration', 6.6)
        anims = [0.3, 0.4, 0.5, 0.3, 0.5, 0.15, 0.15, 0.3]
        wait_time = calc_wait(duration, anims, 3)

        # Chemistry badge with glow
        badge = self.create_subject_badge("CHEMISTRY", PRIMARY)
        badge.to_edge(UP, buff=1.5)
        self.play(FadeIn(badge, scale=0.8), run_time=0.3)

        # Student confidently writing formula
        student_work = VGroup()
        formula_written = MathTex("M = \\frac{n}{V}", font_size=72, color=CYAN)
        formula_written.shift(UP * 0.5)

        # Checkmark first (confident student)
        check = Text("✓", font_size=64, color=CORRECT_GREEN)
        check.next_to(formula_written, RIGHT, buff=0.3)

        self.play(Write(formula_written), run_time=0.4)
        self.play(FadeIn(check), run_time=0.5)

        self.wait(wait_time)

        # Question appears
        question = Text("Is that ALL?", font_size=38, color=YELLOW)
        question.shift(DOWN * 1.2)
        self.play(Write(question), run_time=0.3)

        self.wait(wait_time)

        # WRONG buzzer effect
        wrong = Text("WRONG!", font_size=80, color=WRONG_RED, weight=BOLD)
        wrong.shift(DOWN * 3)

        # Remove checkmark with cross
        cross = Text("✗", font_size=64, color=WRONG_RED)
        cross.move_to(check.get_center())

        self.play(
            Transform(check, cross),
            FadeIn(wrong, scale=1.5),
            run_time=0.5
        )
        self.play(wrong.animate.scale(1.15), run_time=0.15)
        self.play(wrong.animate.scale(1/1.15), run_time=0.15)

        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects[1:]), run_time=0.3)

    # ========================================
    # SEGMENT 02: SETUP - Rasna Analogy (10.104s)
    # ========================================
    def segment_02_setup(self, timing):
        """Setup: Rasna analogy - same powder, different water = different taste!"""
        duration = timing.get('duration', 10.104)
        anims = [0.4, 0.6, 0.4, 0.5, 0.5, 0.4, 0.5, 0.4, 0.3]
        wait_time = calc_wait(duration, anims, 4)

        # Title
        title = Text("Think About This...", font_size=44, color=YELLOW, weight=BOLD)
        title.to_edge(UP, buff=1.8)
        self.play(Write(title), run_time=0.4)

        # Two glasses
        glass1 = self.create_glass(height=2.5, width=1.2)
        glass1.shift(LEFT * 2 + DOWN * 0.5)

        glass2 = self.create_glass(height=2.5, width=1.2)
        glass2.shift(RIGHT * 2 + DOWN * 0.5)

        self.play(
            DrawBorderThenFill(glass1),
            DrawBorderThenFill(glass2),
            run_time=0.6
        )

        # Same Rasna powder amount (dots)
        powder_label = Text("Same Rasna powder", font_size=26, color=ORANGE)
        powder_label.shift(UP * 2.2)
        self.play(Write(powder_label), run_time=0.4)

        # Powder dots falling into glasses
        powder1 = self.create_powder_dots().move_to(glass1.get_center() + DOWN * 0.3)
        powder2 = self.create_powder_dots().move_to(glass2.get_center() + DOWN * 0.3)

        self.play(
            FadeIn(powder1, shift=DOWN),
            FadeIn(powder2, shift=DOWN),
            run_time=0.5
        )

        self.wait(wait_time)

        # Fill with different water levels
        water1 = self.create_water_fill(glass1, fill_level=0.9, color="#3498DB")
        water2 = self.create_water_fill(glass2, fill_level=0.45, color="#3498DB")

        water_label1 = Text("More water", font_size=22, color=BLUE)
        water_label1.next_to(glass1, DOWN, buff=0.3)

        water_label2 = Text("Less water", font_size=22, color=BLUE)
        water_label2.next_to(glass2, DOWN, buff=0.3)

        self.play(
            GrowFromEdge(water1, DOWN),
            GrowFromEdge(water2, DOWN),
            Write(water_label1),
            Write(water_label2),
            run_time=0.5
        )

        self.wait(wait_time)

        # Question: Which is STRONGER?
        question = Text("Which is STRONGER?", font_size=40, color=YELLOW, weight=BOLD)
        question.shift(DOWN * 3.2)
        self.play(Write(question), run_time=0.4)

        # Arrow pointing to half-filled glass
        arrow = Arrow(
            start=RIGHT * 0.5 + DOWN * 3.5,
            end=RIGHT * 1.8 + DOWN * 2,
            color=PRIMARY, stroke_width=4
        )
        self.play(GrowArrow(arrow), run_time=0.5)

        self.wait(wait_time)

        # Answer reveal
        answer = Text("Less water = MORE concentrated!", font_size=32, color=PRIMARY, weight=BOLD)
        answer.shift(DOWN * 4.5)
        self.play(Write(answer), run_time=0.4)

        # Connection to molarity
        molarity_connect = Text("THIS is MOLARITY!", font_size=36, color=CYAN, weight=BOLD)
        molarity_connect.shift(DOWN * 5.3)
        self.play(Write(molarity_connect), run_time=0.3)

        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects[1:]), run_time=0.3)

    # ========================================
    # SEGMENT 03: CONTENT - Core Teaching (34.296s)
    # ========================================
    def segment_03_content(self, timing):
        """Main teaching: Flask visualization, 1M definition, formula build, real-world example."""
        duration = timing.get('duration', 34.296)
        # This is a long segment - divide into 3 scenes

        # Scene 1: 1 Molar definition (~10s)
        self.content_scene_1_molar_definition(duration * 0.30)

        # Scene 2: Half mole comparison (~10s)
        self.content_scene_2_half_mole(duration * 0.30)

        # Scene 3: Real-world IV drip (~14s)
        self.content_scene_3_real_world(duration * 0.40)

    def content_scene_1_molar_definition(self, duration):
        """Scene 1: One liter flask with molecules = 1 Molar"""
        anims = [0.4, 0.8, 1.5, 0.5, 0.5, 0.4, 0.3]
        wait_time = calc_wait(duration, anims, 3)

        # Title
        title = Text("What is 1 Molar?", font_size=44, color=PRIMARY, weight=BOLD)
        title.to_edge(UP, buff=1.6)
        self.play(Write(title), run_time=0.4)

        # Create volumetric flask
        flask = self.create_volumetric_flask(scale=1.2)
        flask.shift(UP * 0.3)
        self.play(DrawBorderThenFill(flask), run_time=0.8)

        # Label "1 Liter"
        liter_label = Text("1 Liter", font_size=32, color=CYAN, weight=BOLD)
        liter_label.next_to(flask, LEFT, buff=0.4)

        # Animate molecules raining into flask
        molecules = self.create_molecule_rain(count=20, target=flask.get_center())
        self.play(
            Write(liter_label),
            *[FadeIn(m, shift=DOWN * np.random.uniform(1, 2)) for m in molecules],
            run_time=1.5
        )

        self.wait(wait_time)

        # Counter showing Avogadro's number
        counter_box = RoundedRectangle(
            width=6.5, height=0.9, corner_radius=0.15,
            fill_color=YELLOW, fill_opacity=0.2,
            stroke_color=YELLOW, stroke_width=2
        )
        counter_box.shift(DOWN * 2.2)

        counter_text = MathTex(
            r"6.022 \times 10^{23}", r"\text{ particles}", r"= 1 \text{ mole}",
            font_size=34, color=YELLOW
        )
        counter_text.move_to(counter_box.get_center())

        self.play(Create(counter_box), Write(counter_text), run_time=0.5)

        self.wait(wait_time)

        # Result: 1 Molar
        result = Text("= 1 Molar (1M)", font_size=48, color=PRIMARY, weight=BOLD)
        result.shift(DOWN * 3.8)
        self.play(Write(result), run_time=0.5)

        # Highlight the concept
        concept_box = RoundedRectangle(
            width=6, height=1.1, corner_radius=0.2,
            fill_color=PRIMARY, fill_opacity=0.2,
            stroke_color=PRIMARY, stroke_width=3
        )
        concept_box.shift(DOWN * 5)
        concept_text = Text("1 mole in 1 liter = 1M", font_size=30, color=TEXT_WHITE, weight=BOLD)
        concept_text.move_to(concept_box.get_center())

        self.play(Create(concept_box), Write(concept_text), run_time=0.4)

        self.wait(wait_time)

        self.play(FadeOut(*self.mobjects[1:]), run_time=0.3)

    def content_scene_2_half_mole(self, duration):
        """Scene 2: Compare 1 mole vs 0.5 mole in same flask"""
        anims = [0.4, 0.6, 0.5, 0.5, 0.4, 0.6, 0.4, 0.3]
        wait_time = calc_wait(duration, anims, 3)

        # Two flasks side by side
        flask1 = self.create_volumetric_flask(scale=0.9)
        flask1.shift(LEFT * 2.2 + UP * 0.5)

        flask2 = self.create_volumetric_flask(scale=0.9)
        flask2.shift(RIGHT * 2.2 + UP * 0.5)

        self.play(
            DrawBorderThenFill(flask1),
            DrawBorderThenFill(flask2),
            run_time=0.4
        )

        # Labels
        label1 = Text("1 mole", font_size=26, color=CYAN, weight=BOLD)
        label1.next_to(flask1, UP, buff=0.2)

        label2 = Text("0.5 mole", font_size=26, color=ORANGE, weight=BOLD)
        label2.next_to(flask2, UP, buff=0.2)

        self.play(Write(label1), Write(label2), run_time=0.6)

        # Molecules in flask 1 (more crowded)
        molecules1 = self.create_molecule_cluster(count=18, spread=0.8)
        molecules1.move_to(flask1.get_center())

        # Molecules in flask 2 (less crowded)
        molecules2 = self.create_molecule_cluster(count=9, spread=0.8)
        molecules2.move_to(flask2.get_center())

        self.play(
            FadeIn(molecules1, scale=0.5),
            run_time=0.5
        )
        self.play(
            FadeIn(molecules2, scale=0.5),
            run_time=0.5
        )

        self.wait(wait_time)

        # Visual comparison
        comparison = Text("Less molecules = Less crowded!", font_size=30, color=YELLOW)
        comparison.shift(DOWN * 1.8)
        self.play(Write(comparison), run_time=0.4)

        # Molarity labels
        m_label1 = Text("1M", font_size=42, color=PRIMARY, weight=BOLD)
        m_label1.next_to(flask1, DOWN, buff=0.3)

        m_label2 = Text("0.5M", font_size=42, color=ORANGE, weight=BOLD)
        m_label2.next_to(flask2, DOWN, buff=0.3)

        self.play(Write(m_label1), Write(m_label2), run_time=0.6)

        self.wait(wait_time)

        # Formula build
        formula = MathTex(
            r"M = \frac{n}{V}",
            font_size=52, color=CYAN
        )
        formula.shift(DOWN * 3.5)
        self.play(Write(formula), run_time=0.4)

        # Legend
        legend = VGroup(
            Text("n = moles", font_size=24, color=TEXT_WHITE),
            Text("V = volume (L)", font_size=24, color=TEXT_WHITE)
        ).arrange(RIGHT, buff=1.5)
        legend.shift(DOWN * 4.5)
        self.play(FadeIn(legend), run_time=0.3)

        self.wait(wait_time)

        self.play(FadeOut(*self.mobjects[1:]), run_time=0.3)

    def content_scene_3_real_world(self, duration):
        """Scene 3: Real-world example - IV drip 0.9% NaCl"""
        anims = [0.4, 0.6, 0.5, 0.5, 0.5, 0.4, 0.5, 0.4, 0.3]
        wait_time = calc_wait(duration, anims, 4)

        # Title
        title = Text("Real Life Example", font_size=40, color=PRIMARY, weight=BOLD)
        title.to_edge(UP, buff=1.6)
        self.play(Write(title), run_time=0.4)

        # IV Drip bag visualization
        iv_bag = self.create_iv_bag()
        iv_bag.shift(UP * 0.8)
        self.play(DrawBorderThenFill(iv_bag), run_time=0.6)

        # Label on bag
        label_bg = RoundedRectangle(
            width=2.8, height=0.7, corner_radius=0.1,
            fill_color=WHITE, fill_opacity=0.9,
            stroke_color=BLUE, stroke_width=2
        )
        label_bg.move_to(iv_bag.get_center() + UP * 0.3)

        label_text = Text("0.9% NaCl", font_size=28, color="#1E3A5F", weight=BOLD)
        label_text.move_to(label_bg.get_center())

        self.play(FadeIn(label_bg), Write(label_text), run_time=0.5)

        self.wait(wait_time)

        # Show calculation
        calc_title = Text("Molarity = ?", font_size=34, color=YELLOW)
        calc_title.shift(DOWN * 1.5)
        self.play(Write(calc_title), run_time=0.5)

        # Calculation steps
        calc1 = MathTex(r"0.9\% = 0.9 \text{ g in 100 mL}", font_size=28, color=TEXT_WHITE)
        calc1.shift(DOWN * 2.3)
        self.play(Write(calc1), run_time=0.5)

        calc2 = MathTex(r"= 9 \text{ g in 1 L}", font_size=28, color=TEXT_WHITE)
        calc2.shift(DOWN * 2.9)
        self.play(Write(calc2), run_time=0.4)

        self.wait(wait_time)

        calc3 = MathTex(r"M = \frac{9}{58.5} = 0.154 \text{ M}", font_size=32, color=CYAN)
        calc3.shift(DOWN * 3.7)
        self.play(Write(calc3), run_time=0.5)

        self.wait(wait_time)

        # Mind-blow fact
        fact_box = RoundedRectangle(
            width=6.5, height=1, corner_radius=0.15,
            fill_color=PINK, fill_opacity=0.2,
            stroke_color=PINK, stroke_width=3
        )
        fact_box.shift(DOWN * 5)

        fact_text = Text("Your BLOOD runs on precise molarity!", font_size=26, color=PINK, weight=BOLD)
        fact_text.move_to(fact_box.get_center())

        self.play(Create(fact_box), Write(fact_text), run_time=0.4)

        self.wait(wait_time)

        self.play(FadeOut(*self.mobjects[1:]), run_time=0.3)

    # ========================================
    # SEGMENT 04: REVEAL - Mind Blow (13.848s)
    # ========================================
    def segment_04_reveal(self, timing):
        """Mind-blow: Volume shrinks, molarity DOUBLES!"""
        duration = timing.get('duration', 13.848)
        anims = [0.4, 0.6, 0.8, 0.5, 1.0, 0.5, 0.6, 0.5, 0.3]
        wait_time = calc_wait(duration, anims, 4)

        # Title
        title = Text("MIND BLOW!", font_size=56, color=YELLOW, weight=BOLD)
        title.to_edge(UP, buff=1.5)
        self.play(Write(title), run_time=0.4)
        self.play(title.animate.scale(1.1), run_time=0.15)
        self.play(title.animate.scale(1/1.1), run_time=0.15)

        # Start with 1L flask with 1 mole
        flask_big = self.create_volumetric_flask(scale=1.3)
        flask_big.shift(LEFT * 1.5 + UP * 0.3)

        molecules = self.create_molecule_cluster(count=16, spread=1.0)
        molecules.move_to(flask_big.get_center())

        label_big = Text("1 L", font_size=32, color=CYAN)
        label_big.next_to(flask_big, DOWN, buff=0.3)

        molarity_big = Text("1M", font_size=48, color=PRIMARY, weight=BOLD)
        molarity_big.next_to(label_big, DOWN, buff=0.2)

        self.play(
            DrawBorderThenFill(flask_big),
            FadeIn(molecules),
            Write(label_big),
            run_time=0.6
        )
        self.play(Write(molarity_big), run_time=0.4)

        self.wait(wait_time)

        # Arrow showing transformation
        arrow = Arrow(
            start=LEFT * 0.3 + UP * 0.3,
            end=RIGHT * 1.5 + UP * 0.3,
            color=YELLOW, stroke_width=5
        )
        self.play(GrowArrow(arrow), run_time=0.5)

        # Smaller flask (0.5L)
        flask_small = self.create_volumetric_flask(scale=0.9)
        flask_small.shift(RIGHT * 2.5 + UP * 0.3)

        # Same molecules but more compressed
        molecules_compressed = self.create_molecule_cluster(count=16, spread=0.5)
        molecules_compressed.move_to(flask_small.get_center())

        label_small = Text("0.5 L", font_size=32, color=ORANGE)
        label_small.next_to(flask_small, DOWN, buff=0.3)

        self.play(
            DrawBorderThenFill(flask_small),
            run_time=0.8
        )

        # Animate molecules "crushing" into smaller flask
        self.play(
            FadeIn(molecules_compressed, scale=1.5),
            Write(label_small),
            run_time=0.5
        )

        self.wait(wait_time)

        # Molarity jumps!
        molarity_small = Text("2M!", font_size=64, color=RED_ACCENT, weight=BOLD)
        molarity_small.next_to(label_small, DOWN, buff=0.2)
        self.play(
            Write(molarity_small),
            Flash(molarity_small, color=RED_ACCENT, line_length=0.4),
            run_time=0.6
        )

        self.wait(wait_time)

        # Explanation
        explain_box = RoundedRectangle(
            width=7, height=1.2, corner_radius=0.2,
            fill_color=CYAN, fill_opacity=0.2,
            stroke_color=CYAN, stroke_width=3
        )
        explain_box.shift(DOWN * 3)

        explain_text = VGroup(
            Text("Volume in DENOMINATOR", font_size=28, color=TEXT_WHITE),
            Text("Smaller V → BIGGER M!", font_size=30, color=CYAN, weight=BOLD)
        ).arrange(DOWN, buff=0.15)
        explain_text.move_to(explain_box.get_center())

        self.play(Create(explain_box), Write(explain_text), run_time=0.5)

        # Lightbulb animation
        bulb = Text("💡", font_size=72)
        bulb.shift(DOWN * 5)
        self.play(FadeIn(bulb, scale=0.3), run_time=0.3)

        self.wait(wait_time)

        self.play(FadeOut(*self.mobjects[1:]), run_time=0.3)

    # ========================================
    # SEGMENT 05: KEY POINT - Formula Card (12.216s)
    # ========================================
    def segment_05_key_point(self, timing):
        """Key formula card with common mistake warning."""
        duration = timing.get('duration', 12.216)
        anims = [0.4, 0.6, 0.5, 0.5, 0.5, 0.6, 0.5, 0.3]
        wait_time = calc_wait(duration, anims, 4)

        # Title
        title = Text("KEY FORMULA", font_size=44, color=PRIMARY, weight=BOLD)
        title.to_edge(UP, buff=1.6)
        self.play(Write(title), run_time=0.4)

        # Main formula card
        formula_box = RoundedRectangle(
            width=7, height=2.2, corner_radius=0.2,
            fill_color="#1a3329", fill_opacity=0.9,
            stroke_color=PRIMARY, stroke_width=4
        )
        formula_box.shift(UP * 0.8)

        formula = MathTex(
            r"M = \frac{n}{V} = \frac{\text{mass}/\text{molar mass}}{\text{Volume (L)}}",
            font_size=36, color=TEXT_WHITE
        )
        formula.move_to(formula_box.get_center())

        self.play(Create(formula_box), run_time=0.3)
        self.play(Write(formula), run_time=0.6)

        self.wait(wait_time)

        # Three boxes showing relationship
        box1 = self.create_info_box("n", "moles", CYAN, 1.8)
        box1.shift(LEFT * 2.5 + DOWN * 1.5)

        box2 = self.create_info_box("M", "molarity", PRIMARY, 1.8)
        box2.shift(DOWN * 1.5)

        box3 = self.create_info_box("V", "volume (L)", ORANGE, 1.8)
        box3.shift(RIGHT * 2.5 + DOWN * 1.5)

        self.play(
            FadeIn(box1, scale=0.8),
            FadeIn(box2, scale=0.8),
            FadeIn(box3, scale=0.8),
            run_time=0.5
        )

        self.wait(wait_time)

        # Highlight: ALWAYS convert to LITERS
        warning_box = RoundedRectangle(
            width=6.5, height=0.9, corner_radius=0.15,
            fill_color=YELLOW, fill_opacity=0.2,
            stroke_color=YELLOW, stroke_width=3
        )
        warning_box.shift(DOWN * 3)

        warning_text = Text("ALWAYS convert to LITERS!", font_size=30, color=YELLOW, weight=BOLD)
        warning_text.move_to(warning_box.get_center())

        self.play(Create(warning_box), Write(warning_text), run_time=0.5)

        self.wait(wait_time)

        # Common mistake animation
        mistake_title = Text("Common Mistake:", font_size=30, color=WRONG_RED, weight=BOLD)
        mistake_title.shift(DOWN * 4.2)
        self.play(Write(mistake_title), run_time=0.5)

        # Student using mL
        wrong_calc = MathTex(r"M = \frac{n}{500 \text{ mL}}", font_size=32, color=WRONG_RED)
        wrong_calc.shift(DOWN * 5)

        cross = Text("✗", font_size=48, color=WRONG_RED)
        cross.next_to(wrong_calc, RIGHT, buff=0.3)

        wrong_result = Text("1000× WRONG!", font_size=28, color=WRONG_RED, weight=BOLD)
        wrong_result.shift(DOWN * 5.8)

        self.play(Write(wrong_calc), FadeIn(cross), run_time=0.6)
        self.play(Write(wrong_result), run_time=0.5)

        self.wait(wait_time)

        self.play(FadeOut(*self.mobjects[1:]), run_time=0.3)

    # ========================================
    # SEGMENT 06: EXAM TIP - JEE/NEET (20.76s)
    # ========================================
    def segment_06_exam_tip(self, timing):
        """JEE/NEET question solve with mL trap warning."""
        duration = timing.get('duration', 20.76)
        anims = [0.4, 0.5, 0.6, 0.5, 0.5, 0.4, 0.4, 0.4, 0.5, 0.4, 0.5, 0.4, 0.3]
        wait_time = calc_wait(duration, anims, 5)

        # JEE/NEET badge
        badge = self.create_exam_badge("JEE / NEET", ORANGE)
        badge.to_edge(UP, buff=1.4)
        self.play(FadeIn(badge, scale=0.8), run_time=0.4)

        # Question box
        q_box = RoundedRectangle(
            width=7, height=1.8, corner_radius=0.2,
            fill_color="#1a3329", fill_opacity=0.9,
            stroke_color=CYAN, stroke_width=3
        )
        q_box.shift(UP * 1.8)

        q_text = VGroup(
            Text("Question:", font_size=28, color=CYAN, weight=BOLD),
            Text("4g NaOH in 500 mL", font_size=30, color=TEXT_WHITE),
            Text("Find Molarity (M)", font_size=28, color=YELLOW)
        ).arrange(DOWN, buff=0.15)
        q_text.move_to(q_box.get_center())

        self.play(Create(q_box), run_time=0.3)
        self.play(Write(q_text), run_time=0.6)

        self.wait(wait_time)

        # Solution steps
        sol_title = Text("Solution:", font_size=32, color=PRIMARY, weight=BOLD)
        sol_title.shift(DOWN * 0.2)
        self.play(Write(sol_title), run_time=0.5)

        # Step 1: Calculate moles
        step1 = MathTex(r"n = \frac{\text{mass}}{\text{molar mass}} = \frac{4}{40}", font_size=30, color=TEXT_WHITE)
        step1.shift(DOWN * 0.9)
        self.play(Write(step1), run_time=0.5)

        step1_result = MathTex(r"= 0.1 \text{ mol}", font_size=30, color=CYAN)
        step1_result.next_to(step1, RIGHT, buff=0.2)
        self.play(Write(step1_result), run_time=0.4)

        self.wait(wait_time)

        # Step 2: Convert volume to L (HIGHLIGHT!)
        step2_box = RoundedRectangle(
            width=6, height=0.8, corner_radius=0.1,
            fill_color=YELLOW, fill_opacity=0.3,
            stroke_color=YELLOW, stroke_width=2
        )
        step2_box.shift(DOWN * 1.9)

        step2 = MathTex(r"V = 500 \text{ mL} = 0.5 \text{ L}", font_size=30, color=YELLOW)
        step2.move_to(step2_box.get_center())

        self.play(Create(step2_box), Write(step2), run_time=0.4)

        # TRAP warning
        trap_text = Text("← TRAP! Always convert!", font_size=24, color=WRONG_RED, weight=BOLD)
        trap_text.next_to(step2_box, RIGHT, buff=0.2)
        self.play(Write(trap_text), run_time=0.4)

        self.wait(wait_time)

        # Step 3: Calculate M
        step3 = MathTex(r"M = \frac{n}{V} = \frac{0.1}{0.5}", font_size=30, color=TEXT_WHITE)
        step3.shift(DOWN * 2.9)
        self.play(Write(step3), run_time=0.5)

        # Final answer with box
        ans_box = RoundedRectangle(
            width=4, height=1, corner_radius=0.2,
            fill_color=PRIMARY, fill_opacity=0.3,
            stroke_color=PRIMARY, stroke_width=4
        )
        ans_box.shift(DOWN * 4)

        answer = MathTex(r"M = 0.2 \text{ M}", font_size=40, color=PRIMARY)
        answer.move_to(ans_box.get_center())

        self.play(Create(ans_box), Write(answer), run_time=0.4)

        # Checkmark
        check = Text("✓", font_size=56, color=CORRECT_GREEN)
        check.next_to(ans_box, RIGHT, buff=0.3)
        self.play(FadeIn(check), run_time=0.5)

        self.wait(wait_time)

        # Pro tip badge
        tip_box = RoundedRectangle(
            width=7, height=1, corner_radius=0.15,
            fill_color=ORANGE, fill_opacity=0.2,
            stroke_color=ORANGE, stroke_width=3
        )
        tip_box.shift(DOWN * 5.5)

        tip_text = Text("They LOVE giving volume in mL to confuse you!", font_size=24, color=ORANGE, weight=BOLD)
        tip_text.move_to(tip_box.get_center())

        self.play(Create(tip_box), Write(tip_text), run_time=0.4)

        self.wait(wait_time)

        self.play(FadeOut(*self.mobjects[1:]), run_time=0.3)

    # ========================================
    # SEGMENT 07: CTA (5.304s)
    # ========================================
    def segment_07_cta(self, timing):
        """CTA with molecules forming FOLLOW text."""
        duration = timing.get('duration', 5.304)

        # Use the standard CTA from mixin
        self._create_chemistry_cta(duration)

    def _create_chemistry_cta(self, duration):
        """Chemistry-specific CTA with molecule visual."""
        anims = [0.4, 0.4, 0.4, 0.3, 0.3, 0.2, 0.2]
        wait_time = calc_wait(duration, anims, 2, buffer=0.5)

        # Molecule dots forming pattern
        mol_dots = VGroup()
        for i in range(12):
            dot = Dot(
                radius=0.15,
                color=MOLECULE_COLORS[i % len(MOLECULE_COLORS)],
                fill_opacity=0.8
            )
            dot.move_to(np.array([
                np.random.uniform(-3, 3),
                np.random.uniform(3, 5),
                0
            ]))
            mol_dots.add(dot)

        self.play(
            *[FadeIn(d, scale=0.3) for d in mol_dots],
            run_time=0.4
        )

        # Official flame icon
        flame = create_brand_flame(scale=0.7)
        flame.move_to(UP * 3.5)
        self.play(FadeIn(flame, scale=0.5), run_time=0.4)

        # JeetLo Chemistry!
        jeet = Text("Jeet", font_size=52, color=TEXT_WHITE, weight=BOLD)
        lo = Text("Lo", font_size=52, color=PRIMARY, weight=BOLD)
        chem = Text(" Chemistry!", font_size=52, color=TEXT_WHITE, weight=BOLD)
        jeetlo = VGroup(jeet, lo, chem).arrange(RIGHT, buff=0.05)
        jeetlo.move_to(UP * 1.5)
        self.play(FadeIn(jeetlo, scale=1.2), run_time=0.4)

        # Follow tagline
        follow = Text("Follow for more!", font_size=36, color=FLAME_CORE, weight=BOLD)
        follow.move_to(DOWN * 0.3)
        self.play(FadeIn(follow, shift=UP), run_time=0.3)

        self.wait(wait_time)

        # URL
        url = Text("jeetlo.ai", font_size=40, color=PHYSICS_BLUE, weight=BOLD)
        url.move_to(DOWN * 2)
        self.play(Write(url), run_time=0.3)

        # Pricing
        pricing = Text("All courses ₹499/month", font_size=26, color=TEXT_WHITE)
        pricing.move_to(DOWN * 3)
        self.play(FadeIn(pricing), run_time=0.2)

        # Pulse flame
        self.play(flame.animate.scale(1.15), run_time=0.1)
        self.play(flame.animate.scale(1/1.15), run_time=0.1)

        self.wait(wait_time)

    # ========================================
    # HELPER METHODS
    # ========================================
    def create_subject_badge(self, text, color):
        """Create a subject badge with glow."""
        badge_bg = RoundedRectangle(
            width=4.5, height=0.85, corner_radius=0.2,
            fill_color=color, fill_opacity=0.3,
            stroke_color=color, stroke_width=3
        )
        badge_text = Text(text, font_size=34, color=color, weight=BOLD)
        badge_text.move_to(badge_bg.get_center())
        return VGroup(badge_bg, badge_text)

    def create_exam_badge(self, text, color):
        """Create an exam badge."""
        badge = RoundedRectangle(
            width=4, height=0.8, corner_radius=0.2,
            fill_color=color, fill_opacity=0.3,
            stroke_color=color, stroke_width=3
        )
        label = Text(text, font_size=28, color=color, weight=BOLD)
        label.move_to(badge.get_center())
        return VGroup(badge, label)

    def create_volumetric_flask(self, scale=1.0):
        """Create a volumetric flask shape."""
        flask = VGroup()

        # Neck (narrow tube)
        neck = Rectangle(
            width=0.4 * scale, height=1.0 * scale,
            fill_color="#0A2F1F", fill_opacity=0.5,
            stroke_color=CYAN, stroke_width=2
        )
        neck.shift(UP * 1.2 * scale)

        # Body (bulb shape - approximated with ellipse)
        body = Ellipse(
            width=2.2 * scale, height=1.8 * scale,
            fill_color="#0A2F1F", fill_opacity=0.5,
            stroke_color=CYAN, stroke_width=2
        )

        # Base
        base = Rectangle(
            width=2.4 * scale, height=0.2 * scale,
            fill_color=CYAN, fill_opacity=0.3,
            stroke_color=CYAN, stroke_width=2
        )
        base.shift(DOWN * 0.9 * scale)

        # Graduation mark
        mark = Line(
            start=LEFT * 1.1 * scale, end=RIGHT * 1.1 * scale,
            color=CYAN, stroke_width=1
        )
        mark.shift(UP * 0.4 * scale)

        flask.add(neck, body, base, mark)
        return flask

    def create_glass(self, height=2.5, width=1.2):
        """Create a simple drinking glass."""
        glass = VGroup()

        # Glass body (trapezoid-ish)
        left_line = Line(
            start=np.array([-width/2 * 0.8, -height/2, 0]),
            end=np.array([-width/2, height/2, 0]),
            color=CYAN, stroke_width=2
        )
        right_line = Line(
            start=np.array([width/2 * 0.8, -height/2, 0]),
            end=np.array([width/2, height/2, 0]),
            color=CYAN, stroke_width=2
        )
        bottom = Line(
            start=np.array([-width/2 * 0.8, -height/2, 0]),
            end=np.array([width/2 * 0.8, -height/2, 0]),
            color=CYAN, stroke_width=2
        )

        glass.add(left_line, right_line, bottom)
        return glass

    def create_water_fill(self, glass, fill_level=0.8, color="#3498DB"):
        """Create water fill inside a glass."""
        glass_center = glass.get_center()
        glass_bottom = glass.get_bottom()

        # Approximate dimensions
        width = 1.0
        height = 2.0 * fill_level

        water = Rectangle(
            width=width, height=height,
            fill_color=color, fill_opacity=0.5,
            stroke_width=0
        )
        water.move_to(glass_bottom + UP * height/2)
        return water

    def create_powder_dots(self, count=5):
        """Create Rasna powder dots."""
        dots = VGroup()
        for i in range(count):
            dot = Dot(
                radius=0.08,
                color=ORANGE,
                fill_opacity=0.9
            )
            dot.shift(np.array([
                np.random.uniform(-0.3, 0.3),
                np.random.uniform(-0.2, 0.2),
                0
            ]))
            dots.add(dot)
        return dots

    def create_molecule_rain(self, count=20, target=ORIGIN):
        """Create molecules that will 'rain' into a flask."""
        molecules = VGroup()
        for i in range(count):
            mol = Dot(
                radius=0.12,
                color=MOLECULE_COLORS[i % len(MOLECULE_COLORS)],
                fill_opacity=0.8
            )
            # Position around target with some spread
            mol.move_to(target + np.array([
                np.random.uniform(-0.7, 0.7),
                np.random.uniform(-0.5, 0.5),
                0
            ]))
            molecules.add(mol)
        return molecules

    def create_molecule_cluster(self, count=15, spread=0.8):
        """Create a cluster of molecules."""
        cluster = VGroup()
        for i in range(count):
            mol = Dot(
                radius=0.1,
                color=MOLECULE_COLORS[i % len(MOLECULE_COLORS)],
                fill_opacity=0.85
            )
            mol.shift(np.array([
                np.random.uniform(-spread, spread),
                np.random.uniform(-spread * 0.6, spread * 0.6),
                0
            ]))
            cluster.add(mol)
        return cluster

    def create_iv_bag(self):
        """Create an IV drip bag visualization."""
        bag = VGroup()

        # Main bag body
        body = RoundedRectangle(
            width=2.5, height=3.2, corner_radius=0.3,
            fill_color="#E8F4FD", fill_opacity=0.8,
            stroke_color=BLUE, stroke_width=2
        )

        # Hanging hook
        hook = Line(
            start=UP * 1.6, end=UP * 2.2,
            color=GRAY, stroke_width=3
        )
        hook_top = Circle(
            radius=0.15, color=GRAY,
            fill_opacity=0.5, stroke_width=2
        )
        hook_top.shift(UP * 2.35)

        # Tube at bottom
        tube = Rectangle(
            width=0.15, height=0.6,
            fill_color=CYAN, fill_opacity=0.5,
            stroke_color=CYAN, stroke_width=1
        )
        tube.shift(DOWN * 1.9)

        bag.add(body, hook, hook_top, tube)
        return bag

    def create_info_box(self, symbol, label, color, width=2.0):
        """Create a small info box with symbol and label."""
        box = VGroup()

        bg = RoundedRectangle(
            width=width, height=1.0, corner_radius=0.15,
            fill_color=color, fill_opacity=0.2,
            stroke_color=color, stroke_width=2
        )

        sym = Text(symbol, font_size=32, color=color, weight=BOLD)
        sym.shift(UP * 0.15)

        lab = Text(label, font_size=18, color=TEXT_WHITE)
        lab.shift(DOWN * 0.25)

        box.add(bg, sym, lab)
        return box


# Exports
__all__ = ['MolarityReel']
