STUDY_GUIDES = {
    "Pre-Calculus 11 Trigonometry": {
        "title": "Pre-Calculus 11 Trigonometry",
        "overview": """
Trigonometry is the study of relationships between angles and sides of triangles.
In Pre-Calculus 11, you will extend your understanding beyond right triangles to
include angles of any size, the unit circle, and graphing trigonometric functions.
This topic is foundational for calculus and physics.
        """,
        "key_concepts": [
            "Angles in standard position and reference angles",
            "The unit circle and coordinates",
            "Primary trig ratios: sin, cos, tan",
            "Exact values for special angles (30°, 45°, 60°)",
            "ASTC rule — signs in each quadrant",
            "Converting between degrees and radians",
            "Graphing y = a·sin(bx + c) + d and transformations",
            "Solving trigonometric equations",
            "Applications and word problems",
        ],
        "formulas": {
            "SOH-CAH-TOA": "sin=opp/hyp, cos=adj/hyp, tan=opp/adj",
            "Pythagorean Identity": "sin²θ + cos²θ = 1",
            "Degrees to Radians": "radians = degrees × (π/180)",
            "Radians to Degrees": "degrees = radians × (180/π)",
            "Period of sin/cos": "T = 2π/b",
            "Period of tan": "T = π/b",
            "Reference Angle Q2": "ref = 180° − θ",
            "Reference Angle Q3": "ref = θ − 180°",
            "Reference Angle Q4": "ref = 360° − θ",
        },
        "sections": [
            {
                "name": "1. Angles and Reference Angles",
                "content": """
An angle in STANDARD POSITION has its vertex at the origin with the initial arm
along the positive x-axis. The terminal arm rotates counterclockwise (positive).

REFERENCE ANGLE: the acute angle between the terminal arm and the x-axis.

  Quadrant 1 (0°–90°):   reference angle = θ
  Quadrant 2 (90°–180°): reference angle = 180° − θ
  Quadrant 3 (180°–270°):reference angle = θ − 180°
  Quadrant 4 (270°–360°):reference angle = 360° − θ

ASTC Rule (All Students Take Calculus):
  Q1: All ratios positive
  Q2: Sin positive only
  Q3: Tan positive only
  Q4: Cos positive only

Example: Find the reference angle and trig signs for 240°.
  240° is in Q3.
  Reference angle = 240° − 180° = 60°
  In Q3: tan is positive, sin and cos are negative.
                """,
            },
            {
                "name": "2. Unit Circle Basics",
                "content": """
The unit circle has radius 1, centered at the origin.
Any point (x, y) on the circle satisfies x² + y² = 1.

For an angle θ in standard position:
  x = cos(θ)
  y = sin(θ)

This means: sin²(θ) + cos²(θ) = 1  ← Pythagorean Identity

Key points on the unit circle:
  θ = 0°:   (1, 0)     → cos=1, sin=0
  θ = 90°:  (0, 1)     → cos=0, sin=1
  θ = 180°: (−1, 0)    → cos=−1, sin=0
  θ = 270°: (0, −1)    → cos=0, sin=−1
                """,
            },
            {
                "name": "3. Exact Values for Special Angles",
                "content": """
You must memorize these exact values:

Angle | sin      | cos      | tan
------+----------+----------+--------
0°    | 0        | 1        | 0
30°   | 1/2      | √3/2     | 1/√3 = √3/3
45°   | √2/2     | √2/2     | 1
60°   | √3/2     | 1/2      | √3
90°   | 1        | 0        | undefined

TIP: For sin, read the table top to bottom: 0, 1/2, √2/2, √3/2, 1
     For cos, read the same table bottom to top.

To find values in other quadrants:
  Step 1: Find the reference angle.
  Step 2: Look up the exact value for the reference angle.
  Step 3: Apply the correct sign using ASTC.

Example: sin(300°)
  300° is in Q4 (sin is negative). Reference angle = 360° − 300° = 60°.
  sin(60°) = √3/2.  So sin(300°) = −√3/2.
                """,
            },
            {
                "name": "4. Radians and Degrees",
                "content": """
Radians are another unit for measuring angles.
Full circle = 360° = 2π radians

Conversions:
  Degrees → Radians: multiply by π/180
  Radians → Degrees: multiply by 180/π

Common conversions to memorize:
  0°   = 0      | 30°  = π/6  | 45°  = π/4
  60°  = π/3    | 90°  = π/2  | 120° = 2π/3
  135° = 3π/4   | 150° = 5π/6 | 180° = π
  210° = 7π/6   | 225° = 5π/4 | 240° = 4π/3
  270° = 3π/2   | 300° = 5π/3 | 315° = 7π/4
  330° = 11π/6  | 360° = 2π

Example: Convert 135° to radians.
  135 × (π/180) = 135π/180 = 3π/4
                """,
            },
            {
                "name": "5. Graphing Trig Functions",
                "content": """
Standard form: y = a·sin(b(x − c)) + d

  |a| = amplitude (height from midline to peak)
  b   → period = 2π/b
  c   = horizontal (phase) shift (right if c > 0)
  d   = vertical shift (midline at y = d)
  If a < 0: the graph is reflected over the x-axis.

Key features of y = sin(x):
  Amplitude: 1
  Period: 2π
  Domain: all real numbers
  Range: [−1, 1]
  Zeros at: 0, π, 2π, ...
  Max at: π/2 (value = 1)
  Min at: 3π/2 (value = −1)

Example: Describe y = −3sin(2x) + 1
  Amplitude = 3, reflected over x-axis
  Period = 2π/2 = π
  Vertical shift up 1
  Midline: y = 1, range: [−2, 4]
                """,
            },
            {
                "name": "6. Solving Trig Equations",
                "content": """
General method:
  Step 1: Isolate the trig function.
  Step 2: Find the reference angle using inverse trig.
  Step 3: Determine which quadrants give the correct sign.
  Step 4: Write all solutions in the given range.

Example 1: Solve 2cos(θ) + √3 = 0 for 0° ≤ θ ≤ 360°
  2cos(θ) = −√3
  cos(θ) = −√3/2
  Reference angle: cos⁻¹(√3/2) = 30°
  cos is negative in Q2 and Q3.
  Q2: θ = 180° − 30° = 150°
  Q3: θ = 180° + 30° = 210°
  Answer: θ = 150° or θ = 210°

Example 2: Solve sin(θ) = 0.5 for 0° ≤ θ ≤ 360°
  Reference angle = 30°
  sin is positive in Q1 and Q2.
  Answer: θ = 30° or θ = 150°
                """,
            },
            {
                "name": "7. Word Problems",
                "content": """
Trig is used to find unknown sides or angles in triangles.

Right triangle problems use SOH-CAH-TOA:
  sin(θ) = opp/hyp → opp = hyp × sin(θ)
  cos(θ) = adj/hyp → adj = hyp × cos(θ)
  tan(θ) = opp/adj → opp = adj × tan(θ)

Angle of elevation: angle measured upward from horizontal.
Angle of depression: angle measured downward from horizontal.

Example: A person stands 50 m from a building.
The angle of elevation to the top is 40°.
How tall is the building?

  tan(40°) = height / 50
  height = 50 × tan(40°)
  height ≈ 50 × 0.839 ≈ 41.95 m
                """,
            },
        ],
        "common_mistakes": [
            "Forgetting to apply the sign from ASTC (e.g., cos is negative in Q2 and Q3)",
            "Finding only one solution when two solutions exist in [0°, 360°]",
            "Mixing up sin and cos when converting (remember sin is y, cos is x)",
            "Using degrees on a calculator when the problem needs radians (or vice versa)",
            "Forgetting that tan is undefined at 90° and 270°",
            "Confusing period formula: period = 2π/b, not 2πb",
            "Misidentifying the quadrant of a negative angle",
        ],
        "worked_examples": [
            {
                "problem": "Find all values of θ in [0°, 360°] where tan(θ) = −1.",
                "solution": """
Step 1: Find reference angle. tan⁻¹(1) = 45°.
Step 2: tan is negative in Q2 and Q4.
Step 3: Q2 answer: θ = 180° − 45° = 135°
        Q4 answer: θ = 360° − 45° = 315°
Answer: θ = 135° or θ = 315°
                """,
            },
            {
                "problem": "The point P(−3, 4) is on the terminal arm of angle θ. Find sin(θ), cos(θ), tan(θ).",
                "solution": """
Step 1: Find r (distance from origin).
        r = √(x² + y²) = √(9 + 16) = √25 = 5
Step 2: Apply definitions.
        sin(θ) = y/r = 4/5
        cos(θ) = x/r = −3/5
        tan(θ) = y/x = 4/(−3) = −4/3
Note: P is in Q2, so sin > 0, cos < 0, tan < 0. ✓
                """,
            },
        ],
        "practice_questions": [
            "1. Find the reference angle for each: a) 100°  b) 250°  c) 320°",
            "2. Determine the exact value of cos(120°).",
            "3. Determine the exact value of sin(330°).",
            "4. Convert 5π/6 to degrees.",
            "5. The point (−5, 12) is on the terminal arm. Find sin, cos, and tan.",
            "6. Solve 2sin(θ) − √3 = 0 for 0° ≤ θ ≤ 360°.",
            "7. A ramp rises 3 m over a horizontal distance of 8 m. Find the angle of inclination.",
        ],
        "challenge_questions": [
            "1. Solve 2cos²(θ) − cos(θ) − 1 = 0 for 0° ≤ θ ≤ 360°.",
            "2. Sketch one full cycle of y = 2sin(3x − π/2) + 1. Label key points.",
            "3. Prove: (sin θ / cos θ) + (cos θ / sin θ) = 1 / (sin θ cos θ).",
        ],
        "summary": """
KEY TAKEAWAYS for Pre-Calculus 11 Trigonometry:

1. SOH-CAH-TOA defines the three primary trig ratios.
2. Reference angles convert any angle to an acute angle (0°–90°).
3. ASTC tells you the sign of each ratio in each quadrant.
4. Know exact values for 0°, 30°, 45°, 60°, 90° without a calculator.
5. Radians and degrees are two ways to measure angles; use π/180 to convert.
6. The Pythagorean Identity sin²θ + cos²θ = 1 is always true.
7. Graphing y = a·sin(bx + c) + d requires knowing amplitude, period, phase shift, vertical shift.
8. Trig equations usually have two solutions in [0°, 360°].

Study tip: Practice drawing the unit circle from memory and labelling all special angles.
        """,
    }
}


def get_study_guide(topic: str) -> dict | None:
    return STUDY_GUIDES.get(topic)


def list_available_guides() -> list[str]:
    return list(STUDY_GUIDES.keys())


def print_study_guide(topic: str) -> None:
    guide = get_study_guide(topic)
    if not guide:
        print(f"No study guide found for '{topic}'.")
        print(f"Available guides: {', '.join(list_available_guides())}")
        return

    width = 72
    print("=" * width)
    print(f"  STUDY GUIDE: {guide['title'].upper()}")
    print("=" * width)

    print("\n--- OVERVIEW ---")
    print(guide["overview"].strip())

    print("\n--- KEY CONCEPTS ---")
    for i, concept in enumerate(guide["key_concepts"], 1):
        print(f"  {i}. {concept}")

    print("\n--- FORMULAS ---")
    for name, formula in guide["formulas"].items():
        print(f"  {name}: {formula}")

    for section in guide["sections"]:
        print(f"\n{'─' * width}")
        print(f"  {section['name']}")
        print("─" * width)
        print(section["content"].strip())

    print(f"\n{'=' * width}")
    print("  COMMON MISTAKES TO AVOID")
    print("=" * width)
    for mistake in guide["common_mistakes"]:
        print(f"  • {mistake}")

    print(f"\n{'=' * width}")
    print("  WORKED EXAMPLES")
    print("=" * width)
    for i, ex in enumerate(guide["worked_examples"], 1):
        print(f"\nExample {i}: {ex['problem']}")
        print(ex["solution"].strip())

    print(f"\n{'=' * width}")
    print("  PRACTICE QUESTIONS")
    print("=" * width)
    for q in guide["practice_questions"]:
        print(f"  {q}")

    print(f"\n{'=' * width}")
    print("  CHALLENGE QUESTIONS")
    print("=" * width)
    for q in guide["challenge_questions"]:
        print(f"  {q}")

    print(f"\n{'=' * width}")
    print("  SUMMARY")
    print("=" * width)
    print(guide["summary"].strip())
    print("=" * width)
