import streamlit as st
import json
import os
import time
import random
import shelve
from datetime import datetime

st.set_page_config(page_title="სამედიცინო ტესტები", page_icon="🧬", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Georgian:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans Georgian', sans-serif !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 700px !important;
}

header[data-testid="stHeader"] { height: 0 !important; background: transparent !important; }

/* ——— progress bar ——— */
.stProgress > div > div { height: 7px !important; border-radius: 99px !important; background: #e8edf5 !important; }
.stProgress > div > div > div { background: linear-gradient(90deg, #2a6bcd, #4f9cf9) !important; border-radius: 99px !important; transition: width 0.4s ease !important; }

/* ——— კითხვის ბარათი ——— */
.q-card {
    background: linear-gradient(135deg, #1e3a5f 0%, #1a3352 100%);
    border-radius: 18px;
    border: none;
    padding: 22px 24px;
    margin-bottom: 6px;
    box-shadow: 0 4px 18px rgba(20,40,80,0.18);
    position: relative;
    overflow: hidden;
}
.q-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 5px; height: 100%;
    background: linear-gradient(180deg, #4f9cf9, #7ec8ff);
    border-radius: 18px 0 0 18px;
}
.q-card-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #7ec8ff;
    margin-bottom: 10px;
    font-family: 'Noto Sans Georgian', sans-serif;
}
.q-card-text {
    font-size: 17px;
    font-weight: 500;
    line-height: 1.65;
    color: #e8f0fb;
    font-family: 'Noto Sans Georgian', sans-serif;
}

/* ——— სტატუს ბარი ——— */
.status-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    font-family: 'Noto Sans Georgian', sans-serif;
}
.status-left { font-size: 13px; color: #8a93a6; }
.status-right { display: flex; gap: 10px; align-items: center; }
.status-chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 13px;
    font-weight: 600;
}
.chip-correct { background: #f0fdf4; color: #15803d; }
.chip-wrong   { background: #fff2f2; color: #b91c1c; }

/* ——— ვარიანტის ღილაკები ——— */
div.stButton > button[kind="secondary"] {
    font-family: 'Noto Sans Georgian', sans-serif !important;
    font-size: 15.5px !important;
    font-weight: 400 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    align-items: center !important;
    display: flex !important;
    width: 100% !important;
    min-height: 54px !important;
    padding: 13px 16px !important;
    background: #ffffff !important;
    color: #1e2d40 !important;
    border: 1.5px solid #e2e8f4 !important;
    border-radius: 14px !important;
    white-space: normal !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    transition: border-color 0.18s, background 0.18s, box-shadow 0.18s, transform 0.1s !important;
    margin-bottom: 2px !important;
}
div.stButton > button[kind="secondary"]:hover {
    background: #f4f7ff !important;
    border-color: #2a6bcd !important;
    color: #0f1e35 !important;
    box-shadow: 0 2px 10px rgba(42,107,205,0.12) !important;
    transform: translateY(-1px) !important;
}
div.stButton > button[kind="secondary"]:active {
    transform: translateY(0px) !important;
}
div.stButton > button[kind="secondary"] div[data-testid="stMarkdownContainer"] p {
    text-align: left !important;
    width: 100% !important;
    margin: 0 !important;
    font-size: 15.5px !important;
    line-height: 1.5 !important;
}
div.stButton > button[kind="secondary"]:disabled {
    background: #f9fafb !important;
    border-color: #e8edf5 !important;
    color: #9aa3b8 !important;
    opacity: 1 !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ——— სწორი / შეცდომა — ფერები (Python nth-child override-ით) ——— */

/* ——— განმარტების ბარათი ——— */
.explanation-wrap {
    background: #f8faff;
    border-radius: 16px;
    border: 1.5px solid #dde6f8;
    padding: 20px 22px;
    margin-top: 8px;
    animation: fadeSlideUp 0.3s ease;
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.explanation-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #2a6bcd;
    margin-bottom: 10px;
    font-family: 'Noto Sans Georgian', sans-serif;
}
.explanation-body {
    font-size: 15.5px;
    line-height: 1.7;
    color: #1e2d40;
    font-family: 'Noto Sans Georgian', sans-serif;
}

/* ——— primary ღილაკი ——— */
div.stButton > button[kind="primary"] {
    font-family: 'Noto Sans Georgian', sans-serif !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 14px 24px !important;
    border-radius: 14px !important;
    background: linear-gradient(135deg, #2a6bcd, #4f9cf9) !important;
    color: #ffffff !important;
    border: none !important;
    width: 100% !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 3px 14px rgba(42,107,205,0.3) !important;
    transition: box-shadow 0.2s, transform 0.15s !important;
}
div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 5px 20px rgba(42,107,205,0.4) !important;
    transform: translateY(-1px) !important;
}
div.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

/* ——— შედეგების SVG gauge ——— */
.result-gauge-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 8px 0 20px;
}

/* ——— შედეგების ბარათები ——— */
.result-chips {
    display: flex;
    gap: 10px;
    margin-bottom: 18px;
}
.result-chip {
    flex: 1;
    background: #f7f9fc;
    border-radius: 16px;
    border: 1.5px solid #e2e8f4;
    padding: 16px 12px;
    text-align: center;
    font-family: 'Noto Sans Georgian', sans-serif;
}
.result-chip-icon { font-size: 24px; margin-bottom: 4px; }
.result-chip-num  { font-size: 22px; font-weight: 700; color: #1a2845; }
.result-chip-lbl  { font-size: 12px; color: #8a93a6; margin-top: 2px; }

/* ——— სტატისტიკა ——— */
.stat-card {
    background: #f8faff;
    border-radius: 16px;
    border: 1.5px solid #e2e8f4;
    padding: 16px 18px;
    margin-bottom: 10px;
}
.stat-card-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8a93a6;
    margin-bottom: 12px;
    font-family: 'Noto Sans Georgian', sans-serif;
}
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid #eef0f8;
    font-family: 'Noto Sans Georgian', sans-serif;
}
.stat-row:last-child { border-bottom: none; }
.stat-row-label { font-size: 14px; color: #3a4a65; }
.stat-row-value { font-size: 14px; font-weight: 600; color: #1a2845; }
.weak-q-badge {
    display: inline-block;
    background: #fff2f2;
    color: #b91c1c;
    border-radius: 8px;
    padding: 3px 9px;
    font-size: 12.5px;
    font-weight: 600;
    margin: 3px 3px;
    font-family: 'Noto Sans Georgian', sans-serif;
    border: 1px solid #fecaca;
}

/* ——— notification banners ——— */
.banner {
    border-radius: 14px;
    padding: 15px 18px;
    margin-bottom: 14px;
    font-family: 'Noto Sans Georgian', sans-serif;
    animation: fadeSlideUp 0.3s ease;
}
.banner-green { background:#f0fdf4; border:1.5px solid #bbf7d0; }
.banner-yellow { background:#fffbeb; border:1.5px solid #fde68a; }
.banner-red    { background:#fff2f2; border:1.5px solid #fecaca; }
.banner-title  { font-size:16px; font-weight:700; margin:0 0 3px; }
.banner-sub    { font-size:13px; margin:0; }
.banner-green  .banner-title { color:#15803d; }
.banner-green  .banner-sub   { color:#166534; }
.banner-yellow .banner-title { color:#92400e; }
.banner-yellow .banner-sub   { color:#78350f; }
.banner-red    .banner-title { color:#b91c1c; }
.banner-red    .banner-sub   { color:#991b1b; }

input[type="number"] {
    font-family: 'Noto Sans Georgian', sans-serif !important;
    font-size: 16px !important;
    border-radius: 10px !important;
}
button[data-baseweb="tab"] p {
    font-family: 'Noto Sans Georgian', sans-serif !important;
    font-size: 14px !important;
}

/* ——— responsive ——— */
@media (max-width: 600px) {
    .block-container { padding-left: 10px !important; padding-right: 10px !important; }
    .q-card-text { font-size: 16px !important; }
    div.stButton > button[kind="secondary"] { font-size: 14.5px !important; padding: 12px 13px !important; min-height: 50px !important; }
    div.stButton > button[kind="primary"]   { font-size: 15px !important; }
    .explanation-body { font-size: 15px !important; }
    .result-chip-num  { font-size: 20px !important; }
}
@media (min-width: 601px) and (max-width: 1024px) {
    .block-container { padding-left: 20px !important; padding-right: 20px !important; }
}
</style>
""", unsafe_allow_html=True)


# ——— სტატისტიკის ფუნქციები ———
STATS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz_stats")

def load_stats():
    with shelve.open(STATS_FILE) as db:
        return {
            "sessions": db.get("sessions", []),
            "question_wrong_counts": db.get("question_wrong_counts", {}),
        }

def save_session_stats(correct, wrong, total, score, wrong_indices, quiz_data_ref):
    with shelve.open(STATS_FILE) as db:
        sessions = db.get("sessions", [])
        # უნიკალური session id — timestamp-ზე დაფუძნებული
        session_id = datetime.now().strftime("%Y%m%d%H%M%S")
        # შეცდომების ID-ები (ბაზის id ან fallback)
        wrong_ids = [quiz_data_ref[idx].get("id", idx + 1) for idx in wrong_indices]
        sessions.append({
            "session_id": session_id,
            "date":       datetime.now().strftime("%d/%m/%Y %H:%M"),
            "correct":    correct,
            "wrong":      wrong,
            "total":      total,
            "score":      round(score, 1),
            "wrong_ids":  wrong_ids,
        })
        db["sessions"] = sessions[-20:]
        q_wrong = db.get("question_wrong_counts", {})
        for idx in wrong_indices:
            key = str(quiz_data_ref[idx].get("id", idx + 1))
            q_wrong[key] = q_wrong.get(key, 0) + 1
        db["question_wrong_counts"] = q_wrong

def clear_stats():
    with shelve.open(STATS_FILE) as db:
        db["sessions"] = []
        db["question_wrong_counts"] = {}

def load_marked() -> set:
    """რთულად მონიშნული კითხვების array index-ების სეტი."""
    with shelve.open(STATS_FILE) as db:
        return set(db.get("marked_indices", []))

def save_marked(marked: set):
    with shelve.open(STATS_FILE) as db:
        db["marked_indices"] = list(marked)

def score_gauge_svg(score):
    """SVG gauge შედეგის ვიზუალიზაციისთვის."""
    pct = min(max(score, 0), 100)
    # ფერი score-ის მიხედვით
    if pct >= 80:
        clr1, clr2, txt_clr = "#16a34a", "#4ade80", "#15803d"
        emoji = "🎉"
    elif pct >= 60:
        clr1, clr2, txt_clr = "#d97706", "#fbbf24", "#92400e"
        emoji = "👍"
    else:
        clr1, clr2, txt_clr = "#dc2626", "#f87171", "#b91c1c"
        emoji = "📚"

    r = 70
    cx, cy = 90, 90
    circumference = 3.14159 * r  # ნახევარი წრე
    dash = (pct / 100) * circumference
    gap = circumference - dash

    return f"""
    <div class="result-gauge-wrap">
      <svg width="180" height="110" viewBox="0 0 180 110">
        <defs>
          <linearGradient id="ggrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{clr1}"/>
            <stop offset="100%" stop-color="{clr2}"/>
          </linearGradient>
        </defs>
        <!-- ფონის ნახევარ-წრე -->
        <path d="M{cx-r},{cy} A{r},{r} 0 0,1 {cx+r},{cy}"
              fill="none" stroke="#e8edf5" stroke-width="14" stroke-linecap="round"/>
        <!-- შევსების ნახევარ-წრე -->
        <path d="M{cx-r},{cy} A{r},{r} 0 0,1 {cx+r},{cy}"
              fill="none" stroke="url(#ggrad)" stroke-width="14" stroke-linecap="round"
              stroke-dasharray="{dash:.1f} {gap:.1f}"
              stroke-dashoffset="0"/>
        <!-- ტექსტი ცენტრში -->
        <text x="{cx}" y="{cy-8}" text-anchor="middle"
              font-size="28" font-weight="700" fill="{txt_clr}"
              font-family="Noto Sans Georgian, sans-serif">{pct:.0f}%</text>
        <text x="{cx}" y="{cy+14}" text-anchor="middle"
              font-size="18" fill="{txt_clr}">{emoji}</text>
      </svg>
    </div>
    """

# ——— კითხვების ჩატვირთვა და ნორმალიზება ———

import re as _re

def _extract_number_from_question(text: str):
    """
    თუ კითხვა იწყება ნომრით (მაგ. "1. რა არის..." ან "42) რა არის..."),
    აბრუნებს (ნომერი, გაწმენდილი_ტექსტი). წინააღმდეგ შემთხვევაში (None, text).
    """
    m = _re.match(r"^\s*(\d+)\s*[.):\-–]\s*", text)
    if m:
        num = int(m.group(1))
        clean = text[m.end():]
        return num, clean
    return None, text

def _normalize_entry(raw: dict, fallback_idx: int) -> dict:
    """
    ერთ JSON ჩანაწერს გადაიყვანს სტანდარტულ ფორმატში:
    {
        "id":          int,   # 1-დან დაწყებული
        "question":    str,   # ნომრის გარეშე
        "options":     list,  # სტრინგების სია
        "correct":     int,   # 0-based ინდექსი options-ში
        "explanation": str,
    }
    მხარს უჭერს:
      - id ველი (int ან str)
      - ნომერი პირდაპირ question-ში ("1. კითხვა..." ან "1) კითხვა...")
      - id არ არის და question-შიც ნომერი არ არის → fallback_idx+1
      - correct: int (0-based), int (1-based როცა >0 და == len(options)),
                 str ("A"/"B"/"C"/"D" ან "ა"/"ბ"/"გ"/"დ" ან "0"/"1"...)
      - options: list ან dict {"A": "...", "B": "..."}
    """
    # ——— id ———
    raw_id = raw.get("id")
    if raw_id is not None:
        try:
            entry_id = int(raw_id)
        except (ValueError, TypeError):
            entry_id = fallback_idx + 1
    else:
        entry_id = None  # შევამოწმებთ question-ში

    # ——— question ———
    question_raw = str(raw.get("question") or raw.get("Question") or "კითხვა არ მოიძებნა")
    num_in_q, question_clean = _extract_number_from_question(question_raw)

    if entry_id is None:
        entry_id = num_in_q if num_in_q is not None else (fallback_idx + 1)

    # ——— options ———
    raw_opts = raw.get("options") or raw.get("Options") or raw.get("choices") or []
    LETTER_MAP_EN = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5}
    LETTER_MAP_KA = {"ა": 0, "ბ": 1, "გ": 2, "დ": 3, "ე": 4, "ვ": 5}

    if isinstance(raw_opts, dict):
        # {"A": "ტექსტი", "B": "ტექსტი"} სახე
        sorted_keys = sorted(raw_opts.keys(), key=lambda k: LETTER_MAP_EN.get(k.lower(), ord(k)))
        options = [str(raw_opts[k]) for k in sorted_keys]
    elif isinstance(raw_opts, list):
        options = [str(o) for o in raw_opts]
    else:
        options = []

    if not options:
        options = ["პასუხი არ მოიძებნა"]


    # ——— correct ———
    # ველების პრიორიტეტი: "correct" → "correct_answer" → "answer" → 0
    # (or გარეშე, რათა "0" და 0 არ დაიკარგოს falsy-ობის გამო)
    if "correct" in raw and raw["correct"] is not None:
        raw_correct = raw["correct"]
    elif "correct_answer" in raw and raw["correct_answer"] is not None:
        raw_correct = raw["correct_answer"]
    elif "answer" in raw and raw["answer"] is not None:
        raw_correct = raw["answer"]
    else:
        raw_correct = 0

    correct_idx = 0
    n_opts = len(options)

    if isinstance(raw_correct, int):
        # int ყოველთვის ინდექსია: 0 → 0-based, 1..n → 1-based
        if raw_correct == 0:
            correct_idx = 0
        elif 1 <= raw_correct <= n_opts:
            correct_idx = raw_correct - 1
        else:
            correct_idx = 0

    elif isinstance(raw_correct, str):
        s  = raw_correct.strip()
        sl = s.lower()

        # 1. ასო-კოდი: "a","b","c" ან "ა","ბ","გ"
        if sl in LETTER_MAP_EN:
            correct_idx = LETTER_MAP_EN[sl]

        elif s in LETTER_MAP_KA:
            correct_idx = LETTER_MAP_KA[s]

        else:
            # 2. პირველ რიგში ვეძებთ options-ში ზუსტი დამთხვევით
            #    ("1" → "1", "1. 2. 3" → "1. 2. 3" და ა.შ.)
            found = False
            for i, opt in enumerate(options):
                if opt.strip().lower() == sl:
                    correct_idx = i
                    found = True
                    break

            # 3. თუ ტექსტით ვერ იპოვა — მხოლოდ მაშინ ვცდით ინდექსად
            if not found:
                try:
                    v = int(s)
                    if v == 0:
                        correct_idx = 0
                    elif 1 <= v <= n_opts:
                        correct_idx = v - 1
                    else:
                        correct_idx = 0
                except ValueError:
                    correct_idx = 0



    # ——— explanation ———
    explanation = str(
        raw.get("explanation") or raw.get("Explanation") or
        raw.get("rationale") or raw.get("comment") or ""
    )
    if not explanation:
        explanation = "განმარტება არ მოიძებნა."

    return {
        "id":          entry_id,
        "question":    question_clean.strip(),
        "options":     options,
        "correct":     correct_idx,
        "explanation": explanation,
    }

@st.cache_data(show_spinner=False)
def load_quiz_data():
    """
    ჩატვირთავს და ანორმალიზებს questions.json-ს.
    მხარს უჭერს:
      - სია სახის JSON: [{...}, {...}]
      - ობიექტ სახის JSON: {"questions": [...]}  ან  {"data": [...]}
      - შერეული ფორმატები (id-ით და id-ის გარეშე ერთად)
      - 3000+ კითხვა (cache_data უზრუნველყოფს ერთჯერად დამუშავებას)
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path   = os.path.join(current_dir, "questions.json")

    if not os.path.exists(json_path):
        return []

    with open(json_path, "r", encoding="utf-8", errors="replace") as f:
        raw = json.load(f)

    # სია პირდაპირ, ან wrapper ობიექტი
    if isinstance(raw, list):
        raw_list = raw
    elif isinstance(raw, dict):
        raw_list = (
            raw.get("questions") or raw.get("data") or
            raw.get("items")     or raw.get("quiz")  or []
        )
    else:
        return []

    result = []
    for i, entry in enumerate(raw_list):
        if not isinstance(entry, dict):
            continue
        try:
            result.append(_normalize_entry(entry, i))
        except Exception:
            # ერთი ჩანაწერის შეცდომა მთელ ბაზას არ ჩააგდებს
            continue

    return result

quiz_data = load_quiz_data()

if not quiz_data:
    st.error("ვერ მოიძებნა 'questions.json' ფაილი ან ის ცარიელია!")
    st.stop()

# ID → array index რუქა (სწრაფი ძებნისთვის)
# თუ ყველა კითხვას აქვს უნიკალური id — ვიყენებთ id-ს
# თუ id-ები არ არის ან მეორდება — fallback: პოზიცია+1
_id_list  = [q.get("id") for q in quiz_data]
_has_ids  = all(x is not None for x in _id_list)
_unique   = len(set(_id_list)) == len(_id_list)
USE_IDS   = _has_ids and _unique

if USE_IDS:
    ID_TO_IDX = {q["id"]: i for i, q in enumerate(quiz_data)}
    ALL_IDS   = sorted(ID_TO_IDX.keys())
    MIN_ID, MAX_ID = ALL_IDS[0], ALL_IDS[-1]
else:
    ID_TO_IDX = {}
    MIN_ID, MAX_ID = 1, len(quiz_data)

TOTAL_QUESTIONS = len(quiz_data)


# ——— session_state ინიციალიზაცია ———
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started    = False
    st.session_state.current_idx     = 0
    st.session_state.correct_count   = 0
    st.session_state.wrong_count     = 0
    st.session_state.wrong_indices   = []
    st.session_state.review_mode     = False
    st.session_state.review_round    = 0
    st.session_state.active_indices  = []
    st.session_state.has_responded   = False
    st.session_state.user_choice     = None
    st.session_state.auto_advance_flash = False
    st.session_state.review_wrong_indices = []
    st.session_state.option_order_map = {}
    st.session_state.stats_saved     = False
    st.session_state.shuffle_on      = True
    st.session_state.selected_session = None
    st.session_state.marked_indices  = load_marked()


# ——— საწყისი ეკრანი ———
if not st.session_state.quiz_started:

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a2845 0%, #1e5bb8 60%, #4f9cf9 100%);
        border-radius: 20px;
        padding: 30px 24px 26px;
        margin-bottom: 22px;
        text-align: center;
        box-shadow: 0 6px 28px rgba(42,107,205,0.22);
    ">
        <div style="font-size:40px; margin-bottom:10px; filter:drop-shadow(0 2px 4px rgba(0,0,0,0.2));">🧬</div>
        <div style="font-size:23px; font-weight:700; color:#ffffff; font-family:'Noto Sans Georgian',sans-serif; margin-bottom:7px; letter-spacing:-0.01em;">
            სამედიცინო ტესტები
        </div>
        <div style="display:inline-block; background:rgba(255,255,255,0.15); border-radius:99px; padding:5px 16px;">
            <span style="font-size:13px; color:rgba(255,255,255,0.9); font-family:'Noto Sans Georgian',sans-serif;">
                ბაზაში სულ <strong style="color:#fff;">{TOTAL_QUESTIONS}</strong> კითხვა
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝  ტესტი", "📊  სტატისტიკა"])

    with tab1:
        st.markdown('<p style="font-size:15px; font-weight:600; color:#1a2845; margin-bottom:12px; font-family:\'Noto Sans Georgian\',sans-serif;">⚙️ კითხვების დიაპაზონი</p>', unsafe_allow_html=True)

        if USE_IDS:
            range_hint = f"ID {MIN_ID} – {MAX_ID}"
        else:
            range_hint = f"1 – {TOTAL_QUESTIONS}"

        st.markdown(f'<p style="font-size:12px; color:#8a93a6; margin-bottom:8px; font-family:\'Noto Sans Georgian\',sans-serif;">დიაპაზონი: {range_hint}</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            start_q = st.number_input("საიდან:", min_value=MIN_ID, max_value=MAX_ID, value=MIN_ID, step=1)
        with col2:
            end_q = st.number_input("სადამდე:", min_value=MIN_ID, max_value=MAX_ID,
                                     value=min(MIN_ID + 2372, MAX_ID), step=1)

        shuffle_on = st.checkbox("🔀 კითხვები და ვარიანტები შეირიოს", value=True)

        if start_q > end_q:
            st.markdown('<div class="banner banner-red"><p class="banner-title">⚠️ საწყისი კითხვა საბოლოოზე მეტია!</p></div>', unsafe_allow_html=True)
        else:
            if USE_IDS:
                # ID-ების მიხედვით — ვიღებთ მხოლოდ იმ ელემენტებს, რომელთა id დიაპაზონშია
                indices = [ID_TO_IDX[i] for i in ALL_IDS if start_q <= i <= end_q]
            else:
                indices = list(range(start_q - 1, end_q))

            q_count = len(indices)
            st.markdown(
                f'<p style="color:#5a6a85; font-size:14px; margin:8px 0 16px; font-family:\'Noto Sans Georgian\',sans-serif;">'
                f'შეირჩა <strong style="color:#2a6bcd">{q_count}</strong> კითხვა</p>',
                unsafe_allow_html=True
            )
            if st.button("🚀  ტესტირების დაწყება", type="primary", use_container_width=True):
                if shuffle_on:
                    random.shuffle(indices)
                st.session_state.active_indices  = indices
                st.session_state.shuffle_on      = shuffle_on
                st.session_state.quiz_started    = True
                st.session_state.stats_saved     = False
                st.rerun()

            # ——— რთული კითხვების გავლა ———
            marked = st.session_state.marked_indices
            if marked:
                marked_in_range = [idx for idx in indices if idx in marked]
                if marked_in_range:
                    st.markdown('<div style="margin-top:8px;"></div>', unsafe_allow_html=True)
                    if st.button(f"⭐  მხოლოდ რთული კითხვები  ({len(marked_in_range)} კ.)",
                                 use_container_width=True):
                        m_list = list(marked_in_range)
                        st.session_state.active_indices = m_list
                        st.session_state.shuffle_on     = False
                        st.session_state.quiz_started   = True
                        st.session_state.stats_saved    = False
                        st.rerun()

            # ——— ყველა რთული (დიაპაზონის გარეშე) ———
            all_marked = list(st.session_state.marked_indices)
            if all_marked and len(all_marked) != len(marked_in_range if marked else []):
                st.markdown(f'<p style="font-size:12px; color:#8a93a6; margin:4px 0 0; font-family:\'Noto Sans Georgian\',sans-serif;">სულ ⭐ მონიშნული: <strong style="color:#d97706">{len(all_marked)}</strong> კითხვა ბაზაში</p>', unsafe_allow_html=True)

    with tab2:
        if "selected_session" not in st.session_state:
            st.session_state.selected_session = None

        stats    = load_stats()
        sessions = stats["sessions"]
        q_wrong  = stats["question_wrong_counts"]

        # კომპაქტური სტილი — spacing-ის მოხსნა
        st.markdown("""
        <style>
        /* tab2-ის შიგნით ყველა element-ს შორის gap მინიმუმამდე */
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div {
            gap: 0 !important;
        }
        /* retry ღილაკი expand-ში */
        .ses-expand div.stButton > button[kind="primary"] {
            min-height: 36px !important;
            padding: 7px 14px !important;
            font-size: 13px !important;
            border-radius: 8px !important;
            box-shadow: none !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if not sessions:
            st.markdown(
                '<div style="text-align:center; padding:36px 0; color:#8a93a6; font-family:\'Noto Sans Georgian\',sans-serif; font-size:15px; line-height:1.8;">'
                '🗂️ სტატისტიკა ჯერ არ გაქვთ.<br>პირველი ტესტის შემდეგ გამოჩნდება.</div>',
                unsafe_allow_html=True
            )
        else:
            all_scores = [s["score"] for s in sessions]
            all_total  = sum(s["total"] for s in sessions)
            avg_score  = sum(all_scores) / len(all_scores)
            best_score = max(all_scores)

            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-title">ზოგადი მაჩვენებლები</div>
                <div class="stat-row"><span class="stat-row-label">სულ ტესტი</span><span class="stat-row-value">{len(sessions)}</span></div>
                <div class="stat-row"><span class="stat-row-label">სულ კითხვა</span><span class="stat-row-value">{all_total}</span></div>
                <div class="stat-row"><span class="stat-row-label">საშუალო</span><span class="stat-row-value">{avg_score:.1f}%</span></div>
                <div class="stat-row"><span class="stat-row-label">საუკეთესო</span><span class="stat-row-value">🏆 {best_score:.1f}%</span></div>
            </div>
            """, unsafe_allow_html=True)

            # ——— სესიების სია: selectbox + HTML ბლოკი ———
            st.markdown('<div style="font-size:11px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:#8a93a6; margin:14px 0 6px; font-family:\'Noto Sans Georgian\',sans-serif;">სესიების ისტორია</div>', unsafe_allow_html=True)

            reversed_sessions = list(reversed(sessions))

            # ——— სესიების სია: st.expander native accordion ———
            st.markdown("""
            <style>
            /* expander-ების სტილი — კომპაქტური სია */
            div[data-testid="stExpander"] {
                border: none !important;
                border-bottom: 1px solid #eef1f8 !important;
                border-radius: 0 !important;
                background: #ffffff !important;
                box-shadow: none !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            div[data-testid="stExpander"]:first-of-type {
                border-radius: 12px 12px 0 0 !important;
                border-top: 1.5px solid #e2e8f4 !important;
            }
            div[data-testid="stExpander"]:last-of-type {
                border-radius: 0 0 12px 12px !important;
                border-bottom: 1.5px solid #e2e8f4 !important;
            }
            div[data-testid="stExpander"] summary {
                padding: 9px 14px !important;
                font-size: 13.5px !important;
                font-family: 'Noto Sans Georgian', sans-serif !important;
                font-weight: 500 !important;
                color: #2d3f5e !important;
                min-height: 0 !important;
            }
            div[data-testid="stExpander"] summary:hover {
                background: #f4f7ff !important;
            }
            div[data-testid="stExpander"] summary svg {
                width: 14px !important;
                height: 14px !important;
                color: #8a93a6 !important;
            }
            div[data-testid="stExpander"] > div[data-testid="stExpanderDetails"] {
                padding: 0 14px 10px !important;
                background: #f8faff !important;
                border-top: 1px solid #e8edf8 !important;
            }
            /* expander wrapper — margin ამოვიღოთ */
            div[data-testid="stExpander"] + div[data-testid="stExpander"] {
                margin-top: 0 !important;
            }
            </style>
            """, unsafe_allow_html=True)

            st.markdown('<div style="font-size:11px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:#8a93a6; margin:14px 0 4px; font-family:\'Noto Sans Georgian\',sans-serif;">სესიების ისტორია</div>', unsafe_allow_html=True)

            # expander-ების გარე wrapper — ერთიანი ჩარჩო
            st.markdown('<div style="border:1.5px solid #e2e8f4; border-radius:12px; overflow:hidden;">', unsafe_allow_html=True)

            for i, s in enumerate(reversed_sessions):
                sid       = s.get("session_id", str(i))
                wrong_ids = s.get("wrong_ids", [])
                icon      = "🟢" if s["score"] >= 80 else ("🟡" if s["score"] >= 60 else "🔴")
                clr       = "#15803d" if s["score"] >= 80 else ("#92400e" if s["score"] >= 60 else "#b91c1c")

                label = f"{icon} {s['date']}  ·  {s['total']} კ.  ·  **{s['score']}%**"

                with st.expander(label, expanded=False):
                    if wrong_ids:
                        badges = "".join([f'<span class="weak-q-badge">#{qid}</span>' for qid in wrong_ids])
                        st.markdown(f"""
                        <div style="font-size:11px; font-weight:700; letter-spacing:0.07em; text-transform:uppercase;
                                    color:#8a93a6; margin:8px 0 6px; font-family:'Noto Sans Georgian',sans-serif;">
                            ❌ შეცდომები — {len(wrong_ids)} კითხვა
                        </div>
                        <div style="line-height:2.3; margin-bottom:8px;">{badges}</div>
                        """, unsafe_allow_html=True)

                        if st.button(f"🔁 გავლა ({len(wrong_ids)} კ.)",
                                     key=f"retry_{sid}", type="primary"):
                            if USE_IDS:
                                retry_indices = [ID_TO_IDX[qid] for qid in wrong_ids if qid in ID_TO_IDX]
                            else:
                                retry_indices = [qid - 1 for qid in wrong_ids if 0 < qid <= TOTAL_QUESTIONS]
                            if retry_indices:
                                st.session_state.quiz_started          = True
                                st.session_state.review_mode           = True
                                st.session_state.review_round          = 1
                                st.session_state.active_indices        = retry_indices
                                st.session_state.shuffle_on            = False
                                st.session_state.current_idx           = 0
                                st.session_state.has_responded         = False
                                st.session_state.user_choice           = None
                                st.session_state.auto_advance_flash    = False
                                st.session_state.review_wrong_indices  = []
                                st.session_state.option_order_map      = {}
                                st.session_state.stats_saved           = False
                                st.session_state.selected_session      = None
                                st.rerun()
                    else:
                        st.markdown('<p style="font-size:13px; color:#15803d; margin:8px 0; font-family:\'Noto Sans Georgian\',sans-serif;">🎉 შეცდომები არ ყოფილა!</p>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # ——— ყველაზე ხშირი შეცდომები ———
            if q_wrong:
                sorted_wrong = sorted(q_wrong.items(), key=lambda x: x[1], reverse=True)[:12]
                badges = "".join([f'<span class="weak-q-badge">#{qn} ({cnt}✗)</span>' for qn, cnt in sorted_wrong])
                st.markdown(f"""
                <div class="stat-card" style="margin-top:14px;">
                    <div class="stat-card-title">ყველაზე ხშირი შეცდომები</div>
                    <div style="padding:4px 0; line-height:2.4;">{badges}</div>
                    <div style="font-size:12px; color:#8a93a6; margin-top:4px; font-family:'Noto Sans Georgian',sans-serif;">ფრჩხილში — რამდენჯერ შეგეშალა</div>
                </div>
                """, unsafe_allow_html=True)

            st.write("")
            if st.button("🗑️  სტატისტიკის გასუფთავება", use_container_width=True):
                clear_stats()
                st.session_state.selected_session = None
                st.rerun()

            # ——— ⭐ მონიშნული კითხვები ———
            marked = st.session_state.get("marked_indices", set())
            if marked:
                marked_ids = sorted([quiz_data[i].get("id", i+1) for i in marked])
                badges = "".join([f'<span class="weak-q-badge" style="background:#fffbeb; color:#b45309; border-color:#fcd34d;">⭐ #{qid}</span>' for qid in marked_ids])
                st.markdown(f"""
                <div class="stat-card" style="margin-top:10px; border-color:#fde68a;">
                    <div class="stat-card-title" style="color:#b45309;">⭐ მონიშნული რთული კითხვები — {len(marked)}</div>
                    <div style="padding:4px 0; line-height:2.4;">{badges}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"⭐  ყველა რთული კითხვის გავლა  ({len(marked)} კ.)",
                             key="start_marked_stats", use_container_width=True):
                    m_list = list(marked)
                    st.session_state.quiz_started       = True
                    st.session_state.review_mode        = False
                    st.session_state.active_indices     = m_list
                    st.session_state.shuffle_on         = False
                    st.session_state.current_idx        = 0
                    st.session_state.correct_count      = 0
                    st.session_state.wrong_count        = 0
                    st.session_state.wrong_indices      = []
                    st.session_state.has_responded      = False
                    st.session_state.user_choice        = None
                    st.session_state.auto_advance_flash = False
                    st.session_state.option_order_map   = {}
                    st.session_state.stats_saved        = False
                    st.rerun()

                if st.button("🗑️  მონიშვნების გასუფთავება", key="clear_marked", use_container_width=True):
                    st.session_state.marked_indices = set()
                    save_marked(set())
                    st.rerun()

    st.stop()


# ——— კითხვის ეკრანი — safety guards ———
if "option_order_map"      not in st.session_state: st.session_state.option_order_map      = {}
if "stats_saved"           not in st.session_state: st.session_state.stats_saved           = False
if "shuffle_on"            not in st.session_state: st.session_state.shuffle_on            = True
if "review_wrong_indices"  not in st.session_state: st.session_state.review_wrong_indices  = []
if "review_round"          not in st.session_state: st.session_state.review_round          = 0
if "review_mode"           not in st.session_state: st.session_state.review_mode           = False

active_indices = st.session_state.active_indices
current_idx    = st.session_state.current_idx

LETTERS = ["ა", "ბ", "გ", "დ", "ე", "ვ"]

if current_idx < len(active_indices):
    real_idx = active_indices[current_idx]
    q_data   = quiz_data[real_idx]


    # ვარიანტების shuffle — ერთხელ გენერირდება და ინახება order+correct_idx ერთად
    if current_idx not in st.session_state.option_order_map:
        order = list(range(len(q_data["options"])))
        if st.session_state.shuffle_on:
            random.shuffle(order)
        # correct_idx ერთხელ ვთვლით და ვინახავთ — ყოველ render-ზე აღარ გამოითვლება
        st.session_state.option_order_map[current_idx] = {
            "order":   order,
            "correct": order.index(q_data["correct"]),
        }

    saved        = st.session_state.option_order_map[current_idx]
    option_order = saved["order"]
    correct_idx  = saved["correct"]

    mode_txt = f" · გადახედვა #{st.session_state.review_round}" if st.session_state.review_mode else ""
    db_id = q_data.get("id", real_idx + 1)

    # ——— counter-ები: review-ში ახლიდან ითვლება ცალკე ველებიდან ———
    if st.session_state.review_mode:
        answered_so_far = [x for x in st.session_state.review_wrong_indices if x in active_indices[:current_idx]]
        chip_wrong   = len(answered_so_far)
        chip_correct = current_idx - chip_wrong
    else:
        chip_correct = st.session_state.correct_count
        chip_wrong   = st.session_state.wrong_count

    # ——— სტატუს ბარი ———
    review_prefix = f'🔁 გადახედვა #{st.session_state.review_round} &nbsp;·&nbsp; ' if st.session_state.review_mode else ''
    is_marked_status = real_idx in st.session_state.get("marked_indices", set())
    star_badge = '&nbsp;<span style="color:#f59e0b; font-size:13px;">⭐</span>' if is_marked_status else ''
    st.markdown(f"""
    <div class="status-bar">
        <span class="status-left">
            {review_prefix}კითხვა {current_idx+1}/{len(active_indices)} &nbsp;·&nbsp; <span style="color:#b0bac9;">#{db_id}</span>{star_badge}
        </span>
        <span class="status-right">
            <span class="status-chip chip-correct">✅ {chip_correct}</span>
            <span class="status-chip chip-wrong">❌ {chip_wrong}</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ——— პროგრეს ბარი — pure HTML ———
    pct = int((current_idx + 1) / len(active_indices) * 100)
    st.markdown(f"""
    <div style="height:7px; background:#e8edf5; border-radius:99px; margin-bottom:16px; overflow:hidden;">
        <div style="height:100%; width:{pct}%; background:linear-gradient(90deg,#2a6bcd,#4f9cf9);
             border-radius:99px; transition:width 0.4s ease;"></div>
    </div>
    """, unsafe_allow_html=True)

    # ——— კითხვის ბარათი ———
    st.markdown(f"""
    <div class="q-card">
        <div class="q-card-label">🩺 კითხვა</div>
        <div class="q-card-text">{q_data["question"]}</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    options = q_data["options"]

    # ——— ფერების CSS override ———
    if st.session_state.has_responded:
        correct_child = correct_idx + 1
        chosen_child  = st.session_state.user_choice + 1

        css = f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-child({correct_child}) button[kind="secondary"]:disabled {{
            background: #f0fdf4 !important;
            border-color: #22c55e !important;
            color: #15803d !important;
            font-weight: 600 !important;
            box-shadow: 0 0 0 3px rgba(34,197,94,0.15) !important;
        }}
        """
        if st.session_state.user_choice != correct_idx:
            css += f"""
            div[data-testid="stVerticalBlock"] > div:nth-child({chosen_child}) button[kind="secondary"]:disabled {{
                background: #fff2f2 !important;
                border-color: #ef4444 !important;
                color: #b91c1c !important;
                font-weight: 600 !important;
                box-shadow: 0 0 0 3px rgba(239,68,68,0.12) !important;
            }}
            """
        css += "</style>"
        st.markdown(css, unsafe_allow_html=True)

    # ——— ვარიანტები ———
    with st.container():
        for display_idx, original_idx in enumerate(option_order):
            letter = LETTERS[display_idx] if display_idx < len(LETTERS) else str(display_idx + 1)
            label  = f"**{letter}**  ·  {options[original_idx]}"
            if st.button(label, key=f"opt_{current_idx}_{display_idx}",
                         disabled=st.session_state.has_responded,
                         use_container_width=True):
                st.session_state.has_responded = True
                st.session_state.user_choice   = display_idx

                if display_idx == correct_idx:
                    if not st.session_state.review_mode:
                        st.session_state.correct_count += 1
                    st.session_state.auto_advance_flash = True
                else:
                    if not st.session_state.review_mode:
                        st.session_state.wrong_count += 1
                        if real_idx not in st.session_state.wrong_indices:
                            st.session_state.wrong_indices.append(real_idx)
                    else:
                        if real_idx not in st.session_state.review_wrong_indices:
                            st.session_state.review_wrong_indices.append(real_idx)
                st.rerun()

    # სწორ პასუხზე: ღილაკები render-ია → მწვანე ჩანს → ვიცდით → გადადის
    if st.session_state.auto_advance_flash:
        time.sleep(0.7)
        st.session_state.current_idx       += 1
        st.session_state.has_responded      = False
        st.session_state.user_choice        = None
        st.session_state.auto_advance_flash = False
        st.rerun()

    # განმარტება — მხოლოდ შეცდომაზე
    if st.session_state.has_responded and not st.session_state.auto_advance_flash:
        st.markdown(f"""
        <div class="explanation-wrap">
            <div class="explanation-label">💡 სამედიცინო განმარტება</div>
            <div class="explanation-body">{q_data["explanation"]}</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

    # ——— ნავიგაციის ღილაკები ———
    # CSS key-ის მიხედვით — Streamlit button key → data-testid="stButton" შვილი
    prev_disabled = current_idx == 0
    next_label    = "შემდეგი ›" if st.session_state.has_responded else "გამოტოვება ›"

    st.markdown(f"""
    <style>
    /* nav_prev */
    div[data-testid="stButton"]:has(button[kind="secondary"][data-testid="baseButton-secondary"]:nth-of-type(1)) {{}}
    button[kind="secondary"][key="nav_prev"],
    #nav_prev button,
    [data-testid="nav_prev"] button {{
        background: #eef2f9 !important;
    }}
    /* ნავიგაციის ღილაკების wrapper — column-ების შემდეგ ბოლო ორი secondary button */
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] {{
        background: #eef2f9 !important;
        border: 1.5px solid #d4dcea !important;
        color: #3d5280 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        min-height: 40px !important;
        padding: 8px 12px !important;
        border-radius: 10px !important;
        box-shadow: none !important;
        transform: none !important;
        transition: background 0.15s, border-color 0.15s !important;
    }}
    div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {{
        background: #dce4f5 !important;
        border-color: #a8bcd8 !important;
        color: #1e2d40 !important;
        transform: none !important;
        box-shadow: none !important;
    }}
    div[data-testid="stHorizontalBlock"] button[kind="secondary"]:disabled {{
        background: #f5f7fb !important;
        border-color: #e4e9f2 !important;
        color: #b8c4d8 !important;
        transform: none !important;
        box-shadow: none !important;
        opacity: 1 !important;
    }}
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] p {{
        font-size: 14px !important;
        color: inherit !important;
    }}
    </style>
    <div style="margin-top:10px;"></div>
    """, unsafe_allow_html=True)

    nav_col1, nav_col2 = st.columns([1, 1])

    with nav_col1:
        if st.button("‹ წინა",
                     key="nav_prev",
                     disabled=prev_disabled,
                     use_container_width=True):
            st.session_state.current_idx       -= 1
            st.session_state.has_responded      = False
            st.session_state.user_choice        = None
            st.session_state.auto_advance_flash = False
            st.rerun()

    with nav_col2:
        if st.button(next_label,
                     key="nav_next",
                     use_container_width=True):
            st.session_state.current_idx       += 1
            st.session_state.has_responded      = False
            st.session_state.user_choice        = None
            st.session_state.auto_advance_flash = False
            st.rerun()

    # ——— ⭐ მარკირების ღილაკი ———
    if "marked_indices" not in st.session_state:
        st.session_state.marked_indices = load_marked()

    is_marked  = real_idx in st.session_state.marked_indices
    star_label = "⭐  რთულია — მონიშნულია" if is_marked else "☆  მონიშვნა როგორც რთული"
    star_bg    = "#fffbeb" if is_marked else "#f8faff"
    star_brd   = "#f59e0b" if is_marked else "#dde6f8"
    star_clr   = "#b45309" if is_marked else "#8a93a6"
    star_fw    = "600"     if is_marked else "400"

    st.markdown(f"""
    <style>
    div[data-testid="stButton"]:has(button[key="star_toggle"]) button {{
        background: {star_bg} !important;
        border: 1.5px solid {star_brd} !important;
        color: {star_clr} !important;
        min-height: 36px !important;
        padding: 6px 14px !important;
        font-size: 13px !important;
        border-radius: 10px !important;
        box-shadow: none !important;
        transform: none !important;
        font-weight: {star_fw} !important;
    }}
    div[data-testid="stButton"]:has(button[key="star_toggle"]) button:hover {{
        background: #fef3c7 !important;
        border-color: #f59e0b !important;
        color: #92400e !important;
    }}
    </style>
    <div style="margin-top:4px;"></div>
    """, unsafe_allow_html=True)

    if st.button(star_label, key="star_toggle", use_container_width=True):
        if is_marked:
            st.session_state.marked_indices.discard(real_idx)
        else:
            st.session_state.marked_indices.add(real_idx)
        save_marked(st.session_state.marked_indices)
        st.rerun()


# ——— შედეგების / გადახედვის ეკრანი ———
else:
    if not st.session_state.review_mode:
        total = st.session_state.correct_count + st.session_state.wrong_count
        score = (st.session_state.correct_count / total * 100) if total > 0 else 0

        if not st.session_state.stats_saved:
            save_session_stats(
                st.session_state.correct_count,
                st.session_state.wrong_count,
                total, score,
                st.session_state.wrong_indices,
                quiz_data
            )
            st.session_state.stats_saved = True

        st.balloons()

        st.markdown('<p style="font-size:20px; font-weight:700; color:#1a2845; margin-bottom:4px; font-family:\'Noto Sans Georgian\',sans-serif;">📊 ტესტირების შედეგები</p>', unsafe_allow_html=True)

        # SVG Gauge
        st.markdown(score_gauge_svg(score), unsafe_allow_html=True)

        # 3 ბარათი
        st.markdown(f"""
        <div class="result-chips">
            <div class="result-chip">
                <div class="result-chip-icon">✅</div>
                <div class="result-chip-num" style="color:#15803d;">{st.session_state.correct_count}</div>
                <div class="result-chip-lbl">სწორი</div>
            </div>
            <div class="result-chip">
                <div class="result-chip-icon">❌</div>
                <div class="result-chip-num" style="color:#b91c1c;">{st.session_state.wrong_count}</div>
                <div class="result-chip-lbl">შეცდომა</div>
            </div>
            <div class="result-chip">
                <div class="result-chip-icon">📝</div>
                <div class="result-chip-num">{total}</div>
                <div class="result-chip-lbl">სულ</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if score >= 80:
            st.markdown('<div class="banner banner-green"><p class="banner-title">🎉 შესანიშნავი შედეგი!</p><p class="banner-sub">გააგრძელეთ ამ ტემპით.</p></div>', unsafe_allow_html=True)
        elif score >= 60:
            st.markdown('<div class="banner banner-yellow"><p class="banner-title">👍 კარგი შედეგი!</p><p class="banner-sub">კიდევ ცოტა ვარჯიში და შესანიშნავი იქნება.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="banner banner-red"><p class="banner-title">📚 კიდევ ვარჯიში გჭირდებათ</p><p class="banner-sub">შეცდომების გადახედვა დაგეხმარება.</p></div>', unsafe_allow_html=True)

        if st.session_state.wrong_indices:
            wrong_nums = [str(quiz_data[i].get("id", i+1)) for i in st.session_state.wrong_indices]
            st.markdown(f'<div class="banner banner-red"><p class="banner-title">❌ შეცდომები ({len(wrong_nums)} კითხვა)</p><p class="banner-sub">ბაზის ნომრები: {", ".join(wrong_nums)}</p></div>', unsafe_allow_html=True)

            if st.button("🔁  შეცდომების ხელახლა გავლა", type="primary", use_container_width=True):
                wrong_list = list(st.session_state.wrong_indices)
                st.session_state.review_mode           = True
                st.session_state.review_round          = 1
                st.session_state.active_indices        = wrong_list
                st.session_state.shuffle_on            = False
                st.session_state.review_wrong_indices  = []
                st.session_state.option_order_map      = {}
                st.session_state.current_idx           = 0
                st.session_state.has_responded         = False
                st.session_state.user_choice           = None
                st.rerun()
        else:
            st.markdown('<div class="banner banner-green"><p class="banner-title">🎉 ყველა კითხვა სწორად!</p></div>', unsafe_allow_html=True)

        st.write("")

    else:
        round_num = st.session_state.review_round
        new_wrong = st.session_state.review_wrong_indices

        if not new_wrong:
            st.balloons()
            st.markdown(
                f'<div class="banner banner-green">'
                f'<p class="banner-title">🎉 ყველა შეცდომა გასწორდა!</p>'
                f'<p class="banner-sub">გადახედვის {round_num} ტური დასჭირდა.</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            wrong_nums = [str(quiz_data[i].get("id", i+1)) for i in new_wrong]
            st.markdown(
                f'<div class="banner banner-yellow">'
                f'<p class="banner-title">გადახედვის #{round_num} ტური დასრულდა</p>'
                f'<p class="banner-sub">კიდევ {len(new_wrong)} კითხვა შეცდომით: {", ".join(wrong_nums)}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            if st.button(f"🔁  კიდევ ერთი ტური  ({len(new_wrong)} კითხვა)", type="primary", use_container_width=True):
                wrong_list = list(new_wrong)
                st.session_state.review_round         += 1
                st.session_state.active_indices        = wrong_list
                st.session_state.shuffle_on            = False
                st.session_state.review_wrong_indices  = []
                st.session_state.option_order_map      = {}
                st.session_state.current_idx           = 0
                st.session_state.has_responded         = False
                st.session_state.user_choice           = None
                st.rerun()

    if st.button("🔄  თავიდან დაწყება", use_container_width=True):
        st.session_state.clear()
        st.rerun()