#!/usr/bin/env python3
"""Math Tutor Bot — Pre-Calculus 11 Trigonometry (v1.0)"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from modules.study_guides import print_study_guide, list_available_guides
from modules.flashcards import run_flashcard_session, add_custom_card
from modules.quizzes import run_quiz, run_mixed_quiz
from modules.tests import run_test
from modules.progress_tracker import (
    record_study_session,
    record_quiz_result,
    record_test_result,
    show_progress,
    get_recommendations,
)
from modules.mistake_review import run_mistake_review, show_mistake_log
from modules.file_reader import process_uploaded_file, list_uploaded_files

DEFAULT_TOPIC = "Pre-Calculus 11 Trigonometry"

BANNER = r"""
  __  __       _   _     _____      _
 |  \/  | __ _| |_| |__ |_   _|   _| |_ ___  _ __
 | |\/| |/ _` | __| '_ \  | || | | | __/ _ \| '__|
 | |  | | (_| | |_| | | | | || |_| | || (_) | |
 |_|  |_|\__,_|\__|_| |_| |_| \__,_|\__\___/|_|
  ____        _
 | __ )  ___ | |_
 |  _ \ / _ \| __|
 | |_) | (_) | |_
 |____/ \___/ \__|

  Pre-Calculus 11 Trigonometry Edition  v1.0
"""


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def main_menu() -> None:
    while True:
        print(BANNER)
        print("  MAIN MENU")
        print("  " + "─" * 40)
        print("  1. Study Guide")
        print("  2. Flashcards / Cue Cards")
        print("  3. Quiz Mode")
        print("  4. Test Mode")
        print("  5. Mistake Review")
        print("  6. Progress Report")
        print("  7. Analyze Uploaded Notes")
        print("  8. Add Custom Flashcard")
        print("  0. Exit")
        print()
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            study_guide_menu()
        elif choice == "2":
            flashcard_menu()
        elif choice == "3":
            quiz_menu()
        elif choice == "4":
            test_menu()
        elif choice == "5":
            mistake_menu()
        elif choice == "6":
            progress_menu()
        elif choice == "7":
            upload_menu()
        elif choice == "8":
            custom_card_menu()
        elif choice == "0":
            print("\n  Goodbye! Keep studying! 📐\n")
            sys.exit(0)
        else:
            print("\n  Invalid choice. Please try again.")
            input("  Press Enter to continue...")
        clear()


def study_guide_menu() -> None:
    clear()
    print(f"\n  Available study guides: {', '.join(list_available_guides())}")
    topic = input(f"\n  Topic [default: {DEFAULT_TOPIC}]: ").strip()
    if not topic:
        topic = DEFAULT_TOPIC
    record_study_session(topic)
    print_study_guide(topic)
    input("\n  Press Enter to return to main menu...")


def flashcard_menu() -> None:
    clear()
    print("\n  FLASHCARD OPTIONS")
    print("  1. All cards")
    print("  2. Easy cards only")
    print("  3. Medium cards only")
    print("  4. Hard cards only")
    choice = input("\n  Choose: ").strip()
    diff_map = {"1": None, "2": "easy", "3": "medium", "4": "hard"}
    difficulty = diff_map.get(choice)
    if choice not in diff_map:
        print("  Invalid choice.")
        input("  Press Enter...")
        return
    run_flashcard_session(DEFAULT_TOPIC, difficulty)
    input("\n  Press Enter to return to main menu...")


def quiz_menu() -> None:
    clear()
    print("\n  QUIZ OPTIONS")
    print("  1. Easy quiz (5 questions)")
    print("  2. Medium quiz (5 questions)")
    print("  3. Hard quiz (5 questions)")
    print("  4. Mixed quiz (easy + medium + hard)")
    choice = input("\n  Choose: ").strip()

    result = {}
    if choice == "1":
        result = run_quiz(DEFAULT_TOPIC, "easy", 5)
    elif choice == "2":
        result = run_quiz(DEFAULT_TOPIC, "medium", 5)
    elif choice == "3":
        result = run_quiz(DEFAULT_TOPIC, "hard", 5)
    elif choice == "4":
        result = run_mixed_quiz(DEFAULT_TOPIC, 9)
    else:
        print("  Invalid choice.")
        input("  Press Enter...")
        return

    record_quiz_result(result)

    recs = get_recommendations()
    if recs:
        print("\n  Recommendations:")
        for r in recs:
            print(f"    • {r}")

    input("\n  Press Enter to return to main menu...")


def test_menu() -> None:
    clear()
    print("\n  TEST MODE")
    print("  This test includes easy, medium, and hard questions.")
    print("  Results and explanations are shown after all questions.")
    input("\n  Press Enter to start the test...")

    result = run_test(DEFAULT_TOPIC, easy=3, medium=4, hard=3)
    record_test_result(result)

    recs = get_recommendations()
    if recs:
        print("\n  Recommendations:")
        for r in recs:
            print(f"    • {r}")

    input("\n  Press Enter to return to main menu...")


def mistake_menu() -> None:
    clear()
    print("\n  MISTAKE REVIEW")
    print("  1. Run targeted review session")
    print("  2. Show mistake log")
    choice = input("\n  Choose: ").strip()
    if choice == "1":
        run_mistake_review()
    elif choice == "2":
        show_mistake_log()
    else:
        print("  Invalid choice.")
    input("\n  Press Enter to return to main menu...")


def progress_menu() -> None:
    clear()
    show_progress()
    recs = get_recommendations()
    print("\n  Study Recommendations:")
    for r in recs:
        print(f"    • {r}")
    input("\n  Press Enter to return to main menu...")


def upload_menu() -> None:
    clear()
    files = list_uploaded_files()
    if not files:
        print("\n  No files found in math_tutor_bot/uploads/")
        print("  Add .txt files there and run this again.")
        input("\n  Press Enter to return...")
        return
    print("\n  Files in uploads/:")
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f}")
    choice = input("\n  Enter file number to analyze: ").strip()
    try:
        idx = int(choice) - 1
        process_uploaded_file(files[idx])
    except (ValueError, IndexError):
        print("  Invalid selection.")
    input("\n  Press Enter to return to main menu...")


def custom_card_menu() -> None:
    clear()
    print("\n  ADD CUSTOM FLASHCARD")
    front = input("  Front (question/concept): ").strip()
    back = input("  Back (answer/explanation): ").strip()
    diff = input("  Difficulty [easy/medium/hard, default: medium]: ").strip() or "medium"
    if front and back:
        add_custom_card(DEFAULT_TOPIC, front, back, diff)
    else:
        print("  Card not added — front and back cannot be empty.")
    input("\n  Press Enter to return to main menu...")


if __name__ == "__main__":
    main_menu()
