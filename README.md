# Math Tutor Bot

A command-line study system for math — starting with **Pre-Calculus 11 Trigonometry**.

## Features (v1.0)

| Feature | Status |
|---|---|
| Study Guide | ✅ Full 7-section guide with formulas, examples, common mistakes |
| Flashcards | ✅ 15 cards, filterable by difficulty, shuffle mode |
| Quiz Mode | ✅ Easy / Medium / Hard / Mixed, auto-graded with explanations |
| Test Mode | ✅ 10-question mixed test, letter grade, full answer key |
| Mistake Review | ✅ Categorized mistakes, targeted drill questions |
| Progress Tracking | ✅ Scores, weak areas, mastery tracking, recommendations |
| File Upload | ✅ Analyze .txt notes — detect topic, extract formulas & key terms |
| Custom Flashcards | ✅ Add your own cards |

## Quick Start — Web App (recommended)

```bash
pip install streamlit
cd math_tutor_bot
streamlit run streamlit_app.py
```

Then open **http://localhost:8501** in your browser.

## Quick Start — Terminal (CLI)

```bash
cd math_tutor_bot
python3 main.py
```

## Project Structure

```
math_tutor_bot/
├── main.py                   # Entry point / main menu
├── data/
│   ├── topics.json           # Topic & subtopic registry
│   ├── flashcards.json       # All flashcard content
│   ├── quizzes.json          # All quiz/test questions
│   └── progress.json         # User progress (auto-saved)
├── modules/
│   ├── study_guides.py       # Full study guide content & renderer
│   ├── flashcards.py         # Flashcard session logic
│   ├── quizzes.py            # Quiz engine
│   ├── tests.py              # Test engine with answer key
│   ├── progress_tracker.py   # Score tracking, mastery, recommendations
│   ├── mistake_review.py     # Mistake log & targeted drills
│   └── file_reader.py        # Upload & analyze .txt notes
└── uploads/                  # Drop .txt notes here for analysis
```

## File Upload

Place any `.txt` file in `math_tutor_bot/uploads/` and select option 7 from
the main menu. The app will:
- Detect the math topic
- Extract formulas
- Identify key terms and question types

## Adding a New Topic

1. Add questions to `data/quizzes.json` under a new topic key
2. Add flashcards to `data/flashcards.json` under the same key
3. Add a study guide dict to `modules/study_guides.py` in `STUDY_GUIDES`
4. The menus will automatically pick it up

## Roadmap

- [ ] Algebra, Quadratics, Calculus guides
- [ ] Streamlit web interface
- [ ] PDF/image upload support
- [ ] Spaced repetition scheduling for flashcards
- [ ] AI-generated personalized questions
