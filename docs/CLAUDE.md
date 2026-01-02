# CLAUDE.md - Instructions for Revolutionary Educational Videos

> **This file instructs Claude on how to create truly exceptional educational content using jeetlo-factory.**

---

## THE VISION: Revolutionary Education

Every JeetLo video must be **unforgettable**. We're not making textbook animations. We're creating content that:

1. **Rewires mental models** - Students see concepts differently forever
2. **Goes viral organically** - So good that sharing is automatic
3. **Beats any coaching institute** - Free content better than paid
4. **Creates "Aha!" moments** - The brain chemistry of sudden understanding

---

## THE MANIM-EDU LIBRARY (MANDATORY)

**Location:** `/Users/pran/Projects/libraries/manim-edu`

All scientific visualizations MUST use manim-edu. This ensures:
- Consistent quality across all reels
- Beautiful formulas WITHOUT LaTeX dependencies
- Smart positioning and animations
- Brand compliance

### Available Components

```python
# Atomic Formula System (NEW - Use This!)
from manim_edu.formulas import (
    # Atomic building blocks
    Char,          # Single character with color + size
    CharSeq,       # Sequence with per-character colors/sizes
    SmartUnit,     # Element + subscript/superscript (self-aware positioning)

    # Formula components
    Term,          # Variable with sub/superscript (x₁², θ, n₁)
    Op,            # Operators (+, -, =, →)
    Frac,          # Fractions (a/b)
    Sqrt,          # Square roots (√x)
    Paren,         # Parentheses that scale
    SumInt,        # Summation and integral symbols

    # High-level
    Formula,       # Combine any components
    Chem,          # Chemical formulas (H₂O, C₆H₁₂O₆, Fe³⁺)
    FormulaRenderer,  # Pre-built physics/chemistry/math formulas
)

# Subject-specific visualizers
from manim_edu.physics import WaveSimulator, FieldVisualizer, MechanicsSimulator
from manim_edu.chemistry import MoleculeBuilder
from manim_edu.biology import CellVisualizer
from manim_edu.mathematics import GraphAnimator
```

### Formula Examples (REVOLUTIONARY)

```python
# Chemical Formula - Smart positioning
water = Chem("H2O", element_colors={"H": BLUE, "O": RED})
glucose = Chem("C6H12O6", element_colors={"C": GRAY, "H": BLUE, "O": RED})
iron_ion = Chem("Fe3+", element_colors={"Fe": ORANGE})  # Charge as superscript

# Physics Formula - Full atomic control
snells_law = Formula(
    Term("n", sub="1", color=BLUE, sub_color=TEAL, size=50),
    Term("sin", color=WHITE, size=40),
    Term("theta", greek=True, sub="1", color=YELLOW, sub_color=ORANGE, size=50),
    Op("=", color=WHITE, size=50),
    Term("n", sub="2", color=GREEN, sub_color=TEAL, size=50),
    Term("sin", color=WHITE, size=40),
    Term("theta", greek=True, sub="2", color=YELLOW, sub_color=ORANGE, size=50),
    buff=0.15
)

# Pre-built formulas
renderer = FormulaRenderer()
emc2 = renderer.emc2()            # E = mc²
gravity = renderer.gravity()       # F = Gm₁m₂/r²
quadratic = renderer.quadratic()   # x = (-b ± √(b²-4ac)) / 2a
```

---

## THE 7 PILLARS OF REVOLUTIONARY CONTENT

### 1. CORE ANALOGY (Not Textbook!)

Every concept needs a **unique metaphor** that sticks:

| Concept | BAD (Textbook) | GOOD (Revolutionary) |
|---------|----------------|----------------------|
| Carbocation | "Positively charged carbon" | "Desperate single at party - will grab anyone!" |
| Mitochondria | "Powerhouse of cell" | "Cell's Bitcoin mining rig - burns fuel for energy tokens" |
| Snell's Law | "n₁sinθ₁ = n₂sinθ₂" | "Light is lazy - takes fastest path, not shortest" |
| DNA Helix | "Double helix structure" | "Nature's USB drive - stores 215 petabytes per gram" |

### 2. SUBCONSCIOUS HOOKS

What psychological trigger makes them NEED to watch?

- **FOMO**: "99% students get this WRONG in JEE!"
- **Identity Challenge**: "Only REAL chemistry students know this..."
- **Curiosity Gap**: "Ice FLOATS... but EVERY other solid SINKS. क्यों?"
- **Mind-Blow**: "Your DNA shares 50% with a BANANA"

### 3. VISUAL-FIRST DESIGN

Animation should explain BEFORE audio does:

```python
# BAD: Text first, then animation
title = Text("Carbon has 4 valence electrons")
self.play(Write(title))
# ... animation later

# GOOD: Animation first, text reinforces
carbon = Chem("C", size=80, color=GRAY)
electrons = [Dot(color=YELLOW) for _ in range(4)]
# Animate electrons appearing around carbon
self.play(Create(carbon))
self.play(LaggedStart(*[FadeIn(e) for e in electrons]))
# THEN add label
label = Text("4 hands = 4 bonds!", font_size=36)
```

### 4. PROGRESSIVE REVELATION

Never show everything at once. Build understanding layer by layer:

```python
# Step 1: Show the question
question = Text("Why does ice float?", color=YELLOW)
self.play(Write(question))
self.wait(1)

# Step 2: Show the expected
water = Chem("H2O", color=BLUE)
ice = water.copy().set_color(WHITE)
self.play(ice.animate.shift(DOWN))  # Ice "should" sink
self.play(Flash(ice, color=RED))    # But wait!

# Step 3: Reveal the truth
self.play(ice.animate.shift(UP * 2))  # Ice actually floats!
secret = Text("SECRET: Hydrogen bonding!", color=GREEN)
```

### 5. 6+ COLOR VARIETY

Monotone = boring. Use colors strategically:

```python
# Color meanings (consistent across all reels)
CONCEPTS = {
    "main_element": BLUE,
    "secondary_element": GREEN,
    "subscript": TEAL,
    "superscript": ORANGE,
    "highlight": YELLOW,
    "warning": RED,
    "success": GREEN,
    "neutral": WHITE,
    "background_accent": PURPLE,
}
```

### 6. DYNAMIC ANIMATIONS (Not Static!)

Every object should MOVE with purpose:

```python
# BAD: Static appearance
formula = Chem("H2O")
self.add(formula)

# GOOD: Dynamic entrance with meaning
formula = Chem("H2O", element_colors={"H": BLUE, "O": RED})
self.play(formula.write_sequence(lag_ratio=0.3))  # Each char appears
self.play(formula.animate.scale(1.2).set_color(YELLOW))  # Highlight
self.play(formula.animate.scale(1/1.2))  # Return
```

### 7. EXAM RELEVANCE

Every video MUST connect to JEE/NEET:

```python
# Segment: Exam tip
exam_tip = VGroup(
    Text("JEE 2024 asked THIS!", color=RED, font_size=40),
    Text("Critical angle = 42° for glass", font_size=32),
    Text("याद रखो: sin θc = 1/n", font_size=28, color=YELLOW)
).arrange(DOWN, buff=0.3)
self.play(FadeIn(exam_tip))
```

---

## SEGMENT STRUCTURE (7 Segments)

Each reel follows this proven structure:

| Segment | Duration | Purpose | Emotion |
|---------|----------|---------|---------|
| `01_hook` | 3-5s | Grab attention | SHOCK |
| `02_setup` | 5-8s | Set up problem | CURIOSITY |
| `03_content_a` | 10-15s | Main education pt 1 | LEARNING |
| `04_content_b` | 10-15s | Main education pt 2 | BUILDING |
| `05_reveal` | 5-8s | Aha moment | TRIUMPH |
| `06_exam_tip` | 5-8s | JEE/NEET relevance | URGENCY |
| `07_cta` | 3-5s | Follow/register | WARM |

**Total: 45-65 seconds optimal**

---

## HINGLISH RULES (ENFORCED BY CI)

| Category | Rule | Example |
|----------|------|---------|
| Hindi words | Devanagari ONLY | भाई (not BHAI) |
| Technical terms | English | angle, reflection, hybridization |
| Greek letters | Devanagari | θ → थीटा |
| Trig functions | Phonetic | sine → sign |
| Acronyms | Hyphenated | J-E-E, A-T-P, D-N-A |
| Numbers | English spelled | forty two (not 42, not बयालीस) |

---

## BRAND ELEMENTS (MANDATORY)

### Watermark
```python
from jeetlo_style import create_brand_watermark
watermark = create_brand_watermark()  # Bottom-right flame + JeetLo
self.add(watermark)
```

### CTA Slide
```python
from jeetlo_style import add_cta_slide_chemistry  # or _physics, _biology, _mathematics
# Call at the end of segment_07_cta
add_cta_slide_chemistry(self, timing['duration'])
```

### Colors by Subject
| Subject | Primary | Background |
|---------|---------|------------|
| Physics | #0066FF | #0A1A3F |
| Chemistry | #00CC66 | #0A2F1F |
| Biology | #CC66FF | #2A1A3F |
| Mathematics | #FF9900 | #3F2A0A |

---

## CODE TEMPLATE

```python
import sys
sys.path.insert(0, '/Users/pran/Projects/libraries/manim-edu')
sys.path.append('/Users/pran/Projects/ace/content-factory/brands/jeetlo/shared')

from manim import *
from jeetlo_style import JeetLoReelMixin, create_brand_watermark, add_cta_slide_chemistry
from manim_edu.formulas import Chem, Formula, Term, Op, FormulaRenderer

class ChemistryReel(JeetLoReelMixin, Scene):
    subject = "chemistry"

    def construct(self):
        self.camera.background_color = '#0A2F1F'
        self.add(create_brand_watermark())

        import json
        with open('audio/timings.json') as f:
            self.timings = json.load(f)

        for seg in self.timings:
            method = getattr(self, f"segment_{seg['id']}", None)
            if method:
                method(seg)

    def segment_01_hook(self, timing):
        duration = timing['duration']

        # REVOLUTIONARY: Visual first!
        water = Chem("H2O", size=80, element_colors={"H": BLUE, "O": RED})
        self.play(FadeIn(water), run_time=0.5)

        # Animate the subscript
        self.play(water.animate.scale(1.3), run_time=0.3)

        hook_text = Text("Ice FLOATS... but WHY?", font_size=48, color=YELLOW)
        hook_text.to_edge(DOWN, buff=1)
        self.play(Write(hook_text), run_time=0.8)

        self.wait(duration - 1.6)
        self.play(FadeOut(water), FadeOut(hook_text))

    def segment_07_cta(self, timing):
        add_cta_slide_chemistry(self, timing['duration'])
```

---

## VALIDATION CHECKLIST

Before CI accepts your reel:

- [ ] Uses manim-edu for ALL formulas (no MathTex/LaTeX)
- [ ] SmartUnit/Chem for chemical formulas
- [ ] Term/Formula for physics/math equations
- [ ] 6+ colors used
- [ ] Dynamic animations (no static .add())
- [ ] Brand watermark present
- [ ] CTA slide at end
- [ ] Hindi in Devanagari (audio script)
- [ ] English only on screen (video)
- [ ] Duration matches audio (±1s)

---

## THE ULTIMATE GOAL

Every video should make the student say:

> "Why didn't my teacher explain it like THIS?!"

That's the standard. Nothing less.

---

*Created by JeetLo Factory - जीत लो!*
