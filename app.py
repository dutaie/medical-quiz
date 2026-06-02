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

    html, body, [class*="css"] { font-family: 'Noto Sans Georgian', sans-serif !important; }
    .block-container { padding-top: 1.25rem !important; padding-bottom: 1.5rem !important; max-width: 680px !important; }

    /* კითხვის წაკითხვადობა */
    div[data-testid="stAlert"][kind="info"] * { color: #000000 !important; font-weight: 500 !important; font-size: 18px !important; line-height: 1.6 !important; }
    div[data-testid="stAlert"][kind="info"] { background: #eef4ff !important; border: none !important; border-left: 4px solid #2a6bcd !important; border-radius: 14px !important; padding: 18px 20px !important; }

    header[data-testid="stHeader"] { height: 0 !important; background: transparent !important; }

    div.stButton > button[kind="secondary"] {
        font-family: 'Noto Sans Georgian', sans-serif !important;
        font-size: 16px !important;
        width: 100% !important;
        min-height: 52px !important;
        padding: 13px 18px !important;
        background: #ffffff !important;
        color: #1e2d40 !important;
        border: 1.5px solid #d5dbe8 !important;
        border-radius: 12px !important;
    }
    
    .explanation-wrap { background: #f7f9fc; border-radius: 14px; border: 1.5px solid #dde3f0; padding: 18px 20px; margin-top: 4px; }
    .explanation-label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: #2a6bcd; margin-bottom: 8px; }
    .explanation-body { font-size: 16px; line-height: 1.65; color: #1e2d40; }
    </style>
""", unsafe_allow_html=True)


# ——— სტატისტიკის ფუნქციები ———
STATS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz_stats")

def load_stats():
    with shelve.open(STATS_FILE) as db:
        return {"sessions": db.get("sessions", []), "question_wrong_counts": db.get("question_wrong_counts", {})}

def save_session_stats(correct, wrong, total, score, wrong_indices):
    with shelve.open(STATS_FILE) as db:
        sessions = db.get("sessions", [])
        sessions.append({"date": datetime.now().strftime("%d/%m/%Y %H:%M"), "correct": correct, "wrong": wrong, "total": total, "score": round(score, 1)})
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
        with open(json_path, "r", encoding="utf-8", errors="ignore") as file: return json.load(file)
    return []

quiz_data = load_quiz_data()

# ——— session_state ———
if "quiz_started" not in st.session_state:
    st.session_state.update({
        "quiz_started": False, "current_idx": 0, "correct_count": 0, "wrong_count": 0,
        "wrong_indices": [], "has_responded": False, "user_choice": None, "option_order_map": {}, "auto_advance_flash": False
    })

# ——— საწყისი ეკრანი ———
if not st.session_state.quiz_started:
    st.markdown("""<div style="text-align: center; padding: 20px;"><h2>🧬 სამედიცინო ტესტები</h2></div>""", unsafe_allow_html=True)
    if st.button("🚀 ტესტირების დაწყება", type="primary", use_container_width=True):
        st.session_state.active_indices = list(range(len(quiz_data)))
        random.shuffle(st.session_state.active_indices)
        st.session_state.quiz_started = True
        st.rerun()
    st.stop()

# ——— კითხვის ეკრანი ———
active_indices = st.session_state.active_indices
current_idx = st.session_state.current_idx

if current_idx < len(active_indices):
    real_idx = active_indices[current_idx]
    q_data = quiz_data[real_idx]
    options = q_data.get("options", [])
    
    # 1. ნომრის გამოჩენა
    st.markdown(f'<p style="font-size:13px; color:#8a93a6;">კითხვა {current_idx + 1} / {len(active_indices)} &nbsp;·&nbsp; ბაზა #{real_idx + 1}</p>', unsafe_allow_html=True)
    st.info(q_data["question"])

    # ლოგიკა დაფლეთილი პასუხებისთვის
    if current_idx not in st.session_state.option_order_map:
        order = list(range(len(options)))
        random.shuffle(order)
        st.session_state.option_order_map[current_idx] = order
    
    order = st.session_state.option_order_map[current_idx]
    correct_idx = -1
    for i, opt in enumerate(options):
        if str(opt).strip() == str(q_data["correct_answer"]).strip():
            correct_idx = i
            break
            
    # პასუხის ფერის ლოგიკა
    if st.session_state.has_responded:
        correct_pos = order.index(correct_idx) + 1
        chosen_pos = st.session_state.user_choice + 1
        color_css = f"""<style>
            div[data-testid="stVerticalBlock"] > div:nth-child({correct_pos}) button {{ background: #dcfce7 !important; border-color: #22c55e !important; }}
        """
        if st.session_state.user_choice != order.index(correct_idx):
            color_css += f'div[data-testid="stVerticalBlock"] > div:nth-child({chosen_pos}) button {{ background: #fee2e2 !important; border-color: #ef4444 !important; }}'
        st.markdown(color_css + "</style>", unsafe_allow_html=True)

    # ღილაკები
    for i, orig_idx in enumerate(order):
        if st.button(options[orig_idx], key=f"btn_{i}", disabled=st.session_state.has_responded, use_container_width=True):
            st.session_state.has_responded = True
            st.session_state.user_choice = i
            if i == order.index(correct_idx): st.session_state.correct_count += 1
            else: 
                st.session_state.wrong_count += 1
                st.session_state.wrong_indices.append(real_idx)
            st.rerun()

    if st.session_state.has_responded:
        st.markdown(f'<div class="explanation-wrap"><div class="explanation-label">💡 განმარტება</div><div class="explanation-body">{q_data.get("explanation", "...")}</div></div>', unsafe_allow_html=True)
        if st.button("შემდეგი კითხვა →", type="primary", use_container_width=True):
            st.session_state.current_idx += 1
            st.session_state.has_responded = False
            st.rerun()
else:
    st.write(f"## ტესტი დასრულდა! შედეგი: {st.session_state.correct_count}/{len(active_indices)}")
    if st.button("🔄 თავიდან"):
        st.session_state.clear()
        st.rerun()