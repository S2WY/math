import json
import os
import random

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "flashcards.json")


def load_flashcards() -> dict:
    with open(DATA_PATH) as f:
        return json.load(f)


def save_flashcards(data: dict) -> None:
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def get_cards(topic: str, difficulty: str | None = None) -> list[dict]:
    data = load_flashcards()
    cards = data.get(topic, [])
    if difficulty:
        cards = [c for c in cards if c.get("difficulty") == difficulty]
    return cards


def run_flashcard_session(topic: str, difficulty: str | None = None) -> None:
    cards = get_cards(topic, difficulty)
    if not cards:
        print(f"No flashcards found for topic '{topic}'.")
        return

    random.shuffle(cards)
    total = len(cards)
    print(f"\n{'=' * 60}")
    print(f"  FLASHCARD SESSION: {topic}")
    if difficulty:
        print(f"  Difficulty: {difficulty.upper()}")
    print(f"  {total} cards total. Press Enter to flip each card.")
    print("=" * 60)

    for i, card in enumerate(cards, 1):
        print(f"\n[Card {i}/{total}] — {card.get('topic', '')}")
        print("─" * 60)
        print("FRONT:")
        print(f"  {card['front']}")
        input("\n  Press Enter to see the answer...")
        print("\nBACK:")
        for line in card["back"].split("\n"):
            print(f"  {line}")

        rating = _ask_rating()
        if rating == "q":
            print("\nSession ended early.")
            break
        print()

    print("\n" + "=" * 60)
    print("  Flashcard session complete!")
    print("=" * 60)


def _ask_rating() -> str:
    while True:
        choice = input(
            "\n  How did you do? [1=Didn't know  2=Got it  q=Quit] > "
        ).strip().lower()
        if choice in ("1", "2", "q"):
            return choice
        print("  Enter 1, 2, or q.")


def add_custom_card(topic: str, front: str, back: str, difficulty: str = "medium") -> None:
    data = load_flashcards()
    if topic not in data:
        data[topic] = []
    existing_ids = [c["id"] for cards in data.values() for c in cards]
    new_id = f"custom_{len(existing_ids) + 1:03d}"
    data[topic].append({
        "id": new_id,
        "front": front,
        "back": back,
        "topic": topic,
        "difficulty": difficulty,
        "custom": True,
    })
    save_flashcards(data)
    print(f"Card added with ID {new_id}.")
