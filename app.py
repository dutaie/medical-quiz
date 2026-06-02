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

    div[data-testid="stAlert"][kind="info"],
    div[data-baseweb="notification"] {
        background: #eef4ff !important;
        border: none !important;
        border-left: 4px solid #2a6bcd !important;
        border-radius: 14px !important;
        padding: 18px 20px !important;
    }
    .stAlert p, .stAlert span, .stAlert li, .stAlert div {
        font-size: 18px !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
        color: #1a2845 !important;
        font-family: 'Noto Sans Georgian', sans-serif !important;
    }
    
    .stAlert ol, .stAlert ul {
        margin-top: 8px !important;
        margin-bottom: 8px !important;
        padding-left: 24px !important;
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

    div.stButton > button[kind="secondary"] div[data-testid="stMarkdownContainer"] p {
        text-align: left !important;
        width: 100% !important;
        margin: 0 !important;
        font-size: 16px !important;
        line-height: 1.55 !important;
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
    div.stButton > button[kind="primary"]:hover {
        background: #1d56b0 !important;
    }

    div[data-testid="stMetric"] {
        background: #f4f7ff !important;
        border-radius: 14px !important;
        padding: 16px !important;
        border: 1px solid #dde3f0 !important;
        text-align: center !important;
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 13px !important;
        font-family: 'Noto Sans Georgian', sans-serif !important;
        color: #5a6a85 !important;
        text-align: center !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #1a2845 !important;
        text-align: center !important;
    }

    input[type="number"] {
        font-family: 'Noto Sans Georgian', sans-serif !important;
        font-size: 16px !important;
        border-radius: 10px !important;
    }

    h3 {
        font-family: 'Noto Sans Georgian', sans-serif !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #1a2845 !important;
        margin-bottom: 4px !important;
    }

    .error-block {
        background: #fff2f2;
        border-left: 4px solid #e53935;
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 16px;
    }
    .error-block p {
        font-size: 15px;
        font-weight: 600;
        color: #991b1b;
        margin: 0;
        font-family: 'Noto Sans Georgian', sans-serif;
        line-height: 1.55;
    }

    .stat-card {
        background: #f7f9fc;
        border-radius: 14px;
        border: 1.5px solid #dde3f0;
        padding: 16px 18px;
        margin-bottom: 10px;
    }
    .stat-card-title {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        color: #8a93a6;
        margin-bottom: 10px;
        font-family: 'Noto Sans Georgian', sans-serif;
    }
    .stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0;
        border-bottom: 1px solid #eef0f5;
        font-family: 'Noto Sans Georgian', sans-serif;
    }
    .stat-row:last-child { border-bottom: none; }
    .stat-row-label { font-size: 14px; color: #3a4a65; }
    .stat-row-value { font-size: 14px; font-weight: 600; color: #1a2845; }
    .weak-q-badge {
        display: inline-block;
        background: #fff2f2;
        color: #b91c1c;
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 13px;
        font-weight: 600;
        margin: 2px 3px;
        font-family: 'Noto Sans Georgian', sans-serif;
    }

    @media (max-width: 600px) {
        .block-container { padding-left: 12px !important; padding-right: 12px !important; }
        .stAlert p, .stAlert span { font-size: 16px !important; }
        div.stButton > button[kind="secondary"] { font-size: 15px !important; padding: 12px 14px !important; }
        div.stButton > button[kind="primary"] { font-size: 15px !important; }
        .explanation-body { font-size: 15px !important; }
        div[data-testid="stMetricValue"] { font-size: 22px !important; }
    }

    @media (min-width: 601px) and (max-width: 1024px) {
        .block-container { padding-left: 24px !important; padding-right: 24px !important; }
    }
    </style>
""", unsafe_allow_html=True)


# ——— სტატისტიკის ფუნქციები (shelve-ზე დაფუძნებული) ———
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
    st.error("ვერ მოიძებნა 'questions.json' ფაილი ან ის ცარიელია!")
    st.stop()


# ——— session_state ინიციალიზაცია ———
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
    st.session_state.show_stats = False


# ——— საწყისი ეკრანი ———
if not st.session_state.quiz_started:
    total_questions = len(quiz_data)

    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a2845 0%, #2a6bcd 100%);
            border-radius: 18px;
            padding: 28px 24px;
            margin-bottom: 24px;
            text-align: center;
        ">
            <div style="font-size: 36px; margin-bottom: 10px;">🧬</div>
            <div style="font-size: 22px; font-weight: 700; color: #ffffff; font-family: 'Noto Sans Georgian', sans-serif; margin-bottom: 6px;">
                სამედიცინო ტესტები
            </div>
            <div style="font-size: 14px; color: rgba(255,255,255,0.75); font-family: 'Noto Sans Georgian', sans-serif;">
                ბაზაში სულ <strong style="color:#fff">{total}</strong> კითხვა
            </div>
        </div>
    """.replace("{total}", str(total_questions)), unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝 ტესტი", "📊 სტატისტიკა"])

    with tab1:
        st.write("### ⚙️ კითხვების დიაპაზონი")
        col1, col2 = st.columns(2)
        with col1:
            start_q = st.number_input("საიდან:", min_value=1, max_value=total_questions, value=1, step=1)
        with col2:
            end_q = st.number_input("სად მდე:", min_value=1, max_value=total_questions, value=min(20, total_questions), step=1)

        shuffle_on = st.checkbox("🔀 კითხვები და ვარიანტები შეირიოს", value=True)

        if start_q > end_q:
            st.markdown('<p style="color:#dc2626; font-weight:600; font-size:14px; margin-top:6px;">⚠️ საწყისი კითხვა საბოლოოზე მეტია!</p>', unsafe_allow_html=True)
        else:
            q_count = end_q - start_q + 1
            st.markdown(f'<p style="color:#5a6a85; font-size:14px; margin: 8px 0 16px;">შეირჩა <strong style="color:#2a6bcd">{q_count}</strong> კითხვა</p>', unsafe_allow_html=True)
            if st.button("🚀 ტესტირების დაწყება", type="primary", use_container_width=True):
                indices = list(range(start_q - 1, end_q))
                if shuffle_on:
                    random.shuffle(indices)
                st.session_state.active_indices = indices
                st.session_state.shuffle_on = shuffle_on
                st.session_state.quiz_started = True
                st.session_state.stats_saved = False
                st.rerun()

    with tab2:
        stats = load_stats()
        sessions = stats["sessions"]
        q_wrong = stats["question_wrong_counts"]

        if not sessions:
            st.markdown('<div style="text-align:center; padding: 32px 0; color:#8a93a6; font-family:\'Noto Sans Georgian\',sans-serif; font-size:15px;">🗂️ სტატისტიკა ჯერ არ გაქვთ.<br>პირველი ტესტის შემდეგ გამოჩნდება.</div>', unsafe_allow_html=True)
        else:
            all_scores = [s["score"] for s in sessions]
            all_total = sum(s["total"] for s in sessions)
            avg_score = sum(all_scores) / len(all_scores)
            best_score = max(all_scores)

            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-card-title">ზოგადი მაჩვენებლები</div>
                    <div class="stat-row"><span class="stat-row-label">სულ ტესტი ჩატარდა</span><span class="stat-row-value">{len(sessions)}</span></div>
                    <div class="stat-row"><span class="stat-row-label">სულ კითხვა გაიარა</span><span class="stat-row-value">{all_total}</span></div>
                    <div class="stat-row"><span class="stat-row-label">საშუალო შედეგი</span><span class="stat-row-value">{avg_score:.1f}%</span></div>
                    <div class="stat-row"><span class="stat-row-label">საუკეთესო შედეგი</span><span class="stat-row-value">🏆 {best_score:.1f}%</span></div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="stat-card"><div class="stat-card-title">ბოლო სესიები</div>', unsafe_allow_html=True)
            for s in reversed(sessions[-5:]):
                color = "#15803d" if s["score"] >= 80 else ("#92400e" if s["score"] >= 60 else "#b91c1c")
                st.markdown(f'<div class="stat-row"><span class="stat-row-label">{s["date"]} &nbsp;·&nbsp; {s["total"]} კითხვა</span><span class="stat-row-value" style="color:{color};">{s["score"]}%</span></div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if q_wrong:
                sorted_wrong = sorted(q_wrong.items(), key=lambda x: x[1], reverse=True)[:10]
                badges = "".join([f'<span class="weak-q-badge">#{qn} ({cnt}✗)</span>' for qn, cnt in sorted_wrong])
                st.markdown(f'<div class="stat-card"><div class="stat-card-title">ყველაზე ხშირი შეცდომები</div><div style="padding: 6px 0; line-height: 2.2;">{badges}</div></div>', unsafe_allow_html=True)

            st.write("")
            if st.button("🗑️ სტატისტიკის გასუფთავება", use_container_width=True):
                clear_stats()
                st.rerun()
    st.stop()


# ——— კითხვის ეკრანი ———
active_indices = st.session_state.active_indices
current_idx = st.session_state.current_idx

if current_idx < len(active_indices):
    real_idx = active_indices[current_idx]
    q_data = quiz_data[real_idx]

    # ——— 🛡️ უსაფრთხო ჩატვირთვის ბლოკი (Safe Load) ———
    question_text = q_data.get("question", f"⚠️ შეცდომა: კითხვის ტექსტი ცარიელია (ბაზა #{real_idx + 1})")
    options = q_data.get("options", [])
    correct_answer_raw = q_data.get("correct_answer", None)
    explanation_text = q_data.get("explanation", "განმარტება არ არის მითითებული.")

    # თუ სტრუქტურა დარღვეულია, ვაჩვენებთ შეცდომას კრაშის ნაცვლად
    if not options or correct_answer_raw is None:
        st.error(f"❌ ბაზის #{real_idx + 1} კითხვა დაზიანებულია! JSON ფაილში ამ კითხვას აკლია ვარიანტები ან სწორი პასუხი.")
        if st.button("გამოტოვება და შემდეგზე გადასვლა →", use_container_width=True):
            st.session_state.current_idx += 1
            st.session_state.has_responded = False
            st.session_state.user_choice = None
            st.rerun()
        st.stop()

    shuffle_on = st.session_state.shuffle_on
    if current_idx not in st.session_state.option_order_map:
        order = list(range(len(options)))
        if shuffle_on:
            random.shuffle(order)
        st.session_state.option_order_map[current_idx] = order
    option_order = st.session_state.option_order_map[current_idx]

    # სუფთა ინდექსაცია ერორების თავიდან ასაცილებლად
    original_correct_clean = str(correct_answer_raw).strip()
    options_clean = [str(opt).strip() for opt in options]
    
    try:
        orig_correct_idx = options_clean.index(original_correct_clean)
        shuffled_correct_idx = option_order.index(orig_correct_idx)
    except ValueError:
        orig_correct_idx = 0
        for i, opt in enumerate(options_clean):
            if original_correct_clean in opt or opt in original_correct_clean:
                orig_correct_idx = i
                break
        shuffled_correct_idx = option_order.index(orig_correct_idx) if orig_correct_idx < len(option_order) else 0

    mode_txt = f" · გადახედვა #{st.session_state.review_round}" if st.session_state.review_mode else ""

    st.markdown(f'<p style="font-size:13px; color:#8a93a6; font-family:\'Noto Sans Georgian\',sans-serif; margin-bottom:6px;">კითხვა {current_idx + 1} / {len(active_indices)}{mode_txt} &nbsp;·&nbsp; ბაზა #{real_idx + 1}</p>', unsafe_allow_html=True)
    st.progress((current_idx + 1) / len(active_indices))
    st.write("")

    st.info(question_text)
    st.write("")

    correct_idx = shuffled_correct_idx

    if st.session_state.has_responded:
        correct_child = correct_idx + 1
        chosen_child = st.session_state.user_choice + 1
        color_override = f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-child({correct_child}) button[kind="secondary"]:disabled {{
            background: #f0fdf4 !important; border-color: #22c55e !important; color: #15803d !important; font-weight: 600 !important;
        }}
        """
        if st.session_state.user_choice != correct_idx:
            color_override += f"""
            div[data-testid="stVerticalBlock"] > div:nth-child({chosen_child}) button[kind="secondary"]:disabled {{
                background: #fff2f2 !important; border-color: #ef4444 !important; color: #b91c1c !important; font-weight: 600 !important;
            }}
            """
        color_override += "</style>"
        st.markdown(color_override, unsafe_allow_html=True)

    letters = ["ა", "ბ", "გ", "დ", "ე", "ვ"]
    options_block = st.container()
    with options_block:
        for display_idx, original_idx in enumerate(option_order):
            if display_idx < len(options):
                letter = letters[display_idx] if display_idx < len(letters) else str(display_idx + 1)
                label = f"**{letter})** {options[original_idx]}"
                if st.button(label, key=f"opt_{current_idx}_{display_idx}", disabled=st.session_state.has_responded, use_container_width=True):
                    st.session_state.has_responded = True
                    st.session_state.user_choice = display_idx

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

    if st.session_state.auto_advance_flash:
        time.sleep(1.2)
        st.session_state.current_idx += 1
        st.session_state.has_responded = False
        st.session_state.user_choice = None
        st.session_state.auto_advance_flash = False
        st.rerun()

    if st.session_state.has_responded and not st.session_state.auto_advance_flash:
        st.markdown(f'<div class="explanation-wrap"><div class="explanation-label">💡 სამედიცინო განმარტება</div><div class="explanation-body">{explanation_text}</div></div>', unsafe_allow_html=True)
        st.write("")
        if st.button("შემდეგი კითხვა →", type="primary", use_container_width=True):
            st.session_state.current_idx += 1
            st.session_state.has_responded = False
            st.session_state.user_choice = None
            st.rerun()
else:
    # ——— შედეგების ეკრანი ———
    if not st.session_state.review_mode:
        total = st.session_state.correct_count + st.session_state.wrong_count
        score = (st.session_state.correct_count / total) * 100 if total > 0 else 0

        if not st.session_state.stats_saved:
            save_session_stats(st.session_state.correct_count, st.session_state.wrong_count, total, score, st.session_state.wrong_indices)
            st.session_state.stats_saved = True

        st.balloons()
        st.write("## 📊 ტესტირების შედეგები")
        st.write("")

        col1, col2, col3 = st.columns(3)
        col1.metric("სწორი", f"✅ {st.session_state.correct_count}")
        col2.metric("შეცდომა", f"❌ {st.session_state.wrong_count}")
        col3.metric("შედეგი", f"{score:.1f}%")
        st.write("")

        if score >= 80:
            st.markdown('<div style="background:#f0fdf4; border-radius:12px; padding:14px 18px; border:1.5px solid #bbf7d0; margin-bottom:16px;"><p style="color:#15803d; font-weight:600; font-size:16px; margin:0;">🎉 შესანიშნავი შედეგი!</p></div>', unsafe_allow_html=True)
        elif score >= 60:
            st.markdown('<div style="background:#fffbeb; border-radius:12px; padding:14px 18px; border:1.5px solid #fde68a; margin-bottom:16px;"><p style="color:#92400e; font-weight:600; font-size:16px; margin:0;">👍 კარგი შედეგი, გააგრძელეთ!</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background:#fff2f2; border-radius:12px; padding:14px 18px; border:1.5px solid #fecaca; margin-bottom:16px;"><p style="color:#991b1b; font-weight:600; font-size:16px; margin:0;">📚 კიდევ ვარჯიში გჭირდებათ!</p></div>', unsafe_allow_html=True)

        if st.session_state.wrong_indices:
            wrong_nums = [str(i + 1) for i in st.session_state.wrong_indices]
            st.markdown(f'<div class="error-block"><p>❌ შეცდომები (ბაზის ნომრები): {", ".join(wrong_nums)}</p></div>', unsafe_allow_html=True)

            if st.button("❌ შეცდომების ხელახლა გავლა", type="primary", use_container_width=True):
                wrong_list = list(st.session_state.wrong_indices)
                if st.session_state.get("shuffle_on", True):
                    random.shuffle(wrong_list)
                st.session_state.review_mode = True
                st.session_state.review_round = 1
                st.session_state.active_indices = wrong_list
                st.session_state.review_wrong_indices = []
                st.session_state.option_order_map = {}
                st.session_state.current_idx = 0
                st.session_state.has_responded = False
                st.session_state.user_choice = None
                st.rerun()
        else:
            st.markdown('<div style="background:#f0fdf4; border-radius:12px; padding:14px 18px; border:1.5px solid #bbf7d0; margin-bottom:16px;"><p style="color:#15803d; font-weight:600; font-size:16px; margin:0;">🎉 ყველა კითხვა სწორად გიპასუხიათ!</p></div>', unsafe_allow_html=True)
        st.write("")
    else:
        round_num = st.session_state.review_round
        new_wrong = st.session_state.review_wrong_indices

        if not new_wrong:
            st.balloons()
            st.markdown(f'<div style="background:#f0fdf4; border-radius:14px; padding:20px 22px; border:1.5px solid #bbf7d0; margin-bottom:20px;"><p style="color:#15803d; font-weight:700; font-size:18px; margin:0 0 6px;">🎉 ყველა შეცდომა გასწორდა!</p><p style="color:#166534; font-size:14px; margin:0;">გადახედვის {round_num} ტური დასჭირდა.</p></div>', unsafe_allow_html=True)
        else:
            wrong_nums = [str(i + 1) for i in new_wrong]
            st.markdown(f'<div style="background:#fffbeb; border-radius:14px; padding:18px 20px; border:1.5px solid #fde68a; margin-bottom:16px;"><p style="color:#92400e; font-weight:700; font-size:17px; margin:0 0 6px;">გადახედვის #{round_num} ტური დასრულდა</p><p style="color:#78350f; font-size:14px; margin:0;">კიდევ {len(new_wrong)} კითხვა შეცდომით: {", ".join(wrong_nums)}</p></div>', unsafe_allow_html=True)

            if st.button(f"🔁 კიდევ ერთი ტური ({len(new_wrong)} კითხვა)", type="primary", use_container_width=True):
                wrong_list = list(new_wrong)
                if st.session_state.get("shuffle_on", True):
                    random.shuffle(wrong_list)
                st.session_state.review_round += 1
                st.session_state.active_indices = wrong_list
                st.session_state.review_wrong_indices = []
                st.session_state.option_order_map = {}
                st.session_state.current_idx = 0
                st.session_state.has_responded = False
                st.session_state.user_choice = None
                st.rerun()

    if st.button("🔄 თავიდან დაწყება", use_container_width=True):
        st.session_state.clear()
        st.rerun()