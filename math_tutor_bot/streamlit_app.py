#!/usr/bin/env python3
"""Cody's Math Lab — Streamlit Web App"""

import streamlit as st
import sys
import os
import json
import random
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.study_guides import get_study_guide, list_available_guides
from modules.progress_tracker import (
    load_progress,
    save_progress,
    record_study_session,
    record_quiz_result,
    record_test_result,
    get_recommendations,
)
from modules.mistake_review import TARGETED_QUESTIONS
from cody import CODY, cody_html, speech_bubble

# ════════════════════════════════════════════════════════════
# PAGE CONFIG  (must be first Streamlit call)
# ════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Cody's Math Lab",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_TOPIC = "Pre-Calculus 11 Trigonometry"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


# ════════════════════════════════════════════════════════════
# DATA HELPERS
# ════════════════════════════════════════════════════════════

@st.cache_data
def _load_json(name: str) -> dict:
    with open(os.path.join(DATA_DIR, name)) as f:
        return json.load(f)


def quiz_pool(topic: str, difficulty: str) -> list[dict]:
    return _load_json("quizzes.json").get(topic, {}).get(difficulty, [])


def all_quiz_questions(topic: str) -> list[dict]:
    data = _load_json("quizzes.json").get(topic, {})
    out = []
    for diff in ("easy", "medium", "hard"):
        for q in data.get(diff, []):
            out.append({**q, "difficulty": diff})
    return out


def flashcard_pool(topic: str) -> list[dict]:
    return _load_json("flashcards.json").get(topic, [])


def _norm(s: str) -> str:
    return str(s).strip().lower().replace("°", "").replace(" ", "").replace("degrees", "")


def check_answer(user: str, q: dict) -> bool:
    n = _norm(user)
    if n == _norm(q["answer"]):
        return True
    return any(n == _norm(str(a)) for a in q.get("accept", []))


# ════════════════════════════════════════════════════════════
# GLOBAL CSS
# ════════════════════════════════════════════════════════════

def inject_css() -> None:
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

/* ── root variables ── */
:root {
  --brown-deep:   #2D1200;
  --brown-dark:   #5C2E0A;
  --brown-mid:    #8B4513;
  --brown-light:  #A0522D;
  --brown-pale:   #D2936A;
  --cream:        #FDF6EE;
  --cream-dark:   #F5E8D5;
  --amber:        #F5A623;
  --green-ok:     #22C55E;
  --red-err:      #EF4444;
  --blue-info:    #3B82F6;
  --text-dark:    #2C1810;
  --text-mid:     #6B3410;
  --radius-lg:    20px;
  --radius-md:    14px;
  --shadow:       0 4px 24px rgba(139,69,19,0.10);
}

/* ── global ── */
html, body, [class*="css"] {
  font-family: 'Nunito', sans-serif !important;
}
.stApp {
  background: var(--cream) !important;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
  background: var(--brown-deep) !important;
  border-right: 2px solid var(--brown-dark) !important;
}
[data-testid="stSidebar"] * {
  color: #F5DEB3 !important;
}
[data-testid="stSidebar"] .stButton > button {
  width: 100% !important;
  background: transparent !important;
  border: 1px solid rgba(245,222,179,0.18) !important;
  color: #F5DEB3 !important;
  border-radius: 12px !important;
  text-align: left !important;
  padding: 10px 16px !important;
  font-size: 0.95rem !important;
  font-weight: 600 !important;
  margin-bottom: 4px !important;
  transition: all 0.18s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(245,222,179,0.12) !important;
  border-color: rgba(245,222,179,0.45) !important;
  transform: translateX(4px) !important;
}

/* ── main buttons ── */
.stButton > button {
  border-radius: var(--radius-md) !important;
  font-family: 'Nunito', sans-serif !important;
  font-weight: 700 !important;
  transition: all 0.18s ease !important;
  border: none !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
}

/* ── cards ── */
.cody-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: 28px 32px;
  box-shadow: var(--shadow);
  border: 1px solid var(--cream-dark);
  margin: 10px 0;
}
.cody-card h3 {
  color: var(--brown-mid) !important;
  margin-top: 0 !important;
}

/* ── nav cards on home page ── */
.nav-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: 28px 20px;
  text-align: center;
  cursor: pointer;
  border: 2px solid var(--cream-dark);
  box-shadow: var(--shadow);
  transition: all 0.22s ease;
  height: 100%;
}
.nav-card:hover {
  transform: translateY(-5px);
  border-color: var(--brown-pale);
  box-shadow: 0 12px 32px rgba(139,69,19,0.18);
}
.nav-card .nav-icon { font-size: 2.4rem; margin-bottom: 10px; }
.nav-card .nav-title { font-size: 1.05rem; font-weight: 800; color: var(--brown-mid); }
.nav-card .nav-desc  { font-size: 0.82rem; color: #888; margin-top: 4px; }

/* ── formula chip ── */
.formula-chip {
  display: inline-block;
  background: #FFF3E0;
  border: 1.5px solid #FFB74D;
  border-radius: 8px;
  padding: 5px 13px;
  margin: 4px 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.88em;
  color: var(--brown-dark);
  font-weight: 600;
}

/* ── concept badge ── */
.concept-badge {
  display: inline-block;
  background: #E8F5E9;
  border: 1.5px solid #81C784;
  border-radius: 20px;
  padding: 4px 14px;
  margin: 3px 3px;
  font-size: 0.82em;
  color: #2E7D32;
  font-weight: 700;
}

/* ── section heading ── */
.section-heading {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--brown-mid);
  border-left: 4px solid var(--amber);
  padding-left: 12px;
  margin: 18px 0 10px;
}

/* ── flashcard ── */
.flashcard {
  border-radius: var(--radius-lg);
  padding: 44px 36px;
  text-align: center;
  min-height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  font-size: 1.2rem;
  font-weight: 700;
  line-height: 1.6;
  box-shadow: 0 10px 40px rgba(0,0,0,0.13);
  margin: 8px 0 20px;
}
.flashcard-front {
  background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
  color: white;
}
.flashcard-back {
  background: linear-gradient(135deg, #1A6B42 0%, #27AE60 100%);
  color: white;
}
.flashcard pre {
  background: rgba(255,255,255,0.15);
  border-radius: 10px;
  padding: 12px 18px;
  font-size: 0.92rem;
  text-align: left;
  white-space: pre-wrap;
  margin-top: 12px;
}

/* ── quiz answer feedback ── */
.answer-correct {
  background: #F0FDF4;
  border: 2px solid var(--green-ok);
  border-radius: var(--radius-md);
  padding: 18px 22px;
  margin: 10px 0;
  color: #166534;
  font-weight: 600;
}
.answer-wrong {
  background: #FEF2F2;
  border: 2px solid var(--red-err);
  border-radius: var(--radius-md);
  padding: 18px 22px;
  margin: 10px 0;
  color: #991B1B;
  font-weight: 600;
}

/* ── quiz choice buttons ── */
.choice-btn > button {
  background: white !important;
  border: 2px solid var(--cream-dark) !important;
  color: var(--text-dark) !important;
  font-size: 1rem !important;
  padding: 12px 20px !important;
  width: 100% !important;
  text-align: left !important;
  border-radius: var(--radius-md) !important;
  font-weight: 600 !important;
  margin-bottom: 6px !important;
}
.choice-btn > button:hover {
  border-color: var(--brown-pale) !important;
  background: var(--cream) !important;
}

/* ── progress bar custom ── */
.prog-bar-wrap {
  background: var(--cream-dark);
  border-radius: 30px;
  height: 14px;
  overflow: hidden;
  margin: 6px 0 14px;
}
.prog-bar-fill {
  height: 100%;
  border-radius: 30px;
  background: linear-gradient(90deg, #8B4513, #F5A623);
  transition: width 0.4s ease;
}

/* ── stat chip ── */
.stat-chip {
  display: inline-block;
  background: white;
  border: 2px solid var(--cream-dark);
  border-radius: 14px;
  padding: 12px 20px;
  text-align: center;
  box-shadow: var(--shadow);
  margin: 6px;
}
.stat-chip .stat-num { font-size: 1.8rem; font-weight: 900; color: var(--brown-mid); }
.stat-chip .stat-lbl { font-size: 0.78rem; color: #888; font-weight: 600; margin-top: 2px; }

/* ── mastery / weak badges ── */
.badge-master {
  display: inline-block;
  background: #D1FAE5;
  border: 1.5px solid #34D399;
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 0.82rem;
  color: #065F46;
  font-weight: 700;
  margin: 3px;
}
.badge-weak {
  display: inline-block;
  background: #FEE2E2;
  border: 1.5px solid #FCA5A5;
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 0.82rem;
  color: #991B1B;
  font-weight: 700;
  margin: 3px;
}
.badge-neutral {
  display: inline-block;
  background: #EDE9FE;
  border: 1.5px solid #A78BFA;
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 0.82rem;
  color: #5B21B6;
  font-weight: 700;
  margin: 3px;
}

/* ── score result big number ── */
.score-big {
  font-size: 4rem;
  font-weight: 900;
  color: var(--brown-mid);
  line-height: 1;
}
.grade-letter {
  font-size: 2.2rem;
  font-weight: 900;
  padding: 8px 28px;
  border-radius: 16px;
  display: inline-block;
  margin-top: 8px;
}

/* ── difficulty pill ── */
.diff-easy   { color: #166534; background: #D1FAE5; border-radius:8px; padding:2px 10px; font-size:0.8rem; font-weight:700; }
.diff-medium { color: #92400E; background: #FEF3C7; border-radius:8px; padding:2px 10px; font-size:0.8rem; font-weight:700; }
.diff-hard   { color: #991B1B; background: #FEE2E2; border-radius:8px; padding:2px 10px; font-size:0.8rem; font-weight:700; }

/* ── divider ── */
.cody-divider {
  border: none;
  border-top: 2px solid var(--cream-dark);
  margin: 20px 0;
}

/* hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ════════════════════════════════════════════════════════════

def init_state() -> None:
    defaults = {
        "page": "home",
        # flashcards
        "fc_cards": [],
        "fc_index": 0,
        "fc_flipped": False,
        "fc_results": [],
        "fc_done": False,
        # quiz
        "qz_questions": [],
        "qz_index": 0,
        "qz_answers": [],
        "qz_answered": False,
        "qz_last_correct": None,
        "qz_done": False,
        "qz_result": {},
        # test
        "ts_questions": [],
        "ts_user_answers": {},
        "ts_submitted": False,
        "ts_result": {},
        # mistake review
        "mr_questions": [],
        "mr_index": 0,
        "mr_answered": False,
        "mr_last_correct": None,
        "mr_done": False,
        "mr_correct": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════

def go(page: str) -> None:
    st.session_state.page = page
    st.rerun()


def progress_bar_html(value: int, total: int, label: str = "") -> str:
    pct = int(value / total * 100) if total else 0
    return f"""
<div style="margin:4px 0 12px;">
  {'<div style="font-size:0.82rem;color:#888;margin-bottom:4px;font-weight:600;">'+label+'</div>' if label else ''}
  <div class="prog-bar-wrap">
    <div class="prog-bar-fill" style="width:{pct}%"></div>
  </div>
  <div style="font-size:0.78rem;color:#aaa;text-align:right;">{value}/{total}</div>
</div>"""


def grade_color(pct: int) -> str:
    if pct >= 90: return "#166534"
    if pct >= 80: return "#1D4ED8"
    if pct >= 70: return "#92400E"
    if pct >= 60: return "#B45309"
    return "#991B1B"


def grade_bg(pct: int) -> str:
    if pct >= 90: return "#D1FAE5"
    if pct >= 80: return "#DBEAFE"
    if pct >= 70: return "#FEF3C7"
    if pct >= 60: return "#FEF3C7"
    return "#FEE2E2"


def grade_letter(pct: int) -> str:
    if pct >= 90: return "A"
    if pct >= 80: return "B"
    if pct >= 70: return "C"
    if pct >= 60: return "D"
    return "F"


# ════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════

def sidebar() -> None:
    with st.sidebar:
        # Cody logo area
        st.markdown(f"""
<div style="text-align:center;padding:16px 0 8px;">
  <div style="width:110px;height:110px;margin:0 auto;">{CODY['happy']}</div>
  <div style="font-size:1.35rem;font-weight:900;color:#F5DEB3;margin-top:6px;letter-spacing:0.5px;">
    Cody's Math Lab
  </div>
  <div style="font-size:0.78rem;color:#C4A882;margin-top:2px;">Pre-Calculus 11 Trig</div>
</div>
<hr style="border:1px solid rgba(255,255,255,0.08);margin:10px 0 14px;"/>
""", unsafe_allow_html=True)

        pages = [
            ("🏠", "Home",           "home"),
            ("📚", "Study Guide",    "study_guide"),
            ("🃏", "Flashcards",     "flashcards"),
            ("❓", "Quiz Mode",      "quiz"),
            ("📝", "Test Mode",      "test"),
            ("📊", "My Progress",    "progress"),
            ("🔄", "Mistake Review", "mistake_review"),
            ("📄", "Upload Notes",   "upload"),
        ]
        for icon, label, key in pages:
            active = st.session_state.page == key
            style = "background:rgba(245,222,179,0.18)!important;border-color:rgba(245,222,179,0.5)!important;" if active else ""
            # We use a button per nav item and inject style via markdown
            if st.button(f"{icon}  {label}", key=f"nav_{key}"):
                go(key)

        # quick progress peek
        st.markdown('<hr style="border:1px solid rgba(255,255,255,0.08);margin:18px 0 10px;"/>', unsafe_allow_html=True)
        prog = load_progress()
        total_quizzes = len(prog.get("quiz_scores", []))
        session_count = prog.get("session_count", 0)
        st.markdown(f"""
<div style="padding:0 4px;">
  <div style="font-size:0.72rem;color:#9E7E5A;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">
    Quick Stats
  </div>
  <div style="display:flex;gap:8px;">
    <div style="flex:1;background:rgba(255,255,255,0.06);border-radius:10px;padding:8px;text-align:center;">
      <div style="font-size:1.3rem;font-weight:900;color:#F5DEB3;">{session_count}</div>
      <div style="font-size:0.68rem;color:#9E7E5A;">Sessions</div>
    </div>
    <div style="flex:1;background:rgba(255,255,255,0.06);border-radius:10px;padding:8px;text-align:center;">
      <div style="font-size:1.3rem;font-weight:900;color:#F5DEB3;">{total_quizzes}</div>
      <div style="font-size:0.68rem;color:#9E7E5A;">Quizzes</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE: HOME
# ════════════════════════════════════════════════════════════

def page_home() -> None:
    st.markdown(f"""
<div style="text-align:center;padding:32px 0 16px;">
  <div style="width:200px;height:200px;margin:0 auto;">{CODY['happy']}</div>
  <h1 style="font-size:2.6rem;font-weight:900;color:#8B4513;margin:12px 0 4px;">
    Hey! I'm Cody! 🐾
  </h1>
  <p style="font-size:1.15rem;color:#6B3410;max-width:520px;margin:0 auto 6px;">
    Your personal math tutor — here to help you master
    <strong>Pre-Calculus 11 Trigonometry</strong> step by step.
  </p>
  <p style="font-size:0.9rem;color:#999;">Pick a mode below to get started!</p>
</div>
""", unsafe_allow_html=True)

    nav_items = [
        ("📚", "Study Guide",    "study_guide", "Full notes, formulas & worked examples"),
        ("🃏", "Flashcards",     "flashcards",  "Drill key concepts one card at a time"),
        ("❓", "Quiz Mode",      "quiz",         "Test yourself with instant feedback"),
        ("📝", "Test Mode",      "test",         "Full exam with grade & answer key"),
        ("📊", "My Progress",    "progress",     "Track scores, mastery & weak spots"),
        ("🔄", "Mistake Review", "mistake_review","Targeted practice on your errors"),
    ]

    cols1 = st.columns(3, gap="medium")
    cols2 = st.columns(3, gap="medium")
    all_cols = cols1 + cols2

    for col, (icon, title, page_key, desc) in zip(all_cols, nav_items):
        with col:
            st.markdown(f"""
<div class="nav-card" style="margin-bottom:0;">
  <div class="nav-icon">{icon}</div>
  <div class="nav-title">{title}</div>
  <div class="nav-desc">{desc}</div>
</div>
""", unsafe_allow_html=True)
            if st.button(f"Open {title}", key=f"home_{page_key}", use_container_width=True):
                go(page_key)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(speech_bubble(
        "I'll guide you through <strong>angles, reference angles, the unit circle, exact values, "
        "graphing trig functions, solving equations</strong>, and more. "
        "Start with the Study Guide if you're new, or jump straight into Flashcards or a Quiz! 🐾",
        mood="happy",
    ), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE: STUDY GUIDE
# ════════════════════════════════════════════════════════════

def page_study_guide() -> None:
    guide = get_study_guide(DEFAULT_TOPIC)
    if not guide:
        st.error("Study guide not found.")
        return

    record_study_session(DEFAULT_TOPIC)

    st.markdown(f"<h1 style='color:#8B4513;font-weight:900;'>📚 {guide['title']}</h1>", unsafe_allow_html=True)

    st.markdown(speech_bubble(
        "Let's go through everything together! I've organised this into sections. "
        "Expand each one and take your time. <strong>Don't skip the worked examples!</strong> 🐾",
        mood="reading",
    ), unsafe_allow_html=True)

    # Overview
    st.markdown("<div class='cody-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>Overview</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#444;line-height:1.7;'>{guide['overview'].strip()}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Key concepts
    st.markdown("<div class='cody-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>Key Concepts</div>", unsafe_allow_html=True)
    badges = "".join(f"<span class='concept-badge'>{c}</span>" for c in guide["key_concepts"])
    st.markdown(badges, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Formulas
    st.markdown("<div class='cody-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>Essential Formulas</div>", unsafe_allow_html=True)
    chips = "".join(
        f"<span class='formula-chip'><strong>{name}:</strong> {formula}</span>"
        for name, formula in guide["formulas"].items()
    )
    st.markdown(chips, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Content sections
    st.markdown("<div class='section-heading' style='font-size:1.3rem;margin-top:24px;'>📖 Lesson Sections</div>",
                unsafe_allow_html=True)
    for sec in guide["sections"]:
        with st.expander(sec["name"], expanded=False):
            st.code(sec["content"].strip(), language=None)

    # Worked examples
    st.markdown("<div class='section-heading' style='font-size:1.3rem;margin-top:20px;'>✏️ Worked Examples</div>",
                unsafe_allow_html=True)
    for i, ex in enumerate(guide["worked_examples"], 1):
        with st.expander(f"Example {i}: {ex['problem']}", expanded=False):
            st.code(ex["solution"].strip(), language=None)

    # Common mistakes
    st.markdown("<div class='cody-card' style='border-left:4px solid #EF4444;'>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>⚠️ Common Mistakes to Avoid</div>", unsafe_allow_html=True)
    for mistake in guide["common_mistakes"]:
        st.markdown(f"<p style='margin:4px 0;color:#444;'>❌ {mistake}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Practice questions
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown("<div class='cody-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>📝 Practice Questions</div>", unsafe_allow_html=True)
        for q in guide["practice_questions"]:
            st.markdown(f"<p style='margin:5px 0;color:#444;'>{q}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='cody-card' style='border-left:4px solid #F5A623;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>🔥 Challenge Questions</div>", unsafe_allow_html=True)
        for q in guide["challenge_questions"]:
            st.markdown(f"<p style='margin:5px 0;color:#444;'>{q}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Summary
    st.markdown("<div class='cody-card' style='background:linear-gradient(135deg,#FFF8F0,#FFF3E0);border-left:4px solid #F5A623;'>",
                unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>📌 Summary</div>", unsafe_allow_html=True)
    st.markdown(f"<pre style='white-space:pre-wrap;font-family:Nunito,sans-serif;color:#444;background:transparent;border:none;padding:0;font-size:0.95rem;'>{guide['summary'].strip()}</pre>",
                unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if st.button("🃏 Go to Flashcards →", use_container_width=False):
        go("flashcards")


# ════════════════════════════════════════════════════════════
# PAGE: FLASHCARDS
# ════════════════════════════════════════════════════════════

def page_flashcards() -> None:
    st.markdown("<h1 style='color:#8B4513;font-weight:900;'>🃏 Flashcards</h1>", unsafe_allow_html=True)

    # Setup screen
    if not st.session_state.fc_cards:
        st.markdown(speech_bubble(
            "Let's drill these concepts! Try to <strong>answer in your head</strong> before flipping each card. "
            "Be honest with yourself — that's how you really learn! 🐾",
            mood="thinking",
        ), unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            diff = st.selectbox("Difficulty filter", ["All", "Easy", "Medium", "Hard"])
        with col2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("▶ Start Flashcards", use_container_width=True):
                pool = flashcard_pool(DEFAULT_TOPIC)
                if diff != "All":
                    pool = [c for c in pool if c.get("difficulty", "").lower() == diff.lower()]
                random.shuffle(pool)
                st.session_state.fc_cards = pool
                st.session_state.fc_index = 0
                st.session_state.fc_flipped = False
                st.session_state.fc_results = []
                st.session_state.fc_done = False
                st.rerun()
        return

    # Done screen
    if st.session_state.fc_done:
        known = st.session_state.fc_results.count(True)
        total = len(st.session_state.fc_results)
        pct = int(known / total * 100) if total else 0
        mood = "celebrate" if pct >= 75 else "sad"

        st.markdown(speech_bubble(
            f"Session complete! You knew <strong>{known}/{total}</strong> cards ({pct}%). "
            + ("Amazing memory! 🎉" if pct >= 80 else "Keep reviewing — you'll get there! 💪"),
            mood=mood,
        ), unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"""
<div class="stat-chip" style="width:100%;box-sizing:border-box;">
  <div class="stat-num">{known}/{total}</div>
  <div class="stat-lbl">Known</div>
</div>""", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
<div class="stat-chip" style="width:100%;box-sizing:border-box;">
  <div class="stat-num">{pct}%</div>
  <div class="stat-lbl">Score</div>
</div>""", unsafe_allow_html=True)
        with col_c:
            st.markdown(f"""
<div class="stat-chip" style="width:100%;box-sizing:border-box;">
  <div class="stat-num">{total - known}</div>
  <div class="stat-lbl">Need Review</div>
</div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔄 Restart", use_container_width=True):
                st.session_state.fc_cards = []
                st.rerun()
        with c2:
            if st.button("❓ Take a Quiz", use_container_width=True):
                go("quiz")
        with c3:
            if st.button("🏠 Home", use_container_width=True):
                go("home")
        return

    # Active session
    cards = st.session_state.fc_cards
    idx = st.session_state.fc_index
    card = cards[idx]

    st.markdown(progress_bar_html(idx + 1, len(cards), f"Card {idx+1} of {len(cards)}"),
                unsafe_allow_html=True)

    diff_label = card.get("difficulty", "medium")
    diff_class = f"diff-{diff_label}"
    st.markdown(
        f"<span class='{diff_class}'>{diff_label.upper()}</span>"
        f"&nbsp;&nbsp;<span style='color:#999;font-size:0.85rem;'>{card.get('topic','')}</span>",
        unsafe_allow_html=True,
    )

    # The card
    if not st.session_state.fc_flipped:
        st.markdown(f"""
<div class="flashcard flashcard-front">
  <div style='font-size:0.85rem;opacity:0.7;margin-bottom:10px;letter-spacing:1px;text-transform:uppercase;'>Question</div>
  <div>{card['front']}</div>
</div>""", unsafe_allow_html=True)

        col_flip, _ = st.columns([1, 2])
        with col_flip:
            if st.button("👀 Flip Card", use_container_width=True):
                st.session_state.fc_flipped = True
                st.rerun()
    else:
        st.markdown(f"""
<div class="flashcard flashcard-back">
  <div style='font-size:0.85rem;opacity:0.7;margin-bottom:10px;letter-spacing:1px;text-transform:uppercase;'>Answer</div>
  <pre style='background:rgba(255,255,255,0.15);border-radius:10px;padding:14px 18px;font-size:0.95rem;text-align:left;white-space:pre-wrap;color:white;font-family:Nunito,sans-serif;'>{card['back']}</pre>
</div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("😕 Didn't Know", use_container_width=True):
                st.session_state.fc_results.append(False)
                _fc_advance()
        with c2:
            if st.button("🤔 Almost", use_container_width=True):
                st.session_state.fc_results.append(False)
                _fc_advance()
        with c3:
            if st.button("✅ Got It!", use_container_width=True):
                st.session_state.fc_results.append(True)
                _fc_advance()


def _fc_advance() -> None:
    st.session_state.fc_index += 1
    st.session_state.fc_flipped = False
    if st.session_state.fc_index >= len(st.session_state.fc_cards):
        st.session_state.fc_done = True
    st.rerun()


# ════════════════════════════════════════════════════════════
# PAGE: QUIZ
# ════════════════════════════════════════════════════════════

def page_quiz() -> None:
    st.markdown("<h1 style='color:#8B4513;font-weight:900;'>❓ Quiz Mode</h1>", unsafe_allow_html=True)

    # Setup screen
    if not st.session_state.qz_questions:
        st.markdown(speech_bubble(
            "Time to test what you know! Pick a difficulty and I'll fire questions at you one by one. "
            "I'll give you instant feedback after each one! 🐾",
            mood="happy",
        ), unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            diff = st.selectbox("Difficulty", ["Mixed", "Easy", "Medium", "Hard"])
        with col2:
            n = st.slider("Number of questions", 3, 10, 5)

        if st.button("▶ Start Quiz", use_container_width=True):
            if diff == "Mixed":
                pool = all_quiz_questions(DEFAULT_TOPIC)
            else:
                pool = quiz_pool(DEFAULT_TOPIC, diff.lower())
                pool = [{**q, "difficulty": diff.lower()} for q in pool]
            if not pool:
                st.error("No questions found!")
                return
            questions = random.sample(pool, min(n, len(pool)))
            st.session_state.qz_questions = questions
            st.session_state.qz_index = 0
            st.session_state.qz_answers = []
            st.session_state.qz_answered = False
            st.session_state.qz_last_correct = None
            st.session_state.qz_done = False
            st.session_state.qz_result = {}
            st.rerun()
        return

    # Done screen
    if st.session_state.qz_done:
        result = st.session_state.qz_result
        pct = result.get("percent", 0)
        score = result.get("score", 0)
        total = result.get("total", 0)
        mood = "celebrate" if pct >= 80 else ("thinking" if pct >= 60 else "sad")

        if pct >= 80:
            msg = f"Incredible! You scored <strong>{score}/{total} ({pct}%)</strong>! You're really nailing this! 🎉"
        elif pct >= 60:
            msg = f"Good effort! <strong>{score}/{total} ({pct}%)</strong>. Review the ones you missed and try again!"
        else:
            msg = f"You got <strong>{score}/{total} ({pct}%)</strong>. Let's go back to the study guide and practice more. I believe in you! 💪"

        st.markdown(speech_bubble(msg, mood=mood), unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        gl = grade_letter(pct)
        gc = grade_color(pct)
        gb = grade_bg(pct)
        st.markdown(f"""
<div style="text-align:center;margin:16px 0;">
  <span class="score-big">{pct}%</span>
  <br>
  <span class="grade-letter" style="color:{gc};background:{gb};">{gl}</span>
</div>""", unsafe_allow_html=True)

        # Wrong questions recap
        wrong = result.get("wrong_questions", [])
        if wrong:
            st.markdown("<div class='section-heading'>📋 Questions You Missed</div>", unsafe_allow_html=True)
            for w in wrong:
                st.markdown(f"""
<div class="answer-wrong" style="margin:6px 0;">
  <strong>Q:</strong> {w['question']}<br>
  <strong>Your answer:</strong> {w.get('user_answer','—')} &nbsp;|&nbsp;
  <strong>Correct:</strong> {w['answer']}<br>
  <span style="color:#555;font-size:0.9rem;">💡 {w['explanation']}</span>
</div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.qz_questions = []
                st.rerun()
        with c2:
            if st.button("🔄 Mistake Review", use_container_width=True):
                go("mistake_review")
        with c3:
            if st.button("📝 Take a Test", use_container_width=True):
                go("test")
        return

    # Active question
    questions = st.session_state.qz_questions
    idx = st.session_state.qz_index
    q = questions[idx]
    total = len(questions)

    st.markdown(progress_bar_html(idx + 1, total, f"Question {idx+1} of {total}"),
                unsafe_allow_html=True)

    diff = q.get("difficulty", "medium")
    st.markdown(
        f"<span class='diff-{diff}'>{diff.upper()}</span>"
        f"&nbsp;&nbsp;<span style='color:#999;font-size:0.85rem;'>{q.get('topic','')}</span>",
        unsafe_allow_html=True,
    )

    # Cody asking
    cody_msgs = [
        "Here's your next question — think carefully! 🐾",
        "You've got this! Take your time. 🎯",
        "Read it twice before answering! ✨",
        "I believe in you — what do you think? 🐾",
    ]
    if not st.session_state.qz_answered:
        st.markdown(speech_bubble(random.choice(cody_msgs), mood="thinking"), unsafe_allow_html=True)

    # Question card
    st.markdown(f"""
<div class="cody-card" style="margin-top:12px;">
  <div style="font-size:1.15rem;font-weight:700;color:#2C1810;line-height:1.6;">{q['question']}</div>
</div>""", unsafe_allow_html=True)

    # Already answered — show feedback
    if st.session_state.qz_answered:
        correct = st.session_state.qz_last_correct
        user_ans = st.session_state.qz_answers[-1].get("user_answer", "")
        if correct:
            st.markdown(speech_bubble("✅ Correct! Great job!", mood="celebrate"), unsafe_allow_html=True)
            st.markdown(f"""
<div class="answer-correct">
  ✅ <strong>Your answer "{user_ans}" is correct!</strong><br>
  <span style="font-size:0.92rem;color:#166534;">💡 {q['explanation']}</span>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown(speech_bubble(
                f"Not quite! The correct answer is <strong>{q['answer']}</strong>. Let's look at why...",
                mood="sad",
            ), unsafe_allow_html=True)
            st.markdown(f"""
<div class="answer-wrong">
  ❌ <strong>Your answer: "{user_ans}"</strong> — Correct answer: <strong>{q['answer']}</strong><br>
  <span style="font-size:0.92rem;color:#7F1D1D;">💡 {q['explanation']}</span>
</div>""", unsafe_allow_html=True)

        is_last = idx >= total - 1
        btn_label = "🏁 See Results" if is_last else "Next Question →"
        if st.button(btn_label, use_container_width=False):
            if is_last:
                _quiz_finish()
            else:
                st.session_state.qz_index += 1
                st.session_state.qz_answered = False
                st.session_state.qz_last_correct = None
                st.rerun()
        return

    # Input
    if q["type"] == "multiple_choice":
        choices = q.get("choices", [])
        chosen = st.radio("Select your answer:", choices, key=f"mc_{idx}", label_visibility="collapsed")
        if st.button("Submit Answer", use_container_width=False):
            letter = chosen.strip()[0] if chosen else ""
            _quiz_submit(letter)
    else:
        user_ans = st.text_input("Your answer:", key=f"sa_{idx}", placeholder="Type your answer here...")
        if st.button("Submit Answer", use_container_width=False):
            _quiz_submit(user_ans)


def _quiz_submit(user_ans: str) -> None:
    questions = st.session_state.qz_questions
    idx = st.session_state.qz_index
    q = questions[idx]
    correct = check_answer(user_ans, q)
    st.session_state.qz_answers.append({
        "id": q["id"],
        "correct": correct,
        "user_answer": user_ans,
        "question": q,
    })
    st.session_state.qz_answered = True
    st.session_state.qz_last_correct = correct
    st.rerun()


def _quiz_finish() -> None:
    answers = st.session_state.qz_answers
    questions = st.session_state.qz_questions
    score = sum(1 for a in answers if a["correct"])
    total = len(answers)
    pct = round(score / total * 100) if total else 0
    wrong = [
        {**a["question"], "user_answer": a["user_answer"]}
        for a in answers if not a["correct"]
    ]
    result = {
        "topic": DEFAULT_TOPIC,
        "difficulty": "mixed",
        "score": score,
        "total": total,
        "percent": pct,
        "wrong_questions": wrong,
        "results": [{"id": a["id"], "correct": a["correct"], "user_answer": a["user_answer"]} for a in answers],
        "timestamp": datetime.now().isoformat(),
    }
    record_quiz_result(result)
    st.session_state.qz_result = result
    st.session_state.qz_done = True
    st.rerun()


# ════════════════════════════════════════════════════════════
# PAGE: TEST
# ════════════════════════════════════════════════════════════

def page_test() -> None:
    st.markdown("<h1 style='color:#8B4513;font-weight:900;'>📝 Test Mode</h1>", unsafe_allow_html=True)

    # Setup
    if not st.session_state.ts_questions:
        st.markdown(speech_bubble(
            "This is a proper test! I'll show you all the questions at once. "
            "Answer them all, then hit Submit. I'll mark it and show you the full answer key. "
            "No peeking! 🐾",
            mood="reading",
        ), unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            n_easy = st.number_input("Easy questions", 1, 5, 3)
        with col2:
            n_med = st.number_input("Medium questions", 1, 5, 4)
        with col3:
            n_hard = st.number_input("Hard questions", 1, 5, 3)

        if st.button("▶ Start Test", use_container_width=True):
            easy_q  = random.sample(quiz_pool(DEFAULT_TOPIC, "easy"), min(n_easy, len(quiz_pool(DEFAULT_TOPIC, "easy"))))
            med_q   = random.sample(quiz_pool(DEFAULT_TOPIC, "medium"), min(n_med, len(quiz_pool(DEFAULT_TOPIC, "medium"))))
            hard_q  = random.sample(quiz_pool(DEFAULT_TOPIC, "hard"), min(n_hard, len(quiz_pool(DEFAULT_TOPIC, "hard"))))
            questions = (
                [{**q, "difficulty": "easy"}   for q in easy_q] +
                [{**q, "difficulty": "medium"} for q in med_q]  +
                [{**q, "difficulty": "hard"}   for q in hard_q]
            )
            st.session_state.ts_questions = questions
            st.session_state.ts_user_answers = {}
            st.session_state.ts_submitted = False
            st.session_state.ts_result = {}
            st.rerun()
        return

    # Results screen
    if st.session_state.ts_submitted:
        result = st.session_state.ts_result
        pct = result["percent"]
        score = result["score"]
        total = result["total"]
        mood = "celebrate" if pct >= 80 else ("thinking" if pct >= 60 else "sad")
        gl = grade_letter(pct)
        gc = grade_color(pct)
        gb = grade_bg(pct)

        if pct >= 80:
            msg = f"Outstanding! <strong>{score}/{total} ({pct}%) — Grade {gl}</strong>! You've really been studying! 🎉"
        elif pct >= 60:
            msg = f"Good work! <strong>{score}/{total} ({pct}%) — Grade {gl}</strong>. A bit more practice and you'll ace it!"
        else:
            msg = f"<strong>{score}/{total} ({pct}%) — Grade {gl}</strong>. Don't worry — review the study guide and try again. I'm here to help! 💪"

        st.markdown(speech_bubble(msg, mood=mood), unsafe_allow_html=True)
        st.markdown(f"""
<div style="text-align:center;margin:20px 0;">
  <span class="score-big">{pct}%</span>&nbsp;&nbsp;
  <span class="grade-letter" style="color:{gc};background:{gb};">{gl}</span>
</div>""", unsafe_allow_html=True)

        # Score breakdown by difficulty
        by_diff = {}
        for r in result["results"]:
            d = r["difficulty"]
            by_diff.setdefault(d, {"score": 0, "total": 0})
            by_diff[d]["total"] += 1
            if r["correct"]:
                by_diff[d]["score"] += 1

        cols = st.columns(len(by_diff))
        for col, (diff, counts) in zip(cols, by_diff.items()):
            with col:
                dp = round(counts["score"] / counts["total"] * 100) if counts["total"] else 0
                st.markdown(f"""
<div class="stat-chip" style="width:100%;box-sizing:border-box;">
  <div class="stat-num">{dp}%</div>
  <div class="stat-lbl">{diff.capitalize()}</div>
</div>""", unsafe_allow_html=True)

        # Answer key
        st.markdown("<div class='section-heading' style='margin-top:24px;'>📋 Answer Key & Explanations</div>",
                    unsafe_allow_html=True)
        for i, r in enumerate(result["results"], 1):
            q = r["question_obj"]
            diff_class = f"diff-{r['difficulty']}"
            if r["correct"]:
                st.markdown(f"""
<div class="answer-correct" style="margin:6px 0;">
  <span class="{diff_class}">{r['difficulty'].upper()}</span>&nbsp;
  <strong>Q{i}:</strong> {q['question']}<br>
  ✅ <strong>Your answer "{r['user_answer']}" is correct!</strong><br>
  <span style="font-size:0.9rem;color:#166534;">💡 {q['explanation']}</span>
</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
<div class="answer-wrong" style="margin:6px 0;">
  <span class="{diff_class}">{r['difficulty'].upper()}</span>&nbsp;
  <strong>Q{i}:</strong> {q['question']}<br>
  ❌ Your answer: <strong>"{r['user_answer']}"</strong> — Correct: <strong>{q['answer']}</strong><br>
  <span style="font-size:0.9rem;color:#7F1D1D;">💡 {q['explanation']}</span>
</div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔄 New Test", use_container_width=True):
                st.session_state.ts_questions = []
                st.rerun()
        with c2:
            if st.button("📊 View Progress", use_container_width=True):
                go("progress")
        with c3:
            if st.button("🔄 Mistake Review", use_container_width=True):
                go("mistake_review")
        return

    # Active test — show all questions
    questions = st.session_state.ts_questions
    total = len(questions)
    st.markdown(f"""
<div style="color:#888;font-size:0.9rem;margin-bottom:16px;font-weight:600;">
  📝 {total} questions — Answer all of them, then submit at the bottom.
</div>""", unsafe_allow_html=True)

    for i, q in enumerate(questions):
        diff = q.get("difficulty", "medium")
        st.markdown(f"""
<div class="cody-card" style="margin-bottom:12px;">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
    <span style="font-weight:900;color:#8B4513;font-size:1.1rem;">Q{i+1}</span>
    <span class="diff-{diff}">{diff.upper()}</span>
    <span style="color:#bbb;font-size:0.8rem;">{q.get('topic','')}</span>
  </div>
  <div style="font-size:1rem;font-weight:700;color:#2C1810;margin-bottom:12px;">{q['question']}</div>
""", unsafe_allow_html=True)

        if q["type"] == "multiple_choice":
            choices = q.get("choices", [])
            current = st.session_state.ts_user_answers.get(q["id"], choices[0])
            chosen = st.radio(
                f"q{i}", choices,
                index=choices.index(current) if current in choices else 0,
                key=f"test_mc_{i}",
                label_visibility="collapsed",
            )
            st.session_state.ts_user_answers[q["id"]] = chosen.strip()[0] if chosen else ""
        else:
            current = st.session_state.ts_user_answers.get(q["id"], "")
            val = st.text_input(
                f"Answer {i+1}", value=current,
                key=f"test_sa_{i}",
                placeholder="Your answer...",
                label_visibility="collapsed",
            )
            st.session_state.ts_user_answers[q["id"]] = val

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    answered_count = sum(1 for v in st.session_state.ts_user_answers.values() if str(v).strip())

    col_sub, col_info = st.columns([1, 2])
    with col_info:
        st.markdown(f"<span style='color:#888;font-size:0.9rem;'>{answered_count}/{total} questions answered</span>",
                    unsafe_allow_html=True)
    with col_sub:
        if st.button("🏁 Submit Test", use_container_width=True, type="primary"):
            _test_submit(questions)


def _test_submit(questions: list[dict]) -> None:
    score = 0
    results = []
    wrong = []
    for q in questions:
        user_ans = str(st.session_state.ts_user_answers.get(q["id"], ""))
        correct = check_answer(user_ans, q)
        if correct:
            score += 1
        else:
            wrong.append({**q, "user_answer": user_ans})
        results.append({
            "id": q["id"],
            "difficulty": q.get("difficulty", "medium"),
            "correct": correct,
            "user_answer": user_ans,
            "question_obj": q,
        })

    total = len(questions)
    pct = round(score / total * 100) if total else 0
    gl = grade_letter(pct)

    result = {
        "topic": DEFAULT_TOPIC,
        "score": score,
        "total": total,
        "percent": pct,
        "grade": gl,
        "wrong_questions": wrong,
        "results": results,
        "timestamp": datetime.now().isoformat(),
    }
    record_test_result(result)
    st.session_state.ts_result = result
    st.session_state.ts_submitted = True
    st.rerun()


# ════════════════════════════════════════════════════════════
# PAGE: PROGRESS
# ════════════════════════════════════════════════════════════

def page_progress() -> None:
    st.markdown("<h1 style='color:#8B4513;font-weight:900;'>📊 My Progress</h1>", unsafe_allow_html=True)

    prog = load_progress()
    quiz_scores = prog.get("quiz_scores", [])
    test_scores = prog.get("test_scores", [])
    mistakes = prog.get("mistakes", [])
    mastered = prog.get("mastered_topics", [])
    weak = prog.get("weak_areas", [])
    sessions = prog.get("session_count", 0)

    # Cody message
    if not quiz_scores and not test_scores:
        st.markdown(speech_bubble(
            "No scores yet! Go take a quiz or test to see your progress tracked here. "
            "I can't wait to cheer you on! 🐾",
            mood="happy",
        ), unsafe_allow_html=True)
    elif sum(r["percent"] for r in quiz_scores[-5:]) / max(len(quiz_scores[-5:]), 1) >= 75:
        st.markdown(speech_bubble(
            "You're doing amazing! Keep it up — you're well on your way to mastering this material! 🎉",
            mood="celebrate",
        ), unsafe_allow_html=True)
    else:
        st.markdown(speech_bubble(
            "Here's how you're doing so far! Don't worry about the weak areas — that's exactly what we're here to fix! 💪",
            mood="thinking",
        ), unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Top stats
    avg_quiz = round(sum(r["percent"] for r in quiz_scores) / len(quiz_scores)) if quiz_scores else 0
    avg_test = round(sum(r["percent"] for r in test_scores) / len(test_scores)) if test_scores else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, num, lbl in [
        (c1, sessions, "Study Sessions"),
        (c2, len(quiz_scores), "Quizzes Taken"),
        (c3, f"{avg_quiz}%", "Avg Quiz Score"),
        (c4, f"{avg_test}%", "Avg Test Score"),
    ]:
        with col:
            st.markdown(f"""
<div class="stat-chip" style="width:100%;box-sizing:border-box;text-align:center;">
  <div class="stat-num">{num}</div>
  <div class="stat-lbl">{lbl}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        # Mastered
        st.markdown("<div class='cody-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>🏆 Mastered Topics</div>", unsafe_allow_html=True)
        if mastered:
            for t in mastered:
                st.markdown(f"<span class='badge-master'>✓ {t}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:#999;font-size:0.9rem;'>Score 80%+ on a quiz to master a topic!</p>",
                        unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Weak areas
        st.markdown("<div class='cody-card' style='margin-top:12px;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>⚠️ Weak Areas</div>", unsafe_allow_html=True)
        if weak:
            for t in weak:
                st.markdown(f"<span class='badge-weak'>✗ {t}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:#999;font-size:0.9rem;'>No weak areas identified yet.</p>",
                        unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Recommendations
        recs = get_recommendations()
        st.markdown("<div class='cody-card' style='margin-top:12px;border-left:4px solid #F5A623;'>",
                    unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>💡 Cody's Recommendations</div>", unsafe_allow_html=True)
        for r in recs:
            st.markdown(f"<p style='margin:5px 0;color:#444;'>🐾 {r}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        # Recent quiz scores
        if quiz_scores:
            st.markdown("<div class='cody-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-heading'>📈 Recent Quiz Scores</div>", unsafe_allow_html=True)
            for r in reversed(quiz_scores[-8:]):
                pct = r["percent"]
                gc = grade_color(pct)
                gb = grade_bg(pct)
                date = r.get("timestamp", "")[:10]
                st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid #F5E8D5;">
  <span style="font-weight:900;color:{gc};background:{gb};border-radius:8px;padding:2px 10px;font-size:0.9rem;">{pct}%</span>
  <span style="flex:1;color:#555;font-size:0.88rem;">{r.get('difficulty','mixed').capitalize()} quiz</span>
  <span style="color:#bbb;font-size:0.8rem;">{date}</span>
</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Mistake breakdown
        if mistakes:
            categories = {}
            for m in mistakes:
                c = m["category"]
                categories[c] = categories.get(c, 0) + 1

            st.markdown("<div class='cody-card' style='margin-top:12px;'>", unsafe_allow_html=True)
            st.markdown("<div class='section-heading'>🔍 Mistake Breakdown</div>", unsafe_allow_html=True)
            top = sorted(categories.items(), key=lambda x: -x[1])
            max_val = max(v for _, v in top)
            for cat, count in top:
                bar_w = int(count / max_val * 100)
                st.markdown(f"""
<div style="margin:6px 0;">
  <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:3px;">
    <span style="color:#444;font-weight:600;">{cat}</span>
    <span style="color:#888;">{count}</span>
  </div>
  <div style="background:#F5E8D5;border-radius:20px;height:8px;">
    <div style="width:{bar_w}%;background:linear-gradient(90deg,#8B4513,#F5A623);height:8px;border-radius:20px;"></div>
  </div>
</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔄 Run Mistake Review", use_container_width=False):
        go("mistake_review")


# ════════════════════════════════════════════════════════════
# PAGE: MISTAKE REVIEW
# ════════════════════════════════════════════════════════════

def page_mistake_review() -> None:
    st.markdown("<h1 style='color:#8B4513;font-weight:900;'>🔄 Mistake Review</h1>", unsafe_allow_html=True)

    prog = load_progress()
    mistakes = prog.get("mistakes", [])

    # Setup
    if not st.session_state.mr_questions:
        if not mistakes:
            st.markdown(speech_bubble(
                "No mistakes recorded yet! Take a quiz or test first, then come back here "
                "and I'll help you drill exactly the things you got wrong. 🐾",
                mood="happy",
            ), unsafe_allow_html=True)
            if st.button("❓ Go take a Quiz"):
                go("quiz")
            return

        # Build targeted question list from top mistake categories
        categories = {}
        for m in mistakes:
            c = m["category"]
            categories[c] = categories.get(c, 0) + 1
        top = sorted(categories.items(), key=lambda x: -x[1])

        st.markdown(speech_bubble(
            "I've looked at your past mistakes and prepared <strong>targeted drill questions</strong> "
            "just for you. Let's fix those weak spots! 🐾",
            mood="thinking",
        ), unsafe_allow_html=True)

        st.markdown("<div class='cody-card' style='margin:12px 0;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>Your Top Mistake Categories</div>", unsafe_allow_html=True)
        for cat, count in top:
            st.markdown(f"<p style='margin:4px 0;color:#444;'>📌 <strong>{cat}</strong>: {count} mistake(s)</p>",
                        unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("▶ Start Targeted Review", use_container_width=True):
            questions = []
            for cat, _ in top:
                qs = TARGETED_QUESTIONS.get(cat, [])
                questions.extend(qs)
            random.shuffle(questions)
            st.session_state.mr_questions = questions
            st.session_state.mr_index = 0
            st.session_state.mr_answered = False
            st.session_state.mr_last_correct = None
            st.session_state.mr_done = False
            st.session_state.mr_correct = 0
            st.rerun()
        return

    # Done
    if st.session_state.mr_done:
        correct = st.session_state.mr_correct
        total = len(st.session_state.mr_questions)
        pct = round(correct / total * 100) if total else 0
        mood = "celebrate" if pct >= 80 else ("thinking" if pct >= 60 else "sad")

        st.markdown(speech_bubble(
            f"Review complete! <strong>{correct}/{total} ({pct}%)</strong>. "
            + ("You're improving! 🎉" if pct >= 80 else "Keep practicing — run this again after reviewing the guide! 💪"),
            mood=mood,
        ), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Run Again", use_container_width=True):
                st.session_state.mr_questions = []
                st.rerun()
        with c2:
            if st.button("📊 See Progress", use_container_width=True):
                go("progress")
        return

    # Active review
    questions = st.session_state.mr_questions
    idx = st.session_state.mr_index
    q = questions[idx]
    total = len(questions)

    st.markdown(progress_bar_html(idx + 1, total, f"Question {idx+1} of {total}"), unsafe_allow_html=True)

    st.markdown(f"""
<div class="cody-card">
  <div style="font-size:1.1rem;font-weight:700;color:#2C1810;">{q['question']}</div>
</div>""", unsafe_allow_html=True)

    if st.session_state.mr_answered:
        correct = st.session_state.mr_last_correct
        if correct:
            st.markdown(f"""
<div class="answer-correct">
  ✅ <strong>Correct!</strong><br>
  <span style="font-size:0.92rem;color:#166534;">💡 {q['explanation']}</span>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class="answer-wrong">
  ❌ Correct answer: <strong>{q['answer']}</strong><br>
  <span style="font-size:0.92rem;color:#7F1D1D;">💡 {q['explanation']}</span>
</div>""", unsafe_allow_html=True)

        is_last = idx >= total - 1
        if st.button("🏁 Finish" if is_last else "Next →"):
            if is_last:
                st.session_state.mr_done = True
                st.rerun()
            else:
                st.session_state.mr_index += 1
                st.session_state.mr_answered = False
                st.session_state.mr_last_correct = None
                st.rerun()
        return

    user_ans = st.text_input("Your answer:", key=f"mr_{idx}", placeholder="Type your answer...")
    if st.button("Submit Answer"):
        n = _norm(user_ans)
        correct_ans = _norm(q["answer"])
        correct = n == correct_ans or any(n == _norm(str(a)) for a in q.get("accept", []))
        if correct:
            st.session_state.mr_correct += 1
        st.session_state.mr_last_correct = correct
        st.session_state.mr_answered = True
        st.rerun()


# ════════════════════════════════════════════════════════════
# PAGE: UPLOAD
# ════════════════════════════════════════════════════════════

def page_upload() -> None:
    from modules.file_reader import analyze_notes

    st.markdown("<h1 style='color:#8B4513;font-weight:900;'>📄 Upload Notes</h1>", unsafe_allow_html=True)
    st.markdown(speech_bubble(
        "Got notes from class? Upload a <strong>.txt file</strong> and I'll read through them, "
        "detect the topic, pull out formulas, and identify what types of questions your teacher focuses on! 🐾",
        mood="reading",
    ), unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload your notes (.txt)", type=["txt"])

    if uploaded:
        text = uploaded.read().decode("utf-8", errors="ignore")
        analysis = analyze_notes(text)

        st.markdown("<div class='cody-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>📊 Analysis Results</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Detected topic:** {analysis['detected_topic']}")
            st.markdown(f"**Word count:** {analysis['word_count']}")
        with col2:
            if analysis["question_types_detected"]:
                types = ", ".join(analysis["question_types_detected"])
                st.markdown(f"**Question types found:** {types}")

        if analysis["key_terms"]:
            st.markdown("<div class='section-heading' style='margin-top:16px;'>Key Terms Found</div>",
                        unsafe_allow_html=True)
            badges = "".join(f"<span class='concept-badge'>{t}</span>" for t in analysis["key_terms"])
            st.markdown(badges, unsafe_allow_html=True)

        if analysis["formulas_found"]:
            st.markdown("<div class='section-heading' style='margin-top:16px;'>Formulas Extracted</div>",
                        unsafe_allow_html=True)
            for formula in analysis["formulas_found"]:
                st.markdown(f"<span class='formula-chip'>{formula}</span>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if analysis["detected_topic"] != "Unknown":
            if st.button(f"📚 Open Study Guide for {analysis['detected_topic']}"):
                go("study_guide")

    st.markdown("""
<div class="cody-card" style="margin-top:20px;border-left:4px solid #3B82F6;">
  <strong>💡 Tip:</strong> Save your class notes as a <code>.txt</code> file and upload here.
  Cody will extract formulas, detect the topic, and help you build a personalised study plan.
</div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# MAIN ROUTER
# ════════════════════════════════════════════════════════════

def main() -> None:
    inject_css()
    init_state()
    sidebar()

    page = st.session_state.page
    if page == "home":
        page_home()
    elif page == "study_guide":
        page_study_guide()
    elif page == "flashcards":
        page_flashcards()
    elif page == "quiz":
        page_quiz()
    elif page == "test":
        page_test()
    elif page == "progress":
        page_progress()
    elif page == "mistake_review":
        page_mistake_review()
    elif page == "upload":
        page_upload()
    else:
        page_home()


if __name__ == "__main__":
    main()
