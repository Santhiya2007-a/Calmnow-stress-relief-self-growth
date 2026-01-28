import streamlit as st
import pandas as pd
import os
from datetime import datetime
import random

# Page config
st.set_page_config(page_title="CalmNow", page_icon="🦋", layout="wide")

# Files
USERS_FILE = "users_data.csv"
THOUGHTS_FILE = "user_thoughts.csv"

# CSS with baby pink login and flying butterflies
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    
    .login-container {
        background: linear-gradient(135deg, #FFB6D9 0%, #FFC8DD 50%, #FFE5EC 100%);
        padding: 3rem; border-radius: 25px;
        box-shadow: 0 15px 50px rgba(255, 182, 217, 0.5);
        margin: 2rem auto; max-width: 500px;
        position: relative; overflow: hidden;
    }
    
    .butterfly {
        position: absolute; font-size: 2.5rem;
        animation: fly 15s infinite ease-in-out; opacity: 0.7;
    }
    
    .butterfly:nth-child(1) { left: 10%; animation-delay: 0s; animation-duration: 12s; }
    .butterfly:nth-child(2) { left: 50%; animation-delay: 3s; animation-duration: 15s; }
    .butterfly:nth-child(3) { left: 80%; animation-delay: 6s; animation-duration: 18s; }
    
    @keyframes fly {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 0.7; }
        50% { transform: translateY(-20vh) translateX(30px) rotate(180deg); opacity: 0.9; }
        90% { opacity: 0.7; }
        100% { transform: translateY(-120vh) rotate(360deg); opacity: 0; }
    }
    
    .login-title {
        color: #C41E3A; font-size: 3rem; font-weight: 700;
        text-align: center; margin-bottom: 0.5rem;
        text-shadow: 3px 3px 6px rgba(196, 30, 58, 0.3); z-index: 2;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 2.5rem; border-radius: 20px;
        text-align: center; margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .stress-box {
        background: linear-gradient(135deg, #FA8072 0%, #FF6347 50%, #FF4500 100%);
        padding: 3rem; border-radius: 20px; text-align: center;
        color: white; font-size: 2rem; margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(255, 99, 71, 0.4); font-weight: 600;
    }
    
    .calm-box {
        background: linear-gradient(135deg, #00CED1 0%, #20B2AA 50%, #008B8B 100%);
        padding: 3rem; border-radius: 20px; text-align: center;
        color: white; font-size: 2rem; margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 206, 209, 0.4); font-weight: 600;
    }
    
    .motivation-box {
        background: linear-gradient(135deg, #98FB98 0%, #90EE90 50%, #7FFFD4 100%);
        padding: 2rem; border-radius: 15px; text-align: center;
        margin: 2rem 0; font-size: 1.3rem; color: #2F4F4F;
        box-shadow: 0 8px 25px rgba(152, 251, 152, 0.3); font-weight: 500;
    }
    
    .disclaimer {
        background: linear-gradient(135deg, #FFFFE0 0%, #FFFACD 100%);
        border-left: 6px solid #FFD700; padding: 1.5rem;
        margin: 2rem 0; border-radius: 8px; color: #8B7500;
    }
    
    .stButton>button {
        border-radius: 30px; padding: 1rem 2.5rem;
        font-weight: 600; font-size: 1.1rem; border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover { transform: scale(1.05); }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Init files
def init_files():
    if not os.path.exists(USERS_FILE):
        pd.DataFrame(columns=['username', 'password']).to_csv(USERS_FILE, index=False)
    if not os.path.exists(THOUGHTS_FILE):
        pd.DataFrame(columns=['username', 'timestamp', 'thought_type', 'content']).to_csv(THOUGHTS_FILE, index=False)

def load_users():
    try: return pd.read_csv(USERS_FILE)
    except: return pd.DataFrame(columns=['username', 'password'])

def save_user(u, p):
    df = load_users()
    df = pd.concat([df, pd.DataFrame({'username': [u], 'password': [p]})], ignore_index=True)
    df.to_csv(USERS_FILE, index=False)

def verify_user(u, p):
    df = load_users()
    return not df[(df['username'] == u) & (df['password'] == p)].empty

def save_thought(u, t, c):
    df = pd.read_csv(THOUGHTS_FILE)
    new = pd.DataFrame({'username': [u], 'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                        'thought_type': [t], 'content': [c]})
    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(THOUGHTS_FILE, index=False)

# Content
STRESS_QUOTES = ["Take a deep breath. You're doing better than you think. 💙",
    "It's okay to take a break. Your mental health matters. 🌸",
    "One step at a time. You've got this. ✨",
    "This feeling is temporary. You will get through it. 🌈",
    "Be kind to yourself. You're doing your best. 💝"]

CALM_QUOTES = ["You're radiating positive energy today! ✨",
    "Your smile has the power to brighten someone's day. 😊",
    "Gratitude turns what we have into enough. 🙏",
    "Today is perfect for making beautiful memories. 📸",
    "You are exactly where you need to be right now. 🎯"]

DRAW_PROMPTS = ["🌈 Draw a rainbow with your favorite colors",
    "🦋 Sketch butterflies flying freely",
    "🌸 Create a garden of your dream flowers",
    "🌊 Draw calming ocean waves"]

QUOTES = ["The only way to do great work is to love what you do. - Steve Jobs",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Success is not final, failure is not fatal. - Winston Churchill"]

# Games
def breathing():
    st.markdown("## 🌬️ Breathing Exercise (4-7-8 Method)")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("<div style='background: linear-gradient(135deg, #87CEEB, #4682B4); padding: 2rem; border-radius: 15px; text-align: center; color: white;'><h2>Breathe In</h2><p style='font-size: 4rem;'>👃</p><p style='font-size: 1.5rem;'>4 seconds</p></div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown("<div style='background: linear-gradient(135deg, #FFB347, #FF8C00); padding: 2rem; border-radius: 15px; text-align: center; color: white;'><h2>Hold</h2><p style='font-size: 4rem;'>⏸️</p><p style='font-size: 1.5rem;'>7 seconds</p></div>", unsafe_allow_html=True)
    with cols[2]:
        st.markdown("<div style='background: linear-gradient(135deg, #98D8C8, #6BCF7F); padding: 2rem; border-radius: 15px; text-align: center; color: white;'><h2>Breathe Out</h2><p style='font-size: 4rem;'>😮‍💨</p><p style='font-size: 1.5rem;'>8 seconds</p></div>", unsafe_allow_html=True)
    
    if st.button("✅ Completed!", use_container_width=True):
        save_thought(st.session_state['username'], 'breathing', 'Done')
        st.success("🎉 Great job!")
        st.balloons()

def mood_tracker():
    st.markdown("## 😊 Mood Tracker")
    moods = [("😢", "Very Sad", "#FF6B6B"), ("😔", "Sad", "#FFA07A"), 
             ("😐", "Neutral", "#FFD700"), ("🙂", "Happy", "#90EE90"), ("😄", "Very Happy", "#00FF7F")]
    cols = st.columns(5)
    for i, (col, (emoji, mood, color)) in enumerate(zip(cols, moods)):
        with col:
            st.markdown(f"<div style='background: {color}; padding: 2rem; border-radius: 15px; text-align: center;'><p style='font-size: 3rem;'>{emoji}</p><p style='font-weight: 600;'>{mood}</p></div>", unsafe_allow_html=True)
            if st.button(f"Select", key=f"mood_{i}", use_container_width=True):
                save_thought(st.session_state['username'], 'mood', f"{emoji} {mood}")
                st.success(f"Mood logged: {emoji} {mood}")

def word_game():
    st.markdown("## 🎮 Word Scramble Game")
    words = {"PHYPA": "HAPPY", "EAPCE": "PEACE", "MISEL": "SMILE", "VELO": "LOVE", "ACML": "CALM"}
    if 'word' not in st.session_state:
        st.session_state.word = random.choice(list(words.keys()))
        st.session_state.score = 0
    
    scrambled = st.session_state.word
    correct = words[scrambled]
    st.markdown(f"<div style='background: linear-gradient(135deg, #FFB6C1, #FF69B4); padding: 3rem; border-radius: 20px; text-align: center;'><h2 style='color: white; font-size: 3rem; letter-spacing: 10px;'>{scrambled}</h2></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        answer = st.text_input("Your answer:", key="ans").upper()
    with col2:
        st.markdown(f"### Score: {st.session_state.score}")
    
    cols = st.columns(2)
    with cols[0]:
        if st.button("✅ Check", use_container_width=True):
            if answer == correct:
                st.success(f"🎉 Correct! The word is {correct}!")
                st.session_state.score += 10
                st.session_state.word = random.choice(list(words.keys()))
                st.balloons()
                st.rerun()
            elif answer:
                st.error("❌ Try again!")
    with cols[1]:
        if st.button("🔄 New Word", use_container_width=True):
            st.session_state.word = random.choice(list(words.keys()))
            st.rerun()

def quiz():
    st.markdown("## 🧠 Stress Management Quiz")
    qs = [{"q": "When overwhelmed, what's best?", "opts": ["Ignore feelings", "Take deep breaths", "Call everyone", "Blame yourself"],
           "correct": 1, "exp": "Deep breaths activate your calming system! 🌬️"},
          {"q": "Sleep needed for mental health?", "opts": ["4-5 hours", "6-7 hours", "7-9 hours", "10+ hours"],
           "correct": 2, "exp": "7-9 hours is optimal! 😴"}]
    
    if 'qidx' not in st.session_state:
        st.session_state.qidx = 0
        st.session_state.qscore = 0
        st.session_state.answered = False
    
    if st.session_state.qidx < len(qs):
        q = qs[st.session_state.qidx]
        st.markdown(f"<div style='background: linear-gradient(135deg, #A8E6CF, #77DD77); padding: 2rem; border-radius: 15px;'><h3>Question {st.session_state.qidx + 1}/{len(qs)}</h3><h2>{q['q']}</h2></div>", unsafe_allow_html=True)
        ans = st.radio("Choose:", q['opts'], key=f"q{st.session_state.qidx}")
        
        if st.button("Submit", use_container_width=True) and not st.session_state.answered:
            st.session_state.answered = True
            if q['opts'].index(ans) == q['correct']:
                st.success(f"✅ {q['exp']}")
                st.session_state.qscore += 1
                st.balloons()
            else:
                st.error(f"❌ {q['exp']}")
        
        if st.session_state.answered:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.qidx += 1
                st.session_state.answered = False
                st.rerun()
    else:
        st.markdown(f"<div style='background: linear-gradient(135deg, #FFD700, #FFA500); padding: 3rem; border-radius: 20px; text-align: center;'><h1 style='color: white;'>🎉 Complete!</h1><h2 style='color: white;'>Score: {st.session_state.qscore}/{len(qs)}</h2></div>", unsafe_allow_html=True)
        if st.button("🔄 Retry", use_container_width=True):
            st.session_state.qidx = 0
            st.session_state.qscore = 0
            st.rerun()

def gratitude():
    st.markdown("## 🌟 Gratitude Journal")
    gratitudes = [st.text_input(f"Gratitude #{i}:", key=f"g{i}", placeholder="I'm grateful for...") for i in range(1,4)]
    if st.button("💖 Save", use_container_width=True):
        if all(gratitudes):
            save_thought(st.session_state['username'], 'gratitude', " | ".join(gratitudes))
            st.success("✨ Saved!")
            st.balloons()
        else:
            st.warning("Fill all 3!")

def color_therapy():
    st.markdown("## 🎨 Color Therapy")
    st.markdown("### Pick colors that make you feel good!")
    colors = {"💙 Blue": "#4169E1", "💚 Green": "#32CD32", "💛 Yellow": "#FFD700", "💜 Purple": "#9370DB"}
    cols = st.columns(4)
    selected = []
    for i, (name, color) in enumerate(colors.items()):
        with cols[i]:
            st.markdown(f"<div style='background: {color}; padding: 3rem; border-radius: 15px; text-align: center;'><p style='font-size: 2rem;'>{name.split()[0]}</p></div>", unsafe_allow_html=True)
            if st.checkbox(name.split()[1], key=f"c{i}"):
                selected.append(name)
    if selected and st.button("💾 Save", use_container_width=True):
        save_thought(st.session_state['username'], 'colors', ", ".join(selected))
        st.success("🎨 Saved!")

# Pages
def login_page():
    st.markdown("<div style='position: absolute; width: 100%; height: 100%;'><div style='position: absolute; left: 10%; animation: fly 12s infinite;'>🦋</div><div style='position: absolute; left: 50%; animation: fly 15s infinite; animation-delay: 3s;'>🦋</div><div style='position: absolute; left: 80%; animation: fly 18s infinite; animation-delay: 6s;'>🦋</div></div>", unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🦋 CalmNow 🦋</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #8B2952; font-size: 1.3rem; margin-bottom: 2rem;">Your Safe Space for Peace & Growth</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])
    
    with tab1:
        u = st.text_input("Username", key="lu")
        p = st.text_input("Password", type="password", key="lp")
        if st.button("🦋 Login", use_container_width=True):
            if u and p and verify_user(u, p):
                st.session_state.logged_in = True
                st.session_state.username = u
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Invalid")
    
    with tab2:
        nu = st.text_input("Username", key="nu")
        np = st.text_input("Password", type="password", key="np")
        cp = st.text_input("Confirm", type="password", key="cp")
        if st.button("🌸 Sign Up", use_container_width=True):
            if nu and np and cp:
                if np != cp:
                    st.error("❌ Passwords don't match")
                elif nu in load_users()['username'].values:
                    st.error("❌ Username exists")
                else:
                    save_user(nu, np)
                    st.success("✅ Account created! Login now.")
                    st.balloons()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="disclaimer"><strong>⚠️ Notice:</strong> This supports wellness, not professional therapy. Emergency: 988 (US) or Crisis Text Line: HOME to 741741</div>', unsafe_allow_html=True)

def stress_check():
    st.markdown(f'<div class="main-header"><h1>🦋 Welcome, {st.session_state.username}! 🦋</h1><p style="font-size: 1.3rem;">Let\'s check in...</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="stress-box"><h2>How are you feeling?</h2><p style="font-size: 1.2rem;">Be honest. No wrong answer.</p></div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    with cols[0]:
        if st.button("😰 YES, stressed", use_container_width=True):
            st.session_state.page = 'stressed'
            st.rerun()
    with cols[1]:
        if st.button("😊 NO, good", use_container_width=True):
            st.session_state.page = 'calm'
            st.rerun()
    
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

def stressed_page():
    st.markdown('<div class="main-header" style="background: linear-gradient(135deg, #FF6B6B, #FF8E53);"><h1>💝 Let\'s Help You Feel Better</h1><p style="font-size: 1.3rem;">Choose what feels right</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="motivation-box">💭 {random.choice(STRESS_QUOTES)}</div>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 Activities:")
    cols = st.columns(3)
    with cols[0]:
        if st.button("🎵 Music", use_container_width=True): st.session_state.activity = 'music'
    with cols[1]:
        if st.button("🎨 Draw", use_container_width=True): st.session_state.activity = 'draw'
    with cols[2]:
        if st.button("✍️ Write", use_container_width=True): st.session_state.activity = 'write'
    
    st.markdown("### 🎮 Games:")
    cols = st.columns(4)
    with cols[0]:
        if st.button("🌬️ Breathing", use_container_width=True): st.session_state.activity = 'breathing'
    with cols[1]:
        if st.button("😊 Mood", use_container_width=True): st.session_state.activity = 'mood'
    with cols[2]:
        if st.button("🎮 Word Game", use_container_width=True): st.session_state.activity = 'word'
    with cols[3]:
        if st.button("🧠 Quiz", use_container_width=True): st.session_state.activity = 'quiz'
    
    st.markdown("---")
    
    if st.session_state.get('activity') == 'music': show_music()
    elif st.session_state.get('activity') == 'draw': show_draw()
    elif st.session_state.get('activity') == 'write': show_write()
    elif st.session_state.get('activity') == 'breathing': breathing()
    elif st.session_state.get('activity') == 'mood': mood_tracker()
    elif st.session_state.get('activity') == 'word': word_game()
    elif st.session_state.get('activity') == 'quiz': quiz()
    
    st.markdown("---")
    cols = st.columns(2)
    with cols[0]:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.page = 'main'
            if 'activity' in st.session_state: del st.session_state.activity
            st.rerun()
    with cols[1]:
        if st.button("🚪 Logout", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

def calm_page():
    st.markdown('<div class="main-header" style="background: linear-gradient(135deg, #56CCF2, #2F80ED);"><h1>✨ Wonderful! ✨</h1><p style="font-size: 1.3rem;">Keep that positive energy!</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="background: linear-gradient(135deg, #E6E6FA, #D8BFD8, #DDA0DD); padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0; font-size: 1.3rem; color: #4B0082;">🌟 {random.choice(CALM_QUOTES)}</div>', unsafe_allow_html=True)
    
    st.markdown("### 💫 Activities:")
    cols = st.columns(4)
    with cols[0]:
        if st.button("🌟 Gratitude", use_container_width=True): st.session_state.activity = 'gratitude'
    with cols[1]:
        if st.button("📚 Quotes", use_container_width=True): st.session_state.activity = 'learning'
    with cols[2]:
        if st.button("🎨 Colors", use_container_width=True): st.session_state.activity = 'colors'
    with cols[3]:
        if st.button("🎮 Word Game", use_container_width=True): st.session_state.activity = 'word'
    
    st.markdown("---")
    
    if st.session_state.get('activity') == 'gratitude': gratitude()
    elif st.session_state.get('activity') == 'learning': show_learning()
    elif st.session_state.get('activity') == 'colors': color_therapy()
    elif st.session_state.get('activity') == 'word': word_game()
    
    st.markdown("---")
    cols = st.columns(2)
    with cols[0]:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.page = 'main'
            if 'activity' in st.session_state: del st.session_state.activity
            st.rerun()
    with cols[1]:
        if st.button("🚪 Logout", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

def show_music():
    st.markdown("## 🎵 Music Therapy")
    st.markdown("<div style='background: linear-gradient(135deg, #F8B195, #F67280); padding: 2rem; border-radius: 15px; text-align: center; color: white;'><h3>🎧 Listen and let your mind slow down</h3></div>", unsafe_allow_html=True)
    
    music = {"🌊 Ocean": "https://youtube.com/watch?v=fn3KWM1kuAw", "🌧️ Rain": "https://youtube.com/watch?v=mPZkdNFkNps", "🎹 Piano": "https://youtube.com/watch?v=lTRiuFIWV54"}
    cols = st.columns(3)
    for i, (t, u) in enumerate(music.items()):
        with cols[i]:
            st.markdown(f"<div style='background: linear-gradient(135deg, #667eea, #764ba2); padding: 1.5rem; border-radius: 15px; text-align: center;'><h4 style='color: white;'>{t}</h4><a href='{u}' target='_blank'><button style='background: rgba(255,255,255,0.3); border: none; padding: 10px 20px; border-radius: 20px; color: white;'>▶️ Listen</button></a></div>", unsafe_allow_html=True)
    
    feeling = st.text_area("How do you feel?", placeholder="The music made me feel...")
    if st.button("💖 Save", use_container_width=True):
        if feeling:
            save_thought(st.session_state.username, 'music', feeling)
            st.success("✨ Saved!")
            st.balloons()

def show_draw():
    st.markdown("## 🎨 Creative Expression")
    prompt = random.choice(DRAW_PROMPTS)
    st.markdown(f"<div style='background: linear-gradient(135deg, #A8E6CF, #FFD3B6); padding: 2rem; border-radius: 15px; text-align: center;'><h3>✨ Today's Prompt:</h3><h2>{prompt}</h2></div>", unsafe_allow_html=True)
    
    notes = st.text_area("Describe your art:", height=200, placeholder="I drew...")
    if st.button("💝 Save", use_container_width=True):
        if notes:
            save_thought(st.session_state.username, 'drawing', notes)
            st.success("✨ Saved!")
            st.balloons()

def show_write():
    st.markdown("## ✍️ Journal")
    st.markdown("<div style='background: linear-gradient(135deg, #84FAB0, #8FD3F4); padding: 2rem; border-radius: 15px; text-align: center;'><h3>📖 Write freely. No judgment.</h3></div>", unsafe_allow_html=True)
    
    thoughts = st.text_area("What's on your mind?", height=300, placeholder="I'm feeling...")
    if st.button("💾 Save", use_container_width=True):
        if thoughts:
            save_thought(st.session_state.username, 'journal', thoughts)
            st.success("✨ Saved!")
            st.balloons()
    
    if st.checkbox("📚 View Past"):
        try:
            df = pd.read_csv(THOUGHTS_FILE)
            user_df = df[(df['username'] == st.session_state.username) & (df['thought_type'] == 'journal')].sort_values('timestamp', ascending=False)
            if not user_df.empty:
                for _, row in user_df.head(10).iterrows():
                    with st.expander(f"📝 {row['timestamp']}"):
                        st.write(row['content'])
        except:
            st.info("No entries yet")

def show_learning():
    st.markdown("## 📚 Inspiration")
    quote = random.choice(QUOTES)
    st.markdown(f"<div style='background: linear-gradient(135deg, #FFECD2, #FCB69F); padding: 3rem; border-radius: 20px; text-align: center; font-size: 1.5rem; color: #8B4513;'><h2>💡 Quote</h2><p style='font-style: italic;'>\"{quote}\"</p></div>", unsafe_allow_html=True)
    
    reflection = st.text_area("How can you apply this?", height=150)
    if st.button("💫 Save", use_container_width=True):
        if reflection:
            save_thought(st.session_state.username, 'learning', f"{quote} | {reflection}")
            st.success("✨ Saved!")
            st.balloons()

def main():
    init_files()
    load_css()
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = 'main'
    
    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.page == 'main':
            stress_check()
        elif st.session_state.page == 'stressed':
            stressed_page()
        elif st.session_state.page == 'calm':
            calm_page()

if __name__ == "__main__":
    main()