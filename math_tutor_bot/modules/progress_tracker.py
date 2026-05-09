import json
import os
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "progress.json")

MASTERY_THRESHOLD = 80   # % score considered mastered
WEAK_THRESHOLD = 60      # % score considered a weak area


def load_progress() -> dict:
    with open(DATA_PATH) as f:
        return json.load(f)


def save_progress(data: dict) -> None:
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def record_study_session(topic: str) -> None:
    data = load_progress()
    data["session_count"] += 1
    entry = {"topic": topic, "date": datetime.now().isoformat()}
    data["topics_studied"].append(entry)
    save_progress(data)


def record_quiz_result(result: dict) -> None:
    if not result:
        return
    data = load_progress()
    data["quiz_scores"].append(result)

    topic = result["topic"]
    pct = result["percent"]

    if pct >= MASTERY_THRESHOLD and topic not in data["mastered_topics"]:
        data["mastered_topics"].append(topic)
        print(f"\n  🎉 You've mastered '{topic}'!")

    if pct < WEAK_THRESHOLD and topic not in data["weak_areas"]:
        data["weak_areas"].append(topic)

    for wrong in result.get("wrong_questions", []):
        record_mistake(topic, wrong)

    save_progress(data)


def record_test_result(result: dict) -> None:
    if not result:
        return
    data = load_progress()
    data["test_scores"].append(result)

    for wrong in result.get("wrong_questions", []):
        record_mistake(result["topic"], wrong)

    save_progress(data)


def record_mistake(topic: str, question: dict) -> None:
    data = load_progress()
    category = _classify_mistake(question)
    mistake = {
        "topic": topic,
        "question_id": question.get("id", "unknown"),
        "question": question.get("question", "")[:80],
        "correct_answer": question.get("answer", ""),
        "user_answer": question.get("user_answer", ""),
        "category": category,
        "subtopic": question.get("topic", ""),
        "date": datetime.now().isoformat(),
    }
    data["mistakes"].append(mistake)
    save_progress(data)


def _classify_mistake(question: dict) -> str:
    q_text = question.get("question", "").lower()
    subtopic = question.get("topic", "").lower()
    user_ans = str(question.get("user_answer", "")).lower()
    correct = str(question.get("answer", "")).lower()

    if "sign" in user_ans or ("-" in correct and "-" not in user_ans):
        return "sign error"
    if "formula" in q_text or "identity" in q_text:
        return "forgot formula"
    if "quadrant" in q_text or "quadrant" in subtopic:
        return "wrong quadrant"
    if "factor" in q_text or "factor" in subtopic:
        return "factoring mistake"
    if "convert" in q_text or "radian" in q_text:
        return "unit conversion error"
    if "graph" in subtopic or "period" in q_text or "amplitude" in q_text:
        return "graphing error"
    return "conceptual misunderstanding"


def show_progress() -> None:
    data = load_progress()

    print(f"\n{'=' * 60}")
    print("  YOUR PROGRESS REPORT")
    print("=" * 60)

    print(f"\n  Total study sessions: {data['session_count']}")

    topics = [e["topic"] for e in data["topics_studied"]]
    unique_topics = list(dict.fromkeys(topics))
    print(f"  Topics studied ({len(unique_topics)}): {', '.join(unique_topics) or 'none'}")

    print(f"\n  Mastered topics: {', '.join(data['mastered_topics']) or 'none yet'}")
    print(f"  Weak areas:      {', '.join(data['weak_areas']) or 'none identified'}")

    if data["quiz_scores"]:
        recent = data["quiz_scores"][-5:]
        print(f"\n  Recent quiz scores:")
        for r in recent:
            print(f"    {r['topic']} ({r.get('difficulty','')}) — {r['score']}/{r['total']} ({r['percent']}%)")

    if data["test_scores"]:
        recent = data["test_scores"][-3:]
        print(f"\n  Recent test scores:")
        for r in recent:
            print(f"    {r['topic']} — {r['score']}/{r['total']} ({r['percent']}%) — Grade: {r['grade']}")

    if data["mistakes"]:
        print(f"\n  Total mistakes recorded: {len(data['mistakes'])}")
        categories = {}
        for m in data["mistakes"]:
            c = m["category"]
            categories[c] = categories.get(c, 0) + 1
        print("  Mistake breakdown:")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            print(f"    • {cat}: {count}")

    print("\n" + "=" * 60)


def get_recommendations() -> list[str]:
    data = load_progress()
    recs = []

    if data["weak_areas"]:
        recs.append(f"Review weak areas: {', '.join(data['weak_areas'])}")

    categories = {}
    for m in data["mistakes"]:
        c = m["category"]
        categories[c] = categories.get(c, 0) + 1

    top_mistakes = sorted(categories.items(), key=lambda x: -x[1])[:2]
    for cat, _ in top_mistakes:
        if cat == "sign error":
            recs.append("Practice ASTC quadrant signs — you often make sign errors.")
        elif cat == "forgot formula":
            recs.append("Review and memorize key formulas using flashcards.")
        elif cat == "wrong quadrant":
            recs.append("Drill reference angles and quadrant identification.")
        elif cat == "unit conversion error":
            recs.append("Practice converting between degrees and radians.")
        elif cat == "graphing error":
            recs.append("Review graphing transformations: amplitude, period, shifts.")

    if not recs:
        recs.append("Keep up the great work! Try increasing the difficulty.")

    return recs
