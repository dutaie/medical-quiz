import streamlit as st
import json
import os
import time

# 1. გვერდის ბაზისური კონფიგურაცია
st.set_page_config(page_title="სამედიცინო ტესტები", page_icon="🧬", layout="centered")

# 2. სუფთა და მკაცრი CSS სტილები (მარცხნივ გასწორება, ზედა მარჟინების მოკვლა და მაღალი კითხვითობა)
st.markdown("""
    <style>
    /* აპლიკაციის ზედა ცარიელი სივრცის (Padding) მინიმიზაცია */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0rem !important;
    }
    
    /* ჰედერის (ზედა თეთრი ზოლის) სიმაღლის განულება */
    header[data-testid="stHeader"] {
        height: 0px !important;
        background: transparent !important;
    }

    /* კითხვის დიდი ბარათი */
    .stAlert p {
        font-size: 21px !important;
        font-weight: 600 !important;
        line-height: 1.6 !important;
        color: #1e293b !important;
    }
    
    /* პასუხების ღილაკების საწყისი დიზაინი - მკაცრად მარცხნიდან! */
    div.stButton > button[kind="secondary"] {
        font-size: 18px !important;
        text-align: left !important;
        justify-content: flex-start !important;
        align-items: center !important;
        display: flex !important;
        width: 100% !important;
        padding: 16px 22px !important;
        background-color: #ffffff !important;
        color: #334155 !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        white-space: normal !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02) !important;
    }
    
    /* იძულებითი მარცხნივ გასწორება შიდა ტექსტებისთვის */
    div.stButton > button[kind="secondary"] div[data-testid="stMarkdownContainer"] p {
        text-align: left !important;
        justify-content: flex-start !important;
        width: 100% !important;
        margin: 0 !important;
    }
    
    /* მაუსის მიტანის ეფექტი */
    div.stButton > button[kind="secondary"]:hover {
        background-color: #f8fafc !important;
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
    }

    /* გათიშული ღილაკების მყარი ვიზუალი (სტრიმლიტს ვუკრძალავთ გათეთრებას) */
    div.stButton > button[kind="secondary"]:disabled {
        background-color: #f8fafc !important;
        border-color: #e2e8f0 !important;
        color: #94a3b8 !important;
        opacity: 1 !important;
    }
    
    /* ახალი, სუფთა და მაღალკონტრასტული განმარტების ბლოკი */
    .custom-explanation {
        background-color: #f8fafc !important;
        border-left: 6px solid #2563eb !important;
        padding: 20px !important;
        border-radius: 8px !important;
        margin-top: 20px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    
    .custom-explanation-title {
        font-size: 19px !important;
        font-weight: 700 !important;
        color: #1e3a8a !important;
        margin-bottom: 8px !important;
    }
    
    .custom-explanation-text {
        font-size: 18px !important;
        line-height: 1.6 !important;
        color: #1e293b !important;
    }
    
    /* ქვედა "შემდეგი" და "დაწყების" ღილაკები */
    div.stButton > button[kind="primary"] {
        font-size: 18px !important;
        padding: 14px 28px !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. JSON მონაცემების ჩატვირთვა
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

# 4. სესიის ცვლადების მართვა
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
    st.session_state.current_idx = 0
    st.session_state.correct_count = 0
    st.session_state.wrong_count = 0
    st.session_state.wrong_indices = []
    st.session_state.review_mode = False
    st.session_state.active_indices = []
    st.session_state.has_responded = False
    st.session_state.user_choice = None
    st.session_state.auto_advance_flash = False

# 4.5 საწყისი დიაპაზონის ასარჩევი მენიუ
if not st.session_state.quiz_started:
    total_questions = len(quiz_data)
    st.write("### ⚙️ აირჩიეთ კითხვების დიაპაზონი")
    st.write(f"ბაზაში სულ მოიძებნა **{total_questions}** კითხვა.")
    
    col1, col2 = st.columns(2)
    with col1:
        start_q = st.number_input("რომელი კითხვიდან:", min_value=1, max_value=total_questions, value=1, step=1)
    with col2:
        end_q = st.number_input("რომელ კითხვამდე:", min_value=1, max_value=total_questions, value=min(20, total_questions), step=1)
        
    if start_q > end_q:
        st.markdown('<p style="color: #ef4444; font-weight: 600;">⚠️ საწყისი კითხვა არ უნდა იყოს საბოლოოზე მეტი!</p>', unsafe_allow_html=True)
    else:
        st.write("")
        if st.button("🚀 ტესტირების დაწყება", type="primary", use_container_width=True):
            # მომხმარებლის 1-ზე დაფუძნებული ინდექსები გადაგვყავს პითონის 0-ზე დაფუძნებულ ინდექსებში
            st.session_state.active_indices = list(range(start_q - 1, end_q))
            st.session_state.quiz_started = True
            st.rerun()
    st.stop() # აჩერებს კოდს, სანამ ღილაკს არ დააჭერენ

# მონაცემების მინიჭება დიაპაზონის მიხედვით
active_indices = st.session_state.active_indices
current_idx = st.session_state.current_idx

# 5. ტესტირების აქტიური ფაზა
if current_idx < len(active_indices):
    real_idx = active_indices[current_idx]
    q_data = quiz_data[real_idx]
    
    # პროგრესბარი (აჩვენებს მიმდინარე პროგრესს არჩეულ დიაპაზონში)
    mode_txt = " (შეცდომების გადახედვა)" if st.session_state.review_mode else ""
    st.write(f"### კითხვა {current_idx + 1} / {len(active_indices)}{mode_txt} *(ბაზაში: #{real_idx + 1})*")
    st.progress((current_idx + 1) / len(active_indices))
    
    # კითხვის ჩვენება
    st.info(q_data["question"])
    st.write("")
    
    options = q_data["options"]
    correct_idx = q_data["correct"]
    
    # დინამიური ფერები პასუხის გაცემის შემდეგ
    if st.session_state.has_responded:
        correct_child = correct_idx + 1
        chosen_child = st.session_state.user_choice + 1
        
        color_override = f"""
        <style>
        /* სწორი ვარიანტი ყოველთვის მწვანდება */
        div[data-testid="stVerticalBlock"] > div:nth-child({correct_child}) button[kind="secondary"]:disabled {{
            background-color: #dcfce7 !important;
            border-color: #22c55e !important;
            color: #15803d !important;
            font-weight: 600 !important;
        }}
        """
        # თუ არასწორია, ის წითლდება
        if st.session_state.user_choice != correct_idx:
            color_override += f"""
            div[data-testid="stVerticalBlock"] > div:nth-child({chosen_child}) button[kind="secondary"]:disabled {{
                background-color: #fee2e2 !important;
                border-color: #ef4444 !important;
                color: #b91c1c !important;
                font-weight: 600 !important;
            }}
            """
        color_override += "</style>"
        st.markdown(color_override, unsafe_allow_html=True)

    # მყისიერი ავტომატური გადასვლა სწორ პასუხზე
    if st.session_state.auto_advance_flash:
        time.sleep(0.4) # 0.4 წამი ეფექტისთვის
        st.session_state.current_idx += 1
        st.session_state.has_responded = False
        st.session_state.user_choice = None
        st.session_state.auto_advance_flash = False
        st.rerun()

    # ვარიანტების ბლოკი
    options_block = st.container()
    with options_block:
        for idx, option in enumerate(options):
            if st.button(option, key=f"opt_{current_idx}_{idx}", disabled=st.session_state.has_responded, use_container_width=True):
                st.session_state.has_responded = True
                st.session_state.user_choice = idx
                
                if idx == correct_idx:
                    if not st.session_state.review_mode:
                        st.session_state.correct_count += 1
                    st.session_state.auto_advance_flash = True
                else:
                    if not st.session_state.review_mode:
                        st.session_state.wrong_count += 1
                        if real_idx not in st.session_state.wrong_indices:
                            st.session_state.wrong_indices.append(real_idx)
                st.rerun()

    # თუ პასუხი შეცდომაა -> გამოდის ახალი, სუფთა განმარტების ბლოკი
    if st.session_state.has_responded and not st.session_state.auto_advance_flash:
        st.markdown(f"""
            <div class="custom-explanation">
                <div class="custom-explanation-title">💡 სამედიცინო განმარტება:</div>
                <div class="custom-explanation-text">{q_data["explanation"]}</div>
            </div>
            <br>
        """, unsafe_allow_html=True)
        
        if st.button("შემდეგი კითხვა ➡️", type="primary", use_container_width=True):
            st.session_state.current_idx += 1
            st.session_state.has_responded = False
            st.session_state.user_choice = None
            st.rerun()

else:
    # შედეგების ეკრანი
    st.balloons()
    st.title("ტესტირების შედეგები 📊")
    
    if not st.session_state.review_mode:
        total = st.session_state.correct_count + st.session_state.wrong_count
        score = (st.session_state.correct_count / total) * 100 if total > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("სწორი პასუხი", f"✅ {st.session_state.correct_count}")
        col2.metric("არასწორი პასუხი", f"❌ {st.session_state.wrong_count}")
        col3.metric("საერთო შედეგი", f"{score:.1f}%")
        
        if st.session_state.wrong_indices:
            # აქაც ბაზის რეალური ნომრები რომ აჩვენოს მომხმარებელს (+1)
            wrong_nums = [str(i + 1) for i in st.session_state.wrong_indices]
            
            # მაღალკონტრასტული შეცდომების ბლოკი
            st.markdown(f"""
                <div style="background-color: #fef2f2; border-left: 6px solid #ef4444; padding: 18px; border-radius: 10px; margin-bottom: 20px;">
                    <p style="font-size: 18px; color: #991b1b; font-weight: 600; margin: 0; text-align: left;">
                        ❌ კითხვები, სადაც შეგეშალათ (ნომრები ბაზიდან): [ {', '.join(wrong_nums)} ]
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("❌ მხოლოდ შეცდომების ხელახლა გავლა", type="primary", use_container_width=True):
                st.session_state.review_mode = True
                st.session_state.active_indices = list(st.session_state.wrong_indices)
                st.session_state.current_idx = 0
                st.session_state.has_responded = False
                st.session_state.user_choice = None
                st.rerun()
    else:
        st.success("🎉 თქვენ წარმატებით გადახედეთ ყველა შეცდომას!")
        
    if st.button("🔄 თავიდან დაწყება (ახალი დიაპაზონი)", use_container_width=True):
        st.session_state.clear()
        st.rerun()