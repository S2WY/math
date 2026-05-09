import json
import os
import random
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "quizzes.json")

GRADE_SCALE = [
    (90, "A — Excellent"),
    (80, "B — Good"),
    (70, "C — Satisfactory"),
    (60, "D — Needs Improvement"),
    (0, "F — Please review the study guide and retry"),
]


def _normalize(s: str) -> str:
    return s.strip().lower().replace("°", "").replace(" ", "").replace("degrees", "")


def _check_answer(user: str, question: dict) -> bool:
    norm_user = _normalize(user)
    if norm_user == _normalize(question["answer"]):
        return True
    for alt in question.get("accept", []):
        if norm_user == _normalize(str(alt)):
            return True
    return False


def _get_grade(pct: int) -> str:
    for threshold, label in GRADE_SCALE:
        if pct >= threshold:
            return label
    return "F"


def run_test(topic: str, easy: int = 3, medium: int = 4, hard: int = 3) -> dict:
    with open(DATA_PATH) as f:
        data = json.load(f)

    topic_data = data.get(topic, {})
    easy_pool = topic_data.get("easy", [])
    medium_pool = topic_data.get("medium", [])
    hard_pool = topic_data.get("hard", [])

    selected_easy = random.sample(easy_pool, min(easy, len(easy_pool)))
    selected_med = random.sample(medium_pool, min(medium, len(medium_pool)))
    selected_hard = random.sample(hard_pool, min(hard, len(hard_pool)))

    questions = (
        [(q, "Easy") for q in selected_easy]
        + [(q, "Medium") for q in selected_med]
        + [(q, "Hard") for q in selected_hard]
    )

    total = len(questions)
    if not total:
        print(f"No test questions available for '{topic}'.")
        return {}

    print(f"\n{'=' * 65}")
    print(f"  MATH TEST: {topic}")
    print(f"  {len(selected_easy)} Easy  |  {len(selected_med)} Medium  |  {len(selected_hard)} Hard")
    print(f"  Total: {total} questions")
    print(f"\n  Answer each question. Results and explanations shown at end.")
    print("=" * 65)
    input("\n  Press Enter to begin the test...")

    user_answers = []

    for i, (q, diff_label) in enumerate(questions, 1):
        print(f"\n[{i}/{total}] [{diff_label}] ({q['type'].replace('_', ' ').title()})")
        print("─" * 65)
        print(f"  {q['question']}")
        if q["type"] == "multiple_choice":
            print()
            for choice in q.get("choices", []):
                print(f"    {choice}")
            print()
            ans = input("  Answer (A/B/C/D): ").strip().upper()
        else:
            print()
            ans = input("  Answer: ").strip()
        user_answers.append((q, diff_label, ans))

    # --- Results section ---
    print(f"\n\n{'=' * 65}")
    print("  TEST RESULTS — ANSWER KEY & EXPLANATIONS")
    print("=" * 65)

    score = 0
    wrong_questions = []
    results = []

    for i, (q, diff_label, user_ans) in enumerate(user_answers, 1):
        correct = _check_answer(user_ans, q)
        mark = "✓" if correct else "✗"
        if correct:
            score += 1
        else:
            wrong_questions.append({**q, "user_answer": user_ans, "difficulty": diff_label})

        print(f"\n[{i}] [{diff_label}] {mark}  {q['question'][:60]}")
        print(f"     Your answer: {user_ans}")
        if not correct:
            print(f"     Correct answer: {q['answer']}")
        print(f"     Explanation: {q['explanation']}")

        results.append({
            "id": q["id"],
            "difficulty": diff_label,
            "correct": correct,
            "user_answer": user_ans,
        })

    pct = round(score / total * 100)
    grade = _get_grade(pct)

    print(f"\n{'=' * 65}")
    print(f"  FINAL SCORE: {score}/{total} ({pct}%)")
    print(f"  GRADE: {grade}")
    print("=" * 65)

    return {
        "topic": topic,
        "score": score,
        "total": total,
        "percent": pct,
        "grade": grade,
        "wrong_questions": wrong_questions,
        "results": results,
        "timestamp": datetime.now().isoformat(),
    }
