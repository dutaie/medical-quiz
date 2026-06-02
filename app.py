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
        padding-top: 1.25rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 680px !important;
    }

    div[data-testid="stAlert"][kind="info"] * {
        color: #000000 !important;
        font-weight: 500 !important;
        font-size: 18px !important;
        line-height: 1.6 !important;
    }
    div[data-testid="stAlert"][kind="info"] {
        background: #eef4ff !important;
        border: none !important;
        border-left: 4px solid #2a6bcd !important;
        border-radius: 14px !important;
        padding: 18px 20px !important;
    }

    header[data-testid="stHeader"] {
        height: 0 !important;
        background: transparent !important;
    }

    .stProgress > div > div {
        height: 6px !important;
        border-radius: 99px !important;
    }
    .stProgress > div > div > div {
        background: #2a6bcd !important;
        border-radius: 99px !important;
    }
    .stProgress > div > div {
        background: #e8edf5 !important;
    }

    div.stButton > button[kind="secondary"] {
        font-family: 'Noto Sans Georgian', sans-serif !important;
        font-size: 16px !important;
        font-weight: 400 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        align-items: flex-start !important;
        display: flex !important;
        width: 100% !important;
        min-height: 52px !important;
        padding: 13px 18px !important;
        background: #ffffff !important;
        color: #1e2d40 !important;
        border: 1.5px solid #d5dbe8 !important;
        border-radius: 12px !important;
        white-space: normal !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
        transition: border-color 0.15s, background 0.15s !important;
    }

    div.stButton > button[kind="secondary"]:hover {
        background: #f4f7ff !important;
        border-color: #2a6bcd !important;
        color: #0f1e35 !important;
    }

    div.stButton > button[kind="secondary"]:disabled {
        background: #f9fafb !important;
        border-color: #e0e4ed !important;
        color: #8a93a6 !important;
        opacity: 1 !important;
    }

    .explanation-wrap {
        background: #f7f9fc;
        border-radius: 14px;
        border: 1.5px solid #dde3f0;
        padding: 18px 20px;
        margin-top: 4px;
    }
    .explanation-label {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: #2a6bcd;
        margin-bottom: 8px;
        font-family: 'Noto Sans Georgian', sans-serif;
    }
    .explanation-body {
        font-size: 16px;
        line-height: 1.65;
        color: #1e2d40;
        font-family: 'Noto Sans Georgian', sans-serif;
    }

    div.stButton > button[kind="primary"] {
        font-family: 'Noto Sans Georgian', sans-serif !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 14px 24px !important;
        border-radius: 12px !important;
        background: #2a6bcd !important;
        color: #ffffff !important;
        border: none !important;
        width: 100% !important;
        letter-spacing: 0.01em !important;
        box-shadow: 0 2px 8px rgba(42,107,205,0.25) !important;
        transition: background 0.15s !important;
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

def save_session_stats(correct, wrong, total, score, wrong_indices):
    with shelve.open(STATS_FILE) as db:
        sessions = db.get("sessions", [])
        sessions.append({
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "correct": correct,
            "wrong": wrong,
            "total": total,
            "score": round(score, 1),
        })
        db["sessions"] = sessions[-20:]

        q_wrong = db.get("question_wrong_counts", {})
        for idx in wrong_indices:
            key = str(idx + 1)
            q_wrong[key] = q_wrong.get(key, 0) + 1
        db["question_wrong_counts"] = q_wrong

def clear_stats():
    with shelve.open(STATS_FILE) as db:
        db["sessions"] = []
        db["question_wrong_counts"] = {}


# ——— კითხვების ჩატვირთვა ———
@st.cache_data
def load_quiz_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "questions.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8", errors="ignore") as file:
            return json.load(file)
    return []

quiz_data = load_quiz_data()

if not quiz_data:
    st.error("ვერ მოიძებნა 'questions.json' ფაილი!")
    st.stop()


# ——— session_state ———
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
    st.session_state.current_idx = 0
    st.session_state.correct_count = 0
    st.session_state.wrong_count = 0
    st.session_state.wrong_indices = []
    st.session_state.review_mode = False
    st.session_state.review_round = 0
    st.session_state.active_indices = []
    st.session_state.has_responded = False
    st.session_state.user_choice = None
    st.session_state.auto_advance_flash = False
    st.session_state.review_wrong_indices = []
    st.session_state.option_order_map = {}
    st.session_state.stats_saved = False


# ——— საწყისი ეკრანი ———
if not st.session_state.quiz_started:
    total_questions = len(quiz_data)
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a2845 0%, #2a6bcd 100%); border-radius: 18px; padding: 28px 24px; margin-bottom: 24px; text-align: center;">
            <div style="font-size: 36px; margin-bottom: 10px;">🧬</div>
            <div style="font-size: 22px; font-weight: 700; color: #ffffff; font-family: 'Noto Sans Georgian', sans-serif; margin-bottom: 6px;">სამედიცინო ტესტები</div>
            <div style="font-size: 14px; color: rgba(255,255,255,0.75); font-family: 'Noto Sans Georgian', sans-serif;">ბაზაში სულ {total_questions} კითხვა</div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝 ტესტი", "📊 სტატისტიკა"])
    with tab1:
        start_q = st.number_input("საიდან:", min_value=1, max_value=total_questions, value=1, step=1)
        end_q = st.number_input("სად მდე:", min_value=1, max_value=total_questions, value=min(20, total_questions), step=1)
        shuffle_on = st.checkbox("🔀 კითხვები და ვარიანტები შეირიოს", value=True)
        if st.button("🚀 ტესტირების დაწყება", type="primary", use_container_width=True):
            indices = list(range(start_q - 1, end_q))
            if shuffle_on: random.shuffle(indices)
            st.session_state.active_indices = indices
            st.session_state.shuffle_on = shuffle_on
            st.session_state.quiz_started = True
            st.rerun()

    with tab2:
        stats = load_stats()
        if not stats["sessions"]:
            st.write("სტატისტიკა ჯერ არ არის.")
        else:
            st.write(f"სულ ჩატარდა: {len(stats['sessions'])} ტესტი")
            if st.button("🗑️ გაწმენდა"):
                clear_stats()
                st.rerun()
    st.stop()


# ——— კითხვის ეკრანი ———
active_indices = st.session_state.active_indices
current_idx = st.session_state.current_idx

if current_idx < len(active_indices):
    real_idx = active_indices[current_idx]
    q_data = quiz_data[real_idx]
    question_text = q_data.get("question", "...")
    options = q_data.get("options", [])
    correct_answer_raw = q_data.get("correct_answer", None)
    explanation_text = q_data.get("explanation", "განმარტება არ არის.")

    # პროგრეს ბარი
    st.progress((current_idx + 1) / len(active_indices))
    st.write("")
    st.info(question_text)
    
    # ლოგიკა
    if current_idx not in st.session_state.option_order_map:
        order = list(range(len(options)))
        if st.session_state.shuffle_on: random.shuffle(order)
        st.session_state.option_order_map[current_idx] = order
    option_order = st.session_state.option_order_map[current_idx]

    # პასუხების შემოწმება
    correct_idx = -1
    for i, opt in enumerate(options):
        if str(opt).strip() == str(correct_answer_raw).strip():
            correct_idx = i
            break
    
    # გაშიფრული სწორი პასუხის პოზიცია
    shuffled_correct_idx = -1
    for i, orig_idx in enumerate(option_order):
        if orig_idx == correct_idx:
            shuffled_correct_idx = i
            break

    # ღილაკები
    for display_idx, original_idx in enumerate(option_order):
        if st.button(options[original_idx], key=f"btn_{display_idx}", disabled=st.session_state.has_responded, use_container_width=True):
            st.session_state.has_responded = True
            st.session_state.user_choice = display_idx
            
            if display_idx == shuffled_correct_idx:
                if not st.session_state.review_mode: st.session_state.correct_count += 1
            else:
                if not st.session_state.review_mode: st.session_state.wrong_count += 1
                if real_idx not in st.session_state.wrong_indices: st.session_state.wrong_indices.append(real_idx)
            st.rerun()

    # შემდეგი ნაბიჯი
    if st.session_state.has_responded:
        st.markdown(f'<div class="explanation-wrap"><div class="explanation-label">💡 განმარტება</div><div class="explanation-body">{explanation_text}</div></div>', unsafe_allow_html=True)
        if st.button("შემდეგი →", type="primary", use_container_width=True):
            st.session_state.current_idx += 1
            st.session_state.has_responded = False
            st.session_state.user_choice = None
            st.rerun()
else:
    # შედეგები
    total = st.session_state.correct_count + st.session_state.wrong_count
    score = (st.session_state.correct_count / total) * 100 if total > 0 else 0
    if not st.session_state.stats_saved:
        save_session_stats(st.session_state.correct_count, st.session_state.wrong_count, total, score, st.session_state.wrong_indices)
        st.session_state.stats_saved = True
    
    st.write(f"## შედეგი: {score:.1f}%")
    if st.button("🔄 თავიდან"):
        st.session_state.clear()
        st.rerun()