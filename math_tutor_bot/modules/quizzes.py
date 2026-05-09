import json
import os
import random
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "quizzes.json")


def load_quizzes() -> dict:
    with open(DATA_PATH) as f:
        return json.load(f)


def _normalize(s: str) -> str:
    return s.strip().lower().replace("°", "").replace(" ", "").replace("degrees", "")


def _check_answer(user: str, question: dict) -> bool:
    norm_user = _normalize(user)
    correct = _normalize(question["answer"])
    if norm_user == correct:
        return True
    for alt in question.get("accept", []):
        if norm_user == _normalize(str(alt)):
            return True
    return False


def _present_question(q: dict, num: int, total: int) -> tuple[bool, str]:
    print(f"\n[Question {num}/{total}] ({q['type'].replace('_', ' ').title()}) — {q.get('topic', '')}")
    print("─" * 60)
    print(f"  {q['question']}")

    if q["type"] == "multiple_choice":
        print()
        for choice in q.get("choices", []):
            print(f"    {choice}")
        print()
        user_ans = input("  Your answer (A/B/C/D): ").strip().upper()
    else:
        print()
        user_ans = input("  Your answer: ").strip()

    correct = _check_answer(user_ans, q)

    if correct:
        print("\n  ✓ Correct!")
    else:
        print(f"\n  ✗ Incorrect. Correct answer: {q['answer']}")

    print(f"\n  Explanation: {q['explanation']}")
    return correct, user_ans


def run_quiz(topic: str, difficulty: str = "medium", num_questions: int = 5) -> dict:
    data = load_quizzes()
    topic_data = data.get(topic, {})
    pool = topic_data.get(difficulty, [])

    if not pool:
        print(f"No {difficulty} questions found for '{topic}'.")
        return {}

    questions = random.sample(pool, min(num_questions, len(pool)))
    total = len(questions)
    score = 0
    wrong_questions = []
    results = []

    print(f"\n{'=' * 60}")
    print(f"  QUIZ: {topic}")
    print(f"  Difficulty: {difficulty.upper()} | Questions: {total}")
    print("=" * 60)

    for i, q in enumerate(questions, 1):
        correct, user_ans = _present_question(q, i, total)
        if correct:
            score += 1
        else:
            wrong_questions.append({**q, "user_answer": user_ans})
        results.append({"id": q["id"], "correct": correct, "user_answer": user_ans})
        input("\n  Press Enter to continue...")

    pct = round(score / total * 100)
    print(f"\n{'=' * 60}")
    print(f"  QUIZ COMPLETE")
    print(f"  Score: {score}/{total} ({pct}%)")
    if pct >= 80:
        print("  Great work!")
    elif pct >= 60:
        print("  Good effort — review the questions you missed.")
    else:
        print("  Keep practicing — review the study guide and try again.")
    print("=" * 60)

    return {
        "topic": topic,
        "difficulty": difficulty,
        "score": score,
        "total": total,
        "percent": pct,
        "wrong_questions": wrong_questions,
        "results": results,
        "timestamp": datetime.now().isoformat(),
    }


def run_mixed_quiz(topic: str, num_questions: int = 9) -> dict:
    """Pull questions from all difficulty levels."""
    data = load_quizzes()
    topic_data = data.get(topic, {})

    pool = []
    per_level = max(1, num_questions // 3)
    for diff in ("easy", "medium", "hard"):
        qs = topic_data.get(diff, [])
        pool += random.sample(qs, min(per_level, len(qs)))

    random.shuffle(pool)
    total = len(pool)
    if not total:
        print(f"No questions found for '{topic}'.")
        return {}

    score = 0
    wrong_questions = []
    results = []

    print(f"\n{'=' * 60}")
    print(f"  MIXED QUIZ: {topic}")
    print(f"  Questions: {total} (easy + medium + hard)")
    print("=" * 60)

    for i, q in enumerate(pool, 1):
        correct, user_ans = _present_question(q, i, total)
        if correct:
            score += 1
        else:
            wrong_questions.append({**q, "user_answer": user_ans})
        results.append({"id": q["id"], "correct": correct, "user_answer": user_ans})
        input("\n  Press Enter to continue...")

    pct = round(score / total * 100)
    print(f"\n{'=' * 60}")
    print(f"  QUIZ COMPLETE  |  Score: {score}/{total} ({pct}%)")
    print("=" * 60)

    return {
        "topic": topic,
        "difficulty": "mixed",
        "score": score,
        "total": total,
        "percent": pct,
        "wrong_questions": wrong_questions,
        "results": results,
        "timestamp": datetime.now().isoformat(),
    }
