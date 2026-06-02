import streamlit as st
import json
import os
import time

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
    .stAlert p, .stAlert span {
        font-size: 18px !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
        color: #1a2845 !important;
        font-family: 'Noto Sans Georgian', sans-serif !important;
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

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
    st.session_state.current_idx = 0
    st.session_state.correct_count = 0
    st.session_state.wrong_count = 0
    st.session_state.wrong_indices = []       # ამ run-ის შეცდომები
    st.session_state.review_mode = False
    st.session_state.review_round = 0         # რომელ ტური გადახედვაშია
    st.session_state.active_indices = []
    st.session_state.has_responded = False
    st.session_state.user_choice = None
    st.session_state.auto_advance_flash = False
    # review-ის დროს ახალი შეცდომები ცალკე ინახება
    st.session_state.review_wrong_indices = []

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

    st.write("### ⚙️ კითხვების დიაპაზონი")

    col1, col2 = st.columns(2)
    with col1:
        start_q = st.number_input("საიდან:", min_value=1, max_value=total_questions, value=1, step=1)
    with col2:
        end_q = st.number_input("სად მდე:", min_value=1, max_value=total_questions, value=min(20, total_questions), step=1)

    if start_q > end_q:
        st.markdown(
            '<p style="color:#dc2626; font-weight:600; font-size:14px; margin-top:6px;">'
            '⚠️ საწყისი კითხვა საბოლოოზე მეტია!</p>',
            unsafe_allow_html=True
        )
    else:
        q_count = end_q - start_q + 1
        st.markdown(
            f'<p style="color:#5a6a85; font-size:14px; margin: 8px 0 16px; font-family:\'Noto Sans Georgian\',sans-serif;">'
            f'შეირჩა <strong style="color:#2a6bcd">{q_count}</strong> კითხვა</p>',
            unsafe_allow_html=True
        )
        if st.button("🚀 ტესტირების დაწყება", type="primary", use_container_width=True):
            st.session_state.active_indices = list(range(start_q - 1, end_q))
            st.session_state.quiz_started = True
            st.rerun()
    st.stop()


active_indices = st.session_state.active_indices
current_idx = st.session_state.current_idx

# ——— კითხვის ეკრანი ———
if current_idx < len(active_indices):
    real_idx = active_indices[current_idx]
    q_data = quiz_data[real_idx]

    if st.session_state.review_mode:
        round_num = st.session_state.review_round
        mode_txt = f" · გადახედვა #{round_num}"
    else:
        mode_txt = ""

    st.markdown(
        f'<p style="font-size:13px; color:#8a93a6; font-family:\'Noto Sans Georgian\',sans-serif; margin-bottom:6px;">'
        f'კითხვა {current_idx + 1} / {len(active_indices)}{mode_txt} &nbsp;·&nbsp; ბაზა #{real_idx + 1}</p>',
        unsafe_allow_html=True
    )
    st.progress((current_idx + 1) / len(active_indices))
    st.write("")

    st.info(q_data["question"])
    st.write("")

    options = q_data["options"]
    correct_idx = q_data["correct"]

    # ფერების ოვერრაიდი პასუხის შემდეგ
    if st.session_state.has_responded:
        correct_child = correct_idx + 1
        chosen_child = st.session_state.user_choice + 1

        color_override = f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-child({correct_child}) button[kind="secondary"]:disabled {{
            background: #f0fdf4 !important;
            border-color: #22c55e !important;
            color: #15803d !important;
            font-weight: 600 !important;
        }}
        """
        if st.session_state.user_choice != correct_idx:
            color_override += f"""
            div[data-testid="stVerticalBlock"] > div:nth-child({chosen_child}) button[kind="secondary"]:disabled {{
                background: #fff2f2 !important;
                border-color: #ef4444 !important;
                color: #b91c1c !important;
                font-weight: 600 !important;
            }}
            """
        color_override += "</style>"
        st.markdown(color_override, unsafe_allow_html=True)

    # ——— სწორ პასუხზე: გამწვანებული ველი ჩანს 1.2 წამი, შემდეგ გადადის ———
    if st.session_state.auto_advance_flash:
        time.sleep(1.2)
        st.session_state.current_idx += 1
        st.session_state.has_responded = False
        st.session_state.user_choice = None
        st.session_state.auto_advance_flash = False
        st.rerun()

    options_block = st.container()
    with options_block:
        letters = ["ა", "ბ", "გ", "დ", "ე", "ვ"]
        for idx, option in enumerate(options):
            letter = letters[idx] if idx < len(letters) else str(idx + 1)
            label = f"**{letter})**  {option}"
            if st.button(label, key=f"opt_{current_idx}_{idx}",
                         disabled=st.session_state.has_responded,
                         use_container_width=True):
                st.session_state.has_responded = True
                st.session_state.user_choice = idx

                if idx == correct_idx:
                    # სწორი — მხოლოდ პირვანდელ ტესტზე ვთვლით ქულებს
                    if not st.session_state.review_mode:
                        st.session_state.correct_count += 1
                    st.session_state.auto_advance_flash = True
                else:
                    # შეცდომა — ვიმახსოვრებთ სად
                    if not st.session_state.review_mode:
                        st.session_state.wrong_count += 1
                        if real_idx not in st.session_state.wrong_indices:
                            st.session_state.wrong_indices.append(real_idx)
                    else:
                        # review-ის დროს ახალ შეცდომებს ვაგროვებთ ცალკე
                        if real_idx not in st.session_state.review_wrong_indices:
                            st.session_state.review_wrong_indices.append(real_idx)
                st.rerun()

    # განმარტება — ჩანს მხოლოდ შეცდომაზე (სწორზე ელოდება auto_advance)
    if st.session_state.has_responded and not st.session_state.auto_advance_flash:
        st.markdown(f"""
            <div class="explanation-wrap">
                <div class="explanation-label">💡 სამედიცინო განმარტება</div>
                <div class="explanation-body">{q_data["explanation"]}</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("")

        if st.button("შემდეგი კითხვა →", type="primary", use_container_width=True):
            st.session_state.current_idx += 1
            st.session_state.has_responded = False
            st.session_state.user_choice = None
            st.rerun()

else:
    # ——— შედეგების / გადახედვის ეკრანი ———

    if not st.session_state.review_mode:
        # პირვანდელი ტესტის შედეგი
        st.balloons()
        st.write("## 📊 ტესტირების შედეგები")
        st.write("")

        total = st.session_state.correct_count + st.session_state.wrong_count
        score = (st.session_state.correct_count / total) * 100 if total > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("სწორი", f"✅ {st.session_state.correct_count}")
        col2.metric("შეცდომა", f"❌ {st.session_state.wrong_count}")
        col3.metric("შედეგი", f"{score:.1f}%")
        st.write("")

        if score >= 80:
            st.markdown(
                '<div style="background:#f0fdf4; border-radius:12px; padding:14px 18px; border:1.5px solid #bbf7d0; margin-bottom:16px;">'
                '<p style="color:#15803d; font-weight:600; font-size:16px; margin:0; font-family:\'Noto Sans Georgian\',sans-serif;">🎉 შესანიშნავი შედეგი!</p></div>',
                unsafe_allow_html=True
            )
        elif score >= 60:
            st.markdown(
                '<div style="background:#fffbeb; border-radius:12px; padding:14px 18px; border:1.5px solid #fde68a; margin-bottom:16px;">'
                '<p style="color:#92400e; font-weight:600; font-size:16px; margin:0; font-family:\'Noto Sans Georgian\',sans-serif;">👍 კარგი შედეგი, გააგრძელეთ!</p></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="background:#fff2f2; border-radius:12px; padding:14px 18px; border:1.5px solid #fecaca; margin-bottom:16px;">'
                '<p style="color:#991b1b; font-weight:600; font-size:16px; margin:0; font-family:\'Noto Sans Georgian\',sans-serif;">📚 კიდევ ვარჯიში გჭირდებათ!</p></div>',
                unsafe_allow_html=True
            )

        if st.session_state.wrong_indices:
            wrong_nums = [str(i + 1) for i in st.session_state.wrong_indices]
            st.markdown(f"""
                <div class="error-block">
                    <p>❌ შეცდომები (ბაზის ნომრები): {', '.join(wrong_nums)}</p>
                </div>
            """, unsafe_allow_html=True)

            if st.button("❌ შეცდომების ხელახლა გავლა", type="primary", use_container_width=True):
                st.session_state.review_mode = True
                st.session_state.review_round = 1
                st.session_state.active_indices = list(st.session_state.wrong_indices)
                st.session_state.review_wrong_indices = []
                st.session_state.current_idx = 0
                st.session_state.has_responded = False
                st.session_state.user_choice = None
                st.rerun()
        else:
            st.markdown(
                '<div style="background:#f0fdf4; border-radius:12px; padding:14px 18px; border:1.5px solid #bbf7d0; margin-bottom:16px;">'
                '<p style="color:#15803d; font-weight:600; font-size:16px; margin:0; font-family:\'Noto Sans Georgian\',sans-serif;">🎉 ყველა კითხვა სწორად გიპასუხიათ!</p></div>',
                unsafe_allow_html=True
            )

        st.write("")

    else:
        # ——— გადახედვის ტური დასრულდა ———
        round_num = st.session_state.review_round
        new_wrong = st.session_state.review_wrong_indices

        if not new_wrong:
            # ყველა სწორად გაიარა — დასრულება
            st.balloons()
            st.markdown(
                f'<div style="background:#f0fdf4; border-radius:14px; padding:20px 22px; border:1.5px solid #bbf7d0; margin-bottom:20px;">'
                f'<p style="color:#15803d; font-weight:700; font-size:18px; margin:0 0 6px; font-family:\'Noto Sans Georgian\',sans-serif;">🎉 ყველა შეცდომა გასწორდა!</p>'
                f'<p style="color:#166534; font-size:14px; margin:0; font-family:\'Noto Sans Georgian\',sans-serif;">'
                f'გადახედვის {round_num} ტური დასჭირდა.</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            # კიდევ არის შეცდომები — შემოთავაზება ახლის გავლაზე
            wrong_nums = [str(i + 1) for i in new_wrong]
            st.markdown(
                f'<div style="background:#fffbeb; border-radius:14px; padding:18px 20px; border:1.5px solid #fde68a; margin-bottom:16px;">'
                f'<p style="color:#92400e; font-weight:700; font-size:17px; margin:0 0 6px; font-family:\'Noto Sans Georgian\',sans-serif;">'
                f'გადახედვის #{round_num} ტური დასრულდა</p>'
                f'<p style="color:#78350f; font-size:14px; margin:0; font-family:\'Noto Sans Georgian\',sans-serif;">'
                f'კიდევ {len(new_wrong)} კითხვა შეცდომით: {", ".join(wrong_nums)}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

            if st.button(f"🔁 კიდევ ერთი ტური ({len(new_wrong)} კითხვა)", type="primary", use_container_width=True):
                st.session_state.review_round += 1
                st.session_state.active_indices = list(new_wrong)
                st.session_state.review_wrong_indices = []
                st.session_state.current_idx = 0
                st.session_state.has_responded = False
                st.session_state.user_choice = None
                st.rerun()

    if st.button("🔄 თავიდან დაწყება", use_container_width=True):
        st.session_state.clear()
        st.rerun()