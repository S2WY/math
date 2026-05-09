import json
import os
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "progress.json")

TARGETED_QUESTIONS = {
    "sign error": [
        {
            "question": "What is the sign of cos(240°)? (positive or negative)",
            "answer": "negative",
            "accept": ["negative", "neg", "-"],
            "explanation": "240° is in Q3. In Q3, only tan is positive; sin and cos are both negative.",
        },
        {
            "question": "What is the sign of sin(315°)? (positive or negative)",
            "answer": "negative",
            "accept": ["negative", "neg", "-"],
            "explanation": "315° is in Q4. In Q4, only cos is positive; sin is negative.",
        },
        {
            "question": "Is tan(150°) positive or negative?",
            "answer": "negative",
            "accept": ["negative", "neg", "-"],
            "explanation": "150° is in Q2. In Q2, only sin is positive; tan is negative.",
        },
    ],
    "forgot formula": [
        {
            "question": "State the Pythagorean Identity for sin and cos.",
            "answer": "sin²θ + cos²θ = 1",
            "accept": ["sin^2+cos^2=1", "sin²θ+cos²θ=1"],
            "explanation": "sin²(θ) + cos²(θ) = 1. This comes from the unit circle: x² + y² = 1.",
        },
        {
            "question": "What is the formula for the period of y = sin(bx)?",
            "answer": "2π/b",
            "accept": ["2pi/b", "360/b"],
            "explanation": "Period = 2π/b. Larger b → shorter period (faster oscillation).",
        },
    ],
    "wrong quadrant": [
        {
            "question": "In which two quadrants is sin(θ) positive?",
            "answer": "Q1 and Q2",
            "accept": ["1 and 2", "q1 and q2", "quadrant 1 and 2"],
            "explanation": "sin = y-coordinate. y is positive in Q1 (upper right) and Q2 (upper left).",
        },
        {
            "question": "In which two quadrants is cos(θ) negative?",
            "answer": "Q2 and Q3",
            "accept": ["2 and 3", "q2 and q3", "quadrant 2 and 3"],
            "explanation": "cos = x-coordinate. x is negative in Q2 (left side) and Q3 (lower left).",
        },
        {
            "question": "What is the reference angle for 330°?",
            "answer": "30",
            "accept": ["30°", "30 degrees"],
            "explanation": "330° is in Q4. Reference angle = 360° − 330° = 30°.",
        },
    ],
    "unit conversion error": [
        {
            "question": "Convert 270° to radians.",
            "answer": "3π/2",
            "accept": ["3pi/2", "4.712"],
            "explanation": "270 × (π/180) = 270π/180 = 3π/2.",
        },
        {
            "question": "Convert π/3 to degrees.",
            "answer": "60",
            "accept": ["60°", "60 degrees"],
            "explanation": "(π/3) × (180/π) = 180/3 = 60°.",
        },
    ],
    "graphing error": [
        {
            "question": "What is the amplitude of y = −5cos(x)?",
            "answer": "5",
            "accept": ["5", "|-5|"],
            "explanation": "Amplitude = |a| = |−5| = 5. The negative sign reflects the graph, but does NOT change the amplitude.",
        },
        {
            "question": "What is the period of y = sin(4x)?",
            "answer": "π/2",
            "accept": ["pi/2", "90"],
            "explanation": "Period = 2π/b = 2π/4 = π/2.",
        },
    ],
    "conceptual misunderstanding": [
        {
            "question": "Solve: sin(θ) = 0 for 0° ≤ θ ≤ 360°. List all solutions.",
            "answer": "0, 180, 360",
            "accept": ["0° 180° 360°", "0,180,360"],
            "explanation": "sin(θ) = 0 at θ = 0°, 180°, 360° — wherever the y-coordinate is 0 on the unit circle.",
        },
    ],
}


def _normalize(s: str) -> str:
    return s.strip().lower().replace("°", "").replace(" ", "").replace("degrees", "")


def _check(user: str, q: dict) -> bool:
    norm = _normalize(user)
    if norm == _normalize(q["answer"]):
        return True
    return any(norm == _normalize(str(a)) for a in q.get("accept", []))


def run_mistake_review() -> None:
    with open(DATA_PATH) as f:
        data = json.load(f)

    mistakes = data.get("mistakes", [])
    if not mistakes:
        print("\n  No mistakes recorded yet. Complete a quiz or test first.")
        return

    categories = {}
    for m in mistakes:
        c = m["category"]
        categories[c] = categories.get(c, 0) + 1

    top_categories = sorted(categories.items(), key=lambda x: -x[1])

    print(f"\n{'=' * 60}")
    print("  MISTAKE REVIEW SESSION")
    print("=" * 60)
    print("\n  Your top mistake categories:")
    for cat, count in top_categories:
        print(f"    • {cat}: {count} mistake(s)")

    print("\n  We'll practice targeted questions for your weak areas.")
    print("=" * 60)

    total = 0
    correct_count = 0

    for cat, _ in top_categories:
        qs = TARGETED_QUESTIONS.get(cat, [])
        if not qs:
            continue

        print(f"\n--- Targeting: {cat.upper()} ---")
        for q in qs:
            total += 1
            print(f"\n  Q: {q['question']}")
            ans = input("  Your answer: ").strip()
            if _check(ans, q):
                print("  ✓ Correct!")
                correct_count += 1
            else:
                print(f"  ✗ Incorrect. Answer: {q['answer']}")
            print(f"  Explanation: {q['explanation']}")
            input("  Press Enter to continue...")

    if total:
        pct = round(correct_count / total * 100)
        print(f"\n{'=' * 60}")
        print(f"  Review complete: {correct_count}/{total} ({pct}%)")
        if pct >= 80:
            print("  You're improving! Keep it up.")
        else:
            print("  Keep reviewing — run this again after studying the guide.")
        print("=" * 60)


def show_mistake_log() -> None:
    with open(DATA_PATH) as f:
        data = json.load(f)

    mistakes = data.get("mistakes", [])
    if not mistakes:
        print("\n  No mistakes recorded yet.")
        return

    print(f"\n{'=' * 60}")
    print(f"  MISTAKE LOG ({len(mistakes)} total)")
    print("=" * 60)

    recent = mistakes[-10:]
    for i, m in enumerate(reversed(recent), 1):
        date = m["date"][:10]
        print(f"\n  {i}. [{date}] {m['category'].upper()}")
        print(f"     Topic: {m['subtopic']}")
        print(f"     Q: {m['question'][:60]}")
        print(f"     Your answer: {m['user_answer']}  |  Correct: {m['correct_answer']}")

    print("\n" + "=" * 60)
