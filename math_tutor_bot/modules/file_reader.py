import os
import re

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")


def list_uploaded_files() -> list[str]:
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    return [f for f in os.listdir(UPLOADS_DIR) if not f.startswith(".")]


def read_text_file(filename: str) -> str:
    path = os.path.join(UPLOADS_DIR, filename)
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


def analyze_notes(text: str) -> dict:
    text_lower = text.lower()

    topic = _detect_topic(text_lower)
    formulas = _extract_formulas(text)
    key_terms = _extract_key_terms(text_lower)
    question_hints = _detect_question_types(text_lower)

    return {
        "detected_topic": topic,
        "formulas_found": formulas,
        "key_terms": key_terms,
        "question_types_detected": question_hints,
        "word_count": len(text.split()),
    }


def _detect_topic(text: str) -> str:
    topic_keywords = {
        "Trigonometry": ["sin", "cos", "tan", "angle", "radian", "degree", "hypotenuse", "soh-cah-toa"],
        "Quadratics": ["quadratic", "parabola", "vertex", "discriminant", "x²", "ax^2"],
        "Algebra": ["variable", "equation", "solve for x", "linear", "slope"],
        "Calculus": ["derivative", "integral", "limit", "differentiate"],
        "Statistics": ["mean", "median", "mode", "standard deviation", "probability"],
        "Geometry": ["triangle", "circle", "perimeter", "area", "polygon"],
        "Polynomials": ["polynomial", "degree", "coefficient", "monomial"],
        "Factoring": ["factor", "gcf", "trinomial", "difference of squares"],
    }
    scores = {topic: 0 for topic in topic_keywords}
    for topic, keywords in topic_keywords.items():
        for kw in keywords:
            scores[topic] += text.count(kw)

    best = max(scores, key=lambda t: scores[t])
    return best if scores[best] > 0 else "Unknown"


def _extract_formulas(text: str) -> list[str]:
    formula_pattern = re.compile(
        r"[A-Za-z²³√±][^.\n]{0,60}[=≈][^.\n]{0,60}"
    )
    raw = formula_pattern.findall(text)
    seen = set()
    formulas = []
    for f in raw:
        f = f.strip()
        if f and f not in seen and len(f) > 3:
            seen.add(f)
            formulas.append(f)
    return formulas[:15]


def _extract_key_terms(text: str) -> list[str]:
    math_terms = [
        "amplitude", "period", "frequency", "phase shift", "vertical shift",
        "reference angle", "quadrant", "unit circle", "pythagorean",
        "sin", "cos", "tan", "radian", "degree", "exact value",
        "vertex", "parabola", "discriminant", "derivative", "integral",
        "slope", "intercept", "domain", "range", "function",
        "factor", "polynomial", "coefficient", "asymptote",
    ]
    found = [t for t in math_terms if t in text]
    return found


def _detect_question_types(text: str) -> list[str]:
    types = []
    if any(w in text for w in ["solve", "find", "calculate", "evaluate"]):
        types.append("calculation")
    if any(w in text for w in ["true/false", "multiple choice", "a)", "b)", "c)"]):
        types.append("multiple choice")
    if any(w in text for w in ["word problem", "a ladder", "a person", "a building", "a car"]):
        types.append("word problems")
    if any(w in text for w in ["prove", "show that", "verify"]):
        types.append("proof")
    if any(w in text for w in ["sketch", "graph", "draw"]):
        types.append("graphing")
    return types


def process_uploaded_file(filename: str) -> None:
    text = read_text_file(filename)
    if not text:
        print(f"\n  File '{filename}' not found or empty in uploads/ folder.")
        print(f"  Place your .txt notes in: math_tutor_bot/uploads/")
        return

    print(f"\n{'=' * 60}")
    print(f"  ANALYZING: {filename}")
    print("=" * 60)

    analysis = analyze_notes(text)

    print(f"\n  Detected topic:   {analysis['detected_topic']}")
    print(f"  Word count:       {analysis['word_count']}")

    if analysis["key_terms"]:
        print(f"\n  Key terms found:  {', '.join(analysis['key_terms'][:8])}")

    if analysis["formulas_found"]:
        print(f"\n  Formulas extracted ({len(analysis['formulas_found'])}):")
        for f in analysis["formulas_found"][:8]:
            print(f"    • {f}")

    if analysis["question_types_detected"]:
        print(f"\n  Question types detected: {', '.join(analysis['question_types_detected'])}")

    print(f"\n  Note: Upload support currently reads .txt files.")
    print(f"  Place your notes in math_tutor_bot/uploads/ as .txt files.")
    print("=" * 60)
