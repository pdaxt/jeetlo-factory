"""
Monkey Gun Reel - Physics Educational Content
=============================================
Topic: Projectile Motion - Why aiming directly at a falling target always hits

Creative Brief:
- Core Analogy: Gravity is the ultimate wingman - both bullet and monkey fall together
- Mind Blow: Both fall by ½gt² regardless of bullet speed
"""

import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')
from manim import *
from jeetlo_style import JeetLoReelMixin, create_brand_watermark, PHYSICS_BLUE, WRONG_RED, CORRECT_GREEN, FLAME_CORE, TEXT_WHITE
import numpy as np
import json
import os

# Import manim-edu components for physics
from manim_edu.physics import MechanicsSimulator

# Colors for this reel
BG_COLOR = '#0A1A3F'
SUBJECT_COLOR = '#0066FF'
BULLET_COLOR = '#FFD700'  # Gold
MONKEY_COLOR = '#8B4513'  # Brown
TREE_COLOR = '#228B22'  # Forest green
TRAJECTORY_COLOR = '#FF6B35'  # Orange
GRAVITY_COLOR = '#FF4444'  # Red
HIGHLIGHT_YELLOW = '#FFFF00'


class MonkeyGunReel(JeetLoReelMixin, Scene):
    subject = "physics"

    def construct(self):
        self.camera.background_color = BG_COLOR
        self.add(create_brand_watermark())

        # Load timings from file
        timings_path = os.path.join(os.path.dirname(__file__), 'audio', 'timings.json')
        with open(timings_path) as f:
            timings_data = json.load(f)

        # Filter out combined_audio and create lookup
        self.timings = [t for t in timings_data if t['id'] != 'combined_audio']

        # Call each segment
        for seg in self.timings:
            method_name = f"segment_{seg['id']}"
            method = getattr(self, method_name, None)
            if method:
                method(seg)

    def create_hunter(self, position=ORIGIN, scale=1.0):
        """Create a simple hunter figure."""
        hunter = VGroup()

        # Body
        body = Rectangle(width=0.3*scale, height=0.6*scale, color=SUBJECT_COLOR, fill_opacity=0.8)
        body.move_to(position)

        # Head
        head = Circle(radius=0.15*scale, color=TEXT_WHITE, fill_opacity=0.9)
        head.next_to(body, UP, buff=0.02*scale)

        # Gun
        gun = Rectangle(width=0.5*scale, height=0.08*scale, color='#555555', fill_opacity=1)
        gun.next_to(body, RIGHT, buff=0)
        gun.shift(UP * 0.1 * scale)

        hunter.add(body, head, gun)
        return hunter

    def create_tree(self, position=ORIGIN, scale=1.0):
        """Create a simple tree."""
        tree = VGroup()

        # Trunk
        trunk = Rectangle(width=0.3*scale, height=1.5*scale, color='#8B4513', fill_opacity=0.9)
        trunk.move_to(position)

        # Leaves (triangle)
        leaves = Triangle(color=TREE_COLOR, fill_opacity=0.9)
        leaves.scale(1.2*scale)
        leaves.next_to(trunk, UP, buff=-0.2*scale)

        tree.add(trunk, leaves)
        return tree

    def create_monkey(self, position=ORIGIN, scale=1.0):
        """Create a simple monkey figure."""
        monkey = VGroup()

        # Body
        body = Ellipse(width=0.4*scale, height=0.5*scale, color=MONKEY_COLOR, fill_opacity=0.9)
        body.move_to(position)

        # Head
        head = Circle(radius=0.18*scale, color=MONKEY_COLOR, fill_opacity=0.9)
        head.next_to(body, UP, buff=0.02*scale)

        # Eyes
        left_eye = Dot(radius=0.03*scale, color=WHITE)
        right_eye = Dot(radius=0.03*scale, color=WHITE)
        left_eye.move_to(head.get_center() + LEFT*0.06*scale + UP*0.03*scale)
        right_eye.move_to(head.get_center() + RIGHT*0.06*scale + UP*0.03*scale)

        # Tail
        tail = Arc(radius=0.25*scale, start_angle=PI/2, angle=PI, color=MONKEY_COLOR, stroke_width=4*scale)
        tail.next_to(body, LEFT, buff=-0.05*scale)

        monkey.add(body, head, left_eye, right_eye, tail)
        return monkey

    def create_bullet(self, position=ORIGIN, scale=1.0):
        """Create a bullet."""
        bullet = Dot(radius=0.1*scale, color=BULLET_COLOR)
        bullet.move_to(position)
        bullet.set_z_index(10)
        return bullet

    def segment_01_hook(self, timing):
        """Hook: Hunter aimed directly... and MISSED! Why?"""
        duration = timing['duration']

        # Animation times
        total_anim_time = 0.5 + 0.4 + 0.3 + 0.8 + 0.4 + 0.4
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        # Create scene elements
        hunter = self.create_hunter(position=LEFT*2.5 + DOWN*2, scale=0.8)
        tree = self.create_tree(position=RIGHT*2.5 + DOWN*1, scale=1.2)
        monkey = self.create_monkey(position=RIGHT*2 + UP*2.5, scale=0.7)

        # Branch for monkey to sit on
        branch = Line(RIGHT*1.5 + UP*2.2, RIGHT*3 + UP*2.2, color='#8B4513', stroke_width=8)

        # Title text
        title = Text("DIRECTLY aim... aur MISS?!", font_size=42, color=WRONG_RED, weight=BOLD)
        title.move_to(UP*5)

        # Show scene
        self.play(
            FadeIn(hunter, shift=RIGHT),
            FadeIn(tree, shift=UP),
            FadeIn(branch),
            FadeIn(monkey, shift=DOWN),
            run_time=0.5
        )
        self.wait(wait_time)

        self.play(Write(title), run_time=0.4)
        self.wait(wait_time)

        # Aim line (dashed) - hunter aims DIRECTLY at monkey
        aim_line = DashedLine(
            hunter.get_right() + UP*0.1,
            monkey.get_center(),
            color=SUBJECT_COLOR, stroke_width=2
        )
        self.play(Create(aim_line), run_time=0.3)

        # Fire bullet (naive - straight at where monkey IS)
        bullet = self.create_bullet(hunter.get_right() + UP*0.1, scale=0.8)
        self.add(bullet)

        # Bullet curves down due to gravity (parabolic path) - MISSES above!
        # Bullet drops but monkey stays, so bullet goes UNDER the aim line
        start = np.array(bullet.get_center())
        target = np.array(monkey.get_center())

        # Bullet follows parabola, ends up ABOVE monkey's original position
        # (because gravity pulls it down, it passes above stationary monkey)
        end = target + UP*0.8  # Misses ABOVE

        self.play(
            bullet.animate.move_to(end),
            run_time=0.8,
            rate_func=linear
        )
        self.wait(wait_time)

        # WRONG! text
        wrong = Text("WRONG!", font_size=72, color=WRONG_RED, weight=BOLD)
        wrong.move_to(ORIGIN)
        self.play(FadeIn(wrong, scale=1.5), run_time=0.4)

        # Question text
        question = Text("Intuition WRONG hai!", font_size=36, color=HIGHLIGHT_YELLOW)
        question.move_to(DOWN*2)
        self.play(Write(question), run_time=0.4)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_02_setup(self, timing):
        """Setup: Classic problem - monkey on tree, hunter aims directly."""
        duration = timing['duration']

        total_anim_time = 0.5 + 0.4 + 0.4 + 0.3 + 0.4 + 0.4
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.add(create_brand_watermark())

        # Title
        title = Text("CLASSIC PROBLEM", font_size=48, color=PHYSICS_BLUE, weight=BOLD)
        title.move_to(UP*5.5)

        self.play(FadeIn(title), run_time=0.5)
        self.wait(wait_time)

        # Setup scene
        tree = self.create_tree(position=RIGHT*2.5 + DOWN*0.5, scale=1.3)
        monkey = self.create_monkey(position=RIGHT*2 + UP*3, scale=0.7)
        hunter = self.create_hunter(position=LEFT*2.5 + DOWN*2, scale=0.8)

        self.play(FadeIn(tree), FadeIn(monkey), FadeIn(hunter), run_time=0.4)
        self.wait(wait_time)

        # Height label 'h'
        h_line = DashedLine(
            RIGHT*3.2 + DOWN*2.5,
            RIGHT*3.2 + UP*3,
            color=YELLOW, stroke_width=2
        )
        h_label = Text("h", font_size=36, color=YELLOW)
        h_label.next_to(h_line, RIGHT, buff=0.2)

        self.play(Create(h_line), FadeIn(h_label), run_time=0.4)

        # Distance label 'd'
        d_line = Line(
            LEFT*2.5 + DOWN*3.5,
            RIGHT*2.5 + DOWN*3.5,
            color=TEAL
        )
        d_label = Text("d", font_size=36, color=TEAL)
        d_label.next_to(d_line, DOWN, buff=0.2)

        self.play(Create(d_line), FadeIn(d_label), run_time=0.3)
        self.wait(wait_time)

        # Aim line with question mark
        aim_line = DashedLine(
            hunter.get_right() + UP*0.1,
            monkey.get_center(),
            color=YELLOW, stroke_width=3, dash_length=0.15
        )

        self.play(Create(aim_line), run_time=0.4)

        # Question text
        question = Text("Bullet KAHAAN jaayegi?", font_size=36, color=HIGHLIGHT_YELLOW)
        question.move_to(DOWN*5)

        self.play(Write(question), run_time=0.4)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_03_content_part1(self, timing):
        """Content Part 1: Why direct aim FAILS - bullet curves DOWN."""
        duration = timing['duration']

        total_anim_time = 0.4 + 0.4 + 0.5 + 1.5 + 0.5 + 0.4 + 0.4
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.add(create_brand_watermark())

        # Title
        title = Text("Direct Aim = MISS!", font_size=44, color=WRONG_RED, weight=BOLD)
        title.move_to(UP*5.5)

        self.play(FadeIn(title), run_time=0.4)
        self.wait(wait_time)

        # Scene setup
        tree = self.create_tree(position=RIGHT*2.5 + DOWN*0.5, scale=1.0)
        monkey = self.create_monkey(position=RIGHT*2 + UP*2.5, scale=0.6)
        hunter = self.create_hunter(position=LEFT*2.5 + DOWN*2, scale=0.7)

        # Straight aim line (what would happen WITHOUT gravity)
        straight_line = DashedLine(
            hunter.get_right() + UP*0.1,
            monkey.get_center() + RIGHT*0.5,
            color=WHITE, stroke_width=1, dash_length=0.2
        )

        self.play(FadeIn(tree), FadeIn(monkey), FadeIn(hunter), Create(straight_line), run_time=0.4)
        self.wait(wait_time)

        # Fire explanation
        fire_text = Text("Hunter fires!", font_size=32, color=FLAME_CORE)
        fire_text.move_to(UP*4)
        self.play(Write(fire_text), run_time=0.5)

        # Bullet with trajectory
        bullet = self.create_bullet(hunter.get_right() + UP*0.1, scale=0.8)
        self.add(bullet)

        # Create curved path (parabola due to gravity)
        start = np.array(hunter.get_right() + UP*0.1)
        target = np.array(monkey.get_center())
        direction = target - start

        # Trajectory - bullet curves DOWN
        curve_points = []
        for t in np.linspace(0, 1, 40):
            x = start[0] + t * direction[0]
            y = start[1] + t * direction[1] - 2.5 * t**2  # Gravity pulls down!
            curve_points.append([x, y, 0])

        trajectory = VMobject()
        trajectory.set_points_smoothly([np.array(p) for p in curve_points])
        trajectory.set_stroke(color=TRAJECTORY_COLOR, width=4)

        # Animate bullet along curved path
        self.play(
            Create(trajectory),
            MoveAlongPath(bullet, trajectory),
            run_time=1.5
        )
        self.wait(wait_time)

        # Gravity explanation
        gravity_text = Text("Gravity pulls bullet DOWN!", font_size=32, color=GRAVITY_COLOR, weight=BOLD)
        gravity_text.move_to(DOWN*0.5)
        g_arrow = Arrow(ORIGIN + LEFT*0.5, DOWN*1.2 + LEFT*0.5, color=GRAVITY_COLOR, stroke_width=4)

        self.play(Write(gravity_text), Create(g_arrow), run_time=0.5)
        self.wait(wait_time)

        # MISS result
        miss_x = Text("X MISSED!", font_size=48, color=WRONG_RED, weight=BOLD)
        miss_x.move_to(bullet.get_center() + UP*0.8)

        self.play(FadeIn(miss_x, scale=1.3), run_time=0.4)

        # Direct aim failed text
        failed_text = Text("Direct aim FAILED!", font_size=36, color=WRONG_RED)
        failed_text.move_to(DOWN*4)

        self.play(Write(failed_text), run_time=0.4)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.3)

    def segment_03_content_part2(self, timing):
        """Content Part 2: Magic - what if monkey ALSO falls?"""
        duration = timing['duration']

        total_anim_time = 0.4 + 0.5 + 0.5 + 2.0 + 0.5 + 0.4
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.add(create_brand_watermark())

        # Title
        title = Text("THE MAGIC!", font_size=52, color=FLAME_CORE, weight=BOLD)
        title.move_to(UP*5.5)

        self.play(FadeIn(title, scale=1.2), run_time=0.4)
        self.wait(wait_time)

        # Key insight
        insight = Text("Monkey DROPS when gun fires!", font_size=36, color=HIGHLIGHT_YELLOW, weight=BOLD)
        insight.move_to(UP*4)

        self.play(Write(insight), run_time=0.5)
        self.wait(wait_time)

        # Scene setup
        tree = self.create_tree(position=RIGHT*2.5 + DOWN*0.5, scale=1.0)
        monkey_start = RIGHT*2 + UP*2.5
        monkey = self.create_monkey(position=monkey_start, scale=0.6)
        hunter = self.create_hunter(position=LEFT*2.5 + DOWN*2, scale=0.7)
        bullet_start = hunter.get_right() + UP*0.1
        bullet = self.create_bullet(bullet_start, scale=0.8)

        self.play(FadeIn(tree), FadeIn(monkey), FadeIn(hunter), FadeIn(bullet), run_time=0.5)
        self.wait(wait_time)

        # Both start falling at t=0
        start_text = Text("SAME time pe girna shuru!", font_size=32, color=CORRECT_GREEN)
        start_text.move_to(UP*2.5)

        self.play(Write(start_text), run_time=0.5)

        # Create synchronized falling paths
        # Both fall by SAME amount: ½gt²
        start = np.array(bullet_start)
        target = np.array(monkey_start)
        direction = target - start

        # Final positions - they meet!
        meeting_point = np.array([RIGHT*0.5 + UP*0])

        # Create bullet trace
        bullet_trace = TracedPath(bullet.get_center, stroke_color=BULLET_COLOR, stroke_width=3)
        self.add(bullet_trace)

        # Create monkey trace
        monkey_trace = TracedPath(monkey.get_center, stroke_color=MONKEY_COLOR, stroke_width=3)
        self.add(monkey_trace)

        # Gravity arrows
        g_arrow_1 = Arrow(LEFT*1 + UP*2, LEFT*1 + UP*1, color=GRAVITY_COLOR, stroke_width=3)
        g_label_1 = Text("g", font_size=28, color=GRAVITY_COLOR)
        g_label_1.next_to(g_arrow_1, LEFT, buff=0.1)

        g_arrow_2 = Arrow(RIGHT*3 + UP*2, RIGHT*3 + UP*1, color=GRAVITY_COLOR, stroke_width=3)
        g_label_2 = Text("g", font_size=28, color=GRAVITY_COLOR)
        g_label_2.next_to(g_arrow_2, RIGHT, buff=0.1)

        self.play(
            Create(g_arrow_1), FadeIn(g_label_1),
            Create(g_arrow_2), FadeIn(g_label_2),
            run_time=0.3
        )

        # Animate BOTH falling simultaneously!
        final_meeting = RIGHT*0.5 + DOWN*0.5
        self.play(
            bullet.animate.move_to(final_meeting),
            monkey.animate.move_to(final_meeting),
            run_time=2.0,
            rate_func=smooth
        )
        self.wait(wait_time)

        # Same gravity text
        same_text = Text("SAME gravity on BOTH!", font_size=36, color=GRAVITY_COLOR, weight=BOLD)
        same_text.move_to(DOWN*3.5)

        self.play(Write(same_text), run_time=0.5)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def segment_03_content_part3(self, timing):
        """Content Part 3: The BEAUTIFUL collision - time markers."""
        duration = timing['duration']

        total_anim_time = 0.4 + 0.5 + 0.6 + 0.6 + 0.6 + 0.6 + 2.0 + 0.6 + 0.5 + 0.4
        num_waits = 5
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.add(create_brand_watermark())

        # Title
        title = Text("THE BEAUTIFUL COLLISION", font_size=40, color=PHYSICS_BLUE, weight=BOLD)
        title.move_to(UP*5.5)

        self.play(FadeIn(title), run_time=0.4)
        self.wait(wait_time)

        # Initial positions
        monkey_start = np.array([2, 3, 0])
        bullet_start = np.array([-2.5, -1.5, 0])

        monkey = self.create_monkey(position=monkey_start, scale=0.5)
        bullet = self.create_bullet(bullet_start, scale=0.7)

        # Reference line for monkey's original position
        ref_line = DashedLine(
            monkey_start + UP*0.5,
            monkey_start + DOWN*5,
            color=WHITE, stroke_width=1, dash_length=0.1
        )

        self.play(FadeIn(monkey), FadeIn(bullet), Create(ref_line), run_time=0.5)
        self.wait(wait_time)

        # Time marker: t = 0
        t_label = Text("t = 0", font_size=36, color=WHITE)
        t_label.move_to(LEFT*3 + UP*4)

        self.play(FadeIn(t_label), run_time=0.6)
        self.wait(wait_time)

        # Drop calculations
        direction = monkey_start - bullet_start

        # t = 1
        drop_1 = 0.8
        monkey_t1 = monkey_start + DOWN*drop_1
        bullet_t1 = bullet_start + direction*0.35 + DOWN*drop_1

        t1_label = Text("t = 1", font_size=36, color=WHITE)
        t1_label.move_to(LEFT*3 + UP*4)

        self.play(
            Transform(t_label, t1_label),
            monkey.animate.move_to(monkey_t1),
            bullet.animate.move_to(bullet_t1),
            run_time=0.6
        )

        # Same drop indicator
        drop_text1 = Text("SAME drop!", font_size=28, color=CORRECT_GREEN)
        drop_text1.move_to(ORIGIN + UP*1)
        self.play(FadeIn(drop_text1), run_time=0.6)
        self.wait(wait_time)
        self.play(FadeOut(drop_text1), run_time=0.3)

        # t = 2
        drop_2 = 2.5
        monkey_t2 = monkey_start + DOWN*drop_2
        bullet_t2 = bullet_start + direction*0.7 + DOWN*drop_2

        t2_label = Text("t = 2", font_size=36, color=WHITE)
        t2_label.move_to(LEFT*3 + UP*4)

        self.play(
            Transform(t_label, t2_label),
            monkey.animate.move_to(monkey_t2),
            bullet.animate.move_to(bullet_t2),
            run_time=0.6
        )

        drop_text2 = Text("SAME drop again!", font_size=28, color=CORRECT_GREEN)
        drop_text2.move_to(ORIGIN)
        self.play(FadeIn(drop_text2), run_time=0.6)
        self.wait(wait_time)
        self.play(FadeOut(drop_text2), FadeOut(t_label), run_time=0.3)

        # Final collision!
        collision_point = bullet_start + direction*1.0 + DOWN*4
        self.play(
            monkey.animate.move_to(collision_point),
            bullet.animate.move_to(collision_point),
            run_time=2.0,
            rate_func=smooth
        )

        # Collision effect!
        collision_circle = Circle(radius=0.8, fill_color=YELLOW, fill_opacity=0.6, stroke_width=0)
        collision_circle.move_to(collision_point)

        collision_text = Text("COLLIDE!", font_size=56, color=CORRECT_GREEN, weight=BOLD)
        collision_text.move_to(collision_point + UP*1.5)

        self.play(
            FadeIn(collision_circle, scale=2),
            FadeIn(collision_text, scale=1.3),
            run_time=0.6
        )
        self.play(collision_circle.animate.scale(0.5).set_opacity(0), run_time=0.4)
        self.wait(wait_time)

        # Key formula
        formula = Text("Drop = half g t squared (SAME!)", font_size=32, color=FLAME_CORE)
        formula.move_to(DOWN*5)

        self.play(Write(formula), run_time=0.5)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def segment_04_reveal(self, timing):
        """Reveal: Mind BLOWN - Same gravity = Same fall = GUARANTEED collision."""
        duration = timing['duration']

        total_anim_time = 0.5 + 0.5 + 0.5 + 0.5 + 0.5 + 0.4
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.add(create_brand_watermark())

        # Mind blown
        mind_blown = Text("Mind BLOWN?", font_size=60, color=FLAME_CORE, weight=BOLD)
        mind_blown.move_to(UP*4.5)

        self.play(FadeIn(mind_blown, scale=1.5), run_time=0.5)
        self.wait(wait_time)

        # The beautiful chain
        line1 = Text("Same Gravity", font_size=48, color=PHYSICS_BLUE, weight=BOLD)
        line1.move_to(UP*2)

        equals1 = Text("=", font_size=56, color=WHITE)
        equals1.move_to(UP*1)

        line2 = Text("Same Fall", font_size=48, color=CORRECT_GREEN, weight=BOLD)
        line2.move_to(ORIGIN)

        equals2 = Text("=", font_size=56, color=WHITE)
        equals2.move_to(DOWN*1)

        line3 = Text("GUARANTEED COLLISION!", font_size=44, color=FLAME_CORE, weight=BOLD)
        line3.move_to(DOWN*2.2)

        self.play(Write(line1), run_time=0.5)
        self.wait(wait_time)
        self.play(FadeIn(equals1), Write(line2), run_time=0.5)
        self.wait(wait_time)
        self.play(FadeIn(equals2), Write(line3), run_time=0.5)
        self.wait(wait_time)

        # Speed doesn't matter insight
        insight = Text("Bullet speed = DOESN'T MATTER!", font_size=32, color=WHITE)
        insight.move_to(DOWN*4.5)

        self.play(Write(insight), run_time=0.5)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def segment_05_key_point(self, timing):
        """Key Point: Math proof - half g t squared cancellation."""
        duration = timing['duration']

        total_anim_time = 0.4 + 0.6 + 0.6 + 0.5 + 0.6 + 0.6 + 0.5 + 0.4
        num_waits = 5
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.add(create_brand_watermark())

        # Title
        title = Text("THE MATH", font_size=52, color=PHYSICS_BLUE, weight=BOLD)
        title.move_to(UP*5.5)

        self.play(FadeIn(title), run_time=0.4)
        self.wait(wait_time)

        # Bullet equation
        bullet_label = Text("Bullet height:", font_size=28, color=BULLET_COLOR)
        bullet_label.move_to(UP*3.5 + LEFT*1.5)

        # y = v₀t - ½gt²
        bullet_eq_parts = VGroup(
            Text("y = v", font_size=32, color=WHITE),
            Text("₀", font_size=24, color=WHITE),
            Text("t - ", font_size=32, color=WHITE),
            Text("half g t squared", font_size=28, color=GRAVITY_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.08)
        bullet_eq_parts.move_to(UP*2.5)

        self.play(Write(bullet_label), run_time=0.6)
        self.play(Write(bullet_eq_parts), run_time=0.6)
        self.wait(wait_time)

        # Monkey equation
        monkey_label = Text("Monkey height:", font_size=28, color=MONKEY_COLOR)
        monkey_label.move_to(UP*1 + LEFT*1.5)

        # y = h - ½gt²
        monkey_eq_parts = VGroup(
            Text("y = h - ", font_size=32, color=WHITE),
            Text("half g t squared", font_size=28, color=GRAVITY_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.08)
        monkey_eq_parts.move_to(UP*0)

        self.play(Write(monkey_label), run_time=0.5)
        self.play(Write(monkey_eq_parts), run_time=0.6)
        self.wait(wait_time)

        # Highlight the matching terms
        highlight_box1 = SurroundingRectangle(bullet_eq_parts[-1], color=CORRECT_GREEN, buff=0.1)
        highlight_box2 = SurroundingRectangle(monkey_eq_parts[-1], color=CORRECT_GREEN, buff=0.1)

        self.play(Create(highlight_box1), Create(highlight_box2), run_time=0.6)
        self.wait(wait_time)

        # CANCEL!
        cancel_text = Text("CANCEL!", font_size=56, color=CORRECT_GREEN, weight=BOLD)
        cancel_text.move_to(DOWN*1.5)

        self.play(FadeIn(cancel_text, scale=1.5), run_time=0.5)
        self.wait(wait_time)

        # Result
        result = Text("Bullet's aim = Monkey's position!", font_size=32, color=WHITE)
        result.move_to(DOWN*3.5)

        self.play(Write(result), run_time=0.5)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def segment_06_exam_tip(self, timing):
        """Exam Tip: JEE/NEET pattern - collision INDEPENDENT of v₀."""
        duration = timing['duration']

        total_anim_time = 0.5 + 0.6 + 0.5 + 0.6 + 0.5 + 0.5 + 0.4
        num_waits = 4
        wait_time = max(0.1, (duration - total_anim_time) / num_waits)

        self.add(create_brand_watermark())

        # Exam header
        exam_header = VGroup(
            Text("JEE", font_size=44, color='#FF6B35', weight=BOLD),
            Text(" / ", font_size=44, color=TEXT_WHITE),
            Text("NEET", font_size=44, color=CORRECT_GREEN, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        exam_header.move_to(UP*5.5)

        self.play(Write(exam_header), run_time=0.5)
        self.wait(wait_time)

        # Key exam insight
        insight1 = Text("Collision is INDEPENDENT", font_size=40, color=PHYSICS_BLUE, weight=BOLD)
        insight1.move_to(UP*3.5)

        insight2 = Text("of initial velocity!", font_size=40, color=PHYSICS_BLUE, weight=BOLD)
        insight2.move_to(UP*2.5)

        self.play(Write(insight1), run_time=0.6)
        self.play(Write(insight2), run_time=0.5)
        self.wait(wait_time)

        # Time formula
        time_label = Text("Time to collision:", font_size=28, color=WHITE)
        time_label.move_to(UP*1)

        # t = d / (v₀ cos θ)
        time_formula = Text("t = d / (v naught cos theta)", font_size=32, color=TEAL)
        time_formula.move_to(UP*0)

        self.play(Write(time_label), run_time=0.5)
        self.play(Write(time_formula), run_time=0.6)
        self.wait(wait_time)

        # Key point
        key_point = Text("Both fall half g t squared in that time!", font_size=32, color=CORRECT_GREEN, weight=BOLD)
        key_point.move_to(DOWN*1.5)

        self.play(Write(key_point), run_time=0.5)
        self.wait(wait_time)

        # Remember box
        remember_box = RoundedRectangle(width=5.5, height=1.2, corner_radius=0.2,
                                        color=FLAME_CORE, fill_opacity=0.2, stroke_width=3)
        remember_box.move_to(DOWN*4)

        remember_text = Text("YAAD RAKHIYE!", font_size=36, color=FLAME_CORE, weight=BOLD)
        remember_text.move_to(DOWN*4)

        self.play(Create(remember_box), Write(remember_text), run_time=0.5)
        self.wait(wait_time)

        # Cleanup
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def segment_07_cta(self, timing):
        """CTA: JeetLo Physics - Follow for more!"""
        duration = timing['duration']

        # MANDATORY: Use the pre-built CTA slide from JeetLoReelMixin
        self.add_cta_slide_physics(duration)


# For direct execution
if __name__ == "__main__":
    from manim import config
    config.pixel_width = 1080
    config.pixel_height = 1920
    config.frame_width = 8
    config.frame_height = 14.22

    scene = MonkeyGunReel()
    scene.render()
