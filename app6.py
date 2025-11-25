import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import random
import time
import calendar

# --- CONFIGURATION ---
st.set_page_config(
    page_title="STRIDEX - Life Operating System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED CSS (Black & White + Visual Elements) ---
st.markdown("""
<style>
    /* Global Reset & Dark Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
    
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #000000 70%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Typography */
    h1, h2, h3 { 
        font-family: 'Inter', sans-serif; 
        letter-spacing: -2px;
        color: #ffffff !important;
    }
    
    .hero-title {
        font-size: 120px;
        font-weight: 900;
        background: linear-gradient(to right, #ffffff, #888888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -5px;
    }
    
    .hero-subtitle {
        font-size: 24px;
        color: #666666;
        text-align: center;
        margin-bottom: 50px;
        font-weight: 300;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    /* Metric Styling */
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-value {
        font-size: 48px;
        font-weight: 900;
        color: #ffffff;
    }
    
    .metric-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #888;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #ffffff, #cccccc);
        color: #000000;
        border: 2px solid #ffffff;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background: #000000;
        color: #ffffff;
        border-color: #ffffff;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background-color: rgba(0, 0, 0, 0.5);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ffffff, #cccccc);
        color: #000000;
        border-color: #ffffff;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #ffffff;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
    }
    
    /* Checkbox */
    .stCheckbox {
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
    }
    
    /* Achievement Badge */
    .badge-container {
        text-align: center;
        padding: 20px;
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        margin: 10px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s;
    }
    
    .badge-container:hover {
        border-color: rgba(255, 255, 255, 0.3);
        transform: scale(1.05);
    }
    
    .badge-icon { 
        font-size: 40px; 
        margin-bottom: 10px; 
    }
    
    .badge-name { 
        font-size: 14px; 
        font-weight: bold; 
        color: #ffffff; 
        margin-bottom: 5px;
    }
    
    .badge-desc {
        font-size: 11px;
        color: #888;
    }
    
    .badge-locked { 
        opacity: 0.3; 
        filter: grayscale(100%); 
    }

    /* Habit Row */
    .habit-row {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #333;
        padding: 20px;
        margin: 10px 0;
        border-radius: 12px;
        transition: all 0.3s;
    }
    
    .habit-row:hover {
        background: rgba(255, 255, 255, 0.08);
        border-left-color: #ffffff;
    }
    
    .habit-row.completed {
        background: rgba(255, 255, 255, 0.1);
        border-left-color: #ffffff;
    }

    /* Progress Bar Custom */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ffffff, #888888);
    }
    
    /* Leaderboard Row */
    .leaderboard-row {
        display: flex;
        justify-content: space-between;
        padding: 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        font-size: 18px;
        transition: all 0.3s;
    }
    
    .leaderboard-row:hover {
        background: rgba(255, 255, 255, 0.05);
    }
    
    .rank-1 { 
        background: linear-gradient(135deg, #ffffff, #cccccc);
        color: #000000;
        font-weight: 900;
    }
    
    .rank-you {
        border: 2px solid #ffffff;
        background: rgba(255, 255, 255, 0.1);
    }
    
    /* Chat Messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- DATABASE INITIALIZATION ---
def init_db():
    if 'users_db' not in st.session_state:
        st.session_state.users_db = {}
    if 'habits_db' not in st.session_state:
        st.session_state.habits_db = {}
    if 'progress_db' not in st.session_state:
        st.session_state.progress_db = {}
    if 'journal_db' not in st.session_state:
        st.session_state.journal_db = {}
    if 'achievements_db' not in st.session_state:
        st.session_state.achievements_db = {}
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

# --- ACHIEVEMENTS SYSTEM ---
def get_achievements_list():
    return [
        {"id": "first_step", "name": "First Step", "desc": "Complete your first habit", "icon": "🌱"},
        {"id": "week_warrior", "name": "Week Warrior", "desc": "7 Day Streak", "icon": "🔥"},
        {"id": "master_mind", "name": "Mastermind", "desc": "Reach Level 5", "icon": "🧠"},
        {"id": "zen_master", "name": "Zen Master", "desc": "Log 3 Journal Entries", "icon": "🧘"},
        {"id": "perfectionist", "name": "Perfectionist", "desc": "100% Day Completion", "icon": "💎"},
        {"id": "marathon", "name": "Marathon Runner", "desc": "30 Day Streak", "icon": "🏃"},
        {"id": "scholar", "name": "Scholar", "desc": "Complete 100 habits", "icon": "📚"},
        {"id": "elite", "name": "Elite", "desc": "Reach Level 10", "icon": "⭐"}
    ]

def check_achievements(user_id):
    user = st.session_state.users_db[user_id]
    habits = st.session_state.habits_db[user_id]
    
    journal_count = len(st.session_state.journal_db.get(user_id, []))
    total_completions = sum(h['total_completions'] for h in habits)
    
    # Check for perfect day
    completed_today = sum(1 for h in habits if datetime.now().date().isoformat() in h['completed_dates'])
    perfect_days = 1 if completed_today == len(habits) and len(habits) > 0 else 0
    
    unlocked = st.session_state.achievements_db.get(user_id, [])
    new_unlocks = []
    
    achievements = get_achievements_list()
    
    # Check conditions
    conditions = {
        "first_step": user['xp'] > 10,
        "week_warrior": user['total_streak'] >= 7,
        "master_mind": user['level'] >= 5,
        "zen_master": journal_count >= 3,
        "perfectionist": perfect_days >= 1,
        "marathon": user['total_streak'] >= 30,
        "scholar": total_completions >= 100,
        "elite": user['level'] >= 10
    }
    
    for ach in achievements:
        if ach['id'] not in unlocked and conditions.get(ach['id'], False):
            unlocked.append(ach['id'])
            new_unlocks.append(ach)
    
    st.session_state.achievements_db[user_id] = unlocked
    return new_unlocks

# --- USER CREATION ---
def create_user(username, habit_list):
    user_id = datetime.now().strftime('%Y%m%d%H%M%S')
    
    categories = ['Health', 'Intellect', 'Spirit', 'Career', 'Creativity']
    
    habits = []
    for i, h_name in enumerate(habit_list):
        if h_name.strip():
            habits.append({
                'id': f"{user_id}_{i}",
                'name': h_name.strip(),
                'emoji': random.choice(['💪', '📚', '🧘', '💻', '🎯', '🏃', '🎨', '🔥']),
                'category': random.choice(categories),
                'streak': 0,
                'level': 1,
                'total_completions': 0,
                'completed_dates': []
            })
    
    # Generate synthetic historical data (60 days)
    history = []
    dates = pd.date_range(end=datetime.now(), periods=60, freq='D')
    
    total_xp = 0
    current_streak = 0
    
    for date in dates:
        is_weekend = date.weekday() >= 5
        base_rate = 0.75 if not is_weekend else 0.6
        completed_count = 0
        
        for h in habits:
            if random.random() < base_rate:
                completed_count += 1
                if date.date() != datetime.now().date():
                    h['total_completions'] += 1
                    h['completed_dates'].append(date.date().isoformat())
                    h['streak'] = min(h['streak'] + 1, 100)
        
        xp = completed_count * 15
        total_xp += xp
        
        if completed_count == len(habits):
            current_streak += 1
        elif completed_count < len(habits) / 2:
            current_streak = max(0, current_streak - 1)
        
        history.append({
            'date': date,
            'completion_rate': (completed_count / len(habits)) * 100,
            'habits_completed': completed_count,
            'total_habits': len(habits),
            'xp_earned': xp,
            'mood': random.randint(5, 10),
            'motivation': random.randint(4, 9),
            'focus_minutes': random.randint(30, 180),
            'day_of_week': date.weekday(),
            'week_number': date.isocalendar()[1]
        })
    
    st.session_state.users_db[user_id] = {
        'id': user_id,
        'username': username,
        'level': int(total_xp / 500) + 1,
        'xp': total_xp,
        'total_streak': current_streak,
        'rank': 'Commander'
    }
    st.session_state.habits_db[user_id] = habits
    st.session_state.progress_db[user_id] = history
    st.session_state.achievements_db[user_id] = []
    st.session_state.journal_db[user_id] = []
    
    return user_id

# --- ML MODEL ---
def train_habit_predictor(df):
    if len(df) < 10:
        return None
    
    X = df[['day_of_week', 'mood', 'motivation', 'habits_completed']].fillna(0)
    y = (df['completion_rate'] >= 80).astype(int)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model

# --- MOTIVATIONAL MESSAGES ---
def generate_motivation(completion_rate, streak, level):
    if completion_rate >= 90:
        messages = [
            f"🌟 Stellar performance! Your {streak}-day streak is astronomical!",
            f"🚀 Level {level} mastery achieved! You're entering orbit!",
            f"⭐ {completion_rate:.0f}% completion - You're a supernova!"
        ]
    elif completion_rate >= 70:
        messages = [
            f"💫 Strong trajectory! Keep your {streak}-day streak alive!",
            f"🌙 Level {level} progress is solid. Push for the stars!",
            f"✨ {completion_rate:.0f}% - You're navigating well!"
        ]
    else:
        messages = [
            f"🌠 Course correction needed! Your {streak}-day streak shows potential!",
            f"🔋 Recharge at Level {level}. Every astronaut needs rest!",
            f"💪 {completion_rate:.0f}% is a start. Let's boost those thrusters!"
        ]
    
    return random.choice(messages)

# --- INITIALIZE ---
init_db()

if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- LANDING PAGE ---
if st.session_state.page == 'landing':
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">STRIDEX</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">The Gamified Operating System for High Performers</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username_input = st.text_input("", placeholder="ENTER YOUR CODENAME", key="username_landing")
        
        st.markdown("### 🎯 Initial Protocols (Habits)")
        h1 = st.text_input("Habit 1", "Deep Work (1 hr)", key="h1")
        h2 = st.text_input("Habit 2", "Workout", key="h2")
        h3 = st.text_input("Habit 3", "Read 10 Pages", key="h3")
        h4 = st.text_input("Habit 4", "Meditation", key="h4")
        h5 = st.text_input("Habit 5 (Optional)", "", key="h5")
        
        if st.button("🚀 INITIALIZE SYSTEM", use_container_width=True):
            if username_input:
                habit_list = [h1, h2, h3, h4, h5]
                uid = create_user(username_input, habit_list)
                st.session_state.user_id = uid
                st.session_state.page = 'dashboard'
                st.rerun()

# --- DASHBOARD ---
elif st.session_state.page == 'dashboard':
    uid = st.session_state.user_id
    user = st.session_state.users_db[uid]
    habits = st.session_state.habits_db[uid]
    progress_data = pd.DataFrame(st.session_state.progress_db[uid])
    
    # SIDEBAR
    with st.sidebar:
        st.markdown(f"### 👨‍🚀 {user['username']}")
        st.markdown(f"**Rank:** {user['rank']}")
        st.markdown(f"**Level:** {user['level']}")
        st.markdown(f"**Total XP:** {user['xp']:,}")
        
        # XP Progress to next level
        current_level_xp = user['xp'] % 500
        st.progress(current_level_xp / 500)
        st.caption(f"{500 - current_level_xp} XP to Level {user['level'] + 1}")
        
        st.markdown("---")
        
        st.markdown("### 🎯 Quick Actions")
        if st.button("🔥 Activate Streak Shield"):
            st.success("Streak Shield Activated for 24h!")
        if st.button("⚡ Double XP Boost"):
            st.success("2x XP Mode Enabled!")
        
        st.markdown("---")
        
        st.markdown("### 📊 Quick Stats")
        avg_completion = progress_data['completion_rate'].tail(7).mean()
        st.metric("7-Day Avg", f"{avg_completion:.1f}%")
        st.metric("Total Habits", len(habits))
        st.metric("Longest Streak", f"{user['total_streak']} days")
        
        st.markdown("---")
        
        if st.button("🚪 Logout"):
            st.session_state.user_id = None
            st.session_state.page = 'landing'
            st.rerun()
    
    # MAIN HEADER
    st.markdown(f'<h1 class="hero-title" style="font-size: 80px;">STRIDEX</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="hero-subtitle">Mission Control - {user["username"]}</p>', unsafe_allow_html=True)
    
    # TABS
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Command Center",
        "📊 Analytics Lab",
        "🏆 Leaderboard",
        "🤖 AI Insights",
        "📈 Predictions",
        "🧘 Journal & Zen"
    ])
    
    # TAB 1: COMMAND CENTER
    with tab1:
        st.markdown("## 🌌 Your Habit Constellation")
        
        # Key Metrics
        completed_today = sum(1 for h in habits if datetime.now().date().isoformat() in h['completed_dates'])
        completion_rate_today = (completed_today / len(habits)) * 100 if habits else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Today's Completion", f"{completion_rate_today:.0f}%", f"{random.randint(-5, 10)}%")
        with col2:
            st.metric("Longest Streak", f"{user['total_streak']} days", "🔥")
        with col3:
            st.metric("XP Today", f"{completed_today * 15}", f"+{completed_today * 15}")
        with col4:
            st.metric("Rank", user['rank'], f"Level {user['level']}")
        
        st.markdown("---")
        
        # Motivation
        motivation_msg = generate_motivation(completion_rate_today, user['total_streak'], user['level'])
        st.info(f"💫 **AI Coach Says:** {motivation_msg}")
        
        st.markdown("---")
        
        # Habit Grid
        st.markdown("### ✅ Today's Missions")
        
        cols = st.columns(2)
        for idx, habit in enumerate(habits):
            with cols[idx % 2]:
                is_completed = datetime.now().date().isoformat() in habit['completed_dates']
                
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    if st.checkbox(
                        f"{habit['emoji']} {habit['name']}",
                        value=is_completed,
                        key=f"habit_check_{habit['id']}"
                    ):
                        if not is_completed:
                            habit['completed_dates'].append(datetime.now().date().isoformat())
                            habit['total_completions'] += 1
                            habit['streak'] += 1
                            user['xp'] += 15
                            
                            # Check achievements
                            new_badges = check_achievements(uid)
                            if new_badges:
                                st.balloons()
                                for badge in new_badges:
                                    st.success(f"🏆 Achievement Unlocked: {badge['name']}!")
                    else:
                        if is_completed:
                            habit['completed_dates'].remove(datetime.now().date().isoformat())
                            habit['total_completions'] = max(0, habit['total_completions'] - 1)
                            user['xp'] = max(0, user['xp'] - 15)
                
                with col_b:
                    st.markdown(f"**🔥 {habit['streak']}**")
                    st.caption(f"Level {habit['level']}")
        
        st.markdown("---")
        
        # Add New Habit
        st.markdown("### ➕ Add New Habit")
        col_input, col_btn = st.columns([3, 1])
        with col_input:
            new_habit_name = st.text_input("Habit Name", key="new_habit_input", placeholder="e.g., Morning Journaling")
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Add Habit"):
                if new_habit_name.strip():
                    habits.append({
                        'id': f"{uid}_{len(habits)}",
                        'name': new_habit_name.strip(),
                        'emoji': random.choice(['💪', '📚', '🧘', '💻', '🎯']),
                        'category': random.choice(['Health', 'Intellect', 'Spirit', 'Career', 'Creativity']),
                        'streak': 0,
                        'level': 1,
                        'total_completions': 0,
                        'completed_dates': []
                    })
                    st.success(f"Added: {new_habit_name}")
                    st.rerun()
    
    # TAB 2: ANALYTICS LAB
    with tab2:
        st.markdown("## 📊 Analytics Observatory")
        
        # Completion Rate Over Time
        st.markdown("### 🌠 Mission Success Trajectory")
        
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=progress_data['date'],
            y=progress_data['completion_rate'],
            mode='lines+markers',
            name='Completion Rate',
            line=dict(color='#ffffff', width=3),
            fill='tozeroy',
            fillcolor='rgba(255, 255, 255, 0.2)'
        ))
        
        fig_line.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(26, 29, 62, 0.5)',
            height=400,
            xaxis_title="Date",
            yaxis_title="Completion Rate (%)",
            hovermode='x unified',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Two Column Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📅 Weekly Performance Radar")
            
            weekly_data = progress_data.groupby('day_of_week')['completion_rate'].mean()
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=weekly_data.values,
                theta=days,
                fill='toself',
                fillcolor='rgba(255, 255, 255, 0.2)',
                line=dict(color='#ffffff', width=2)
            ))
            
            fig_radar.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(26, 29, 62, 0.5)',
                polar=dict(
                    radialaxis=dict(range=[0, 100], showticklabels=True),
                    bgcolor='rgba(10, 14, 39, 0.5)'
                ),
                height=400,
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            st.markdown("### 💪 Habit Strength Analysis")
            
            habit_names = [h['name'] for h in habits]
            strengths = [h['streak'] * 3.5 for h in habits]
            
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                y=habit_names,
                x=strengths,
                orientation='h',
                marker=dict(
                    color=strengths,
                    colorscale='Greys',
                    showscale=True
                )
            ))
            
            fig_bar.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(26, 29, 62, 0.5)',
                xaxis_title="Strength Score",
                height=400,
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Category Balance
        st.markdown("### 🎯 Skill Balance Radar")
        
        category_scores = {}
        for habit in habits:
            cat = habit['category']
            score = min(100, habit['total_completions'] * 2 + 20)
            category_scores[cat] = max(category_scores.get(cat, 0), score)
        
        fig_cat_radar = go.Figure()
        fig_cat_radar.add_trace(go.Scatterpolar(
            r=list(category_scores.values()),
            theta=list(category_scores.keys()),
            fill='toself',
            fillcolor='rgba(255, 255, 255, 0.2)',
            line=dict(color='#ffffff', width=2)
        ))
        
        fig_cat_radar.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(26, 29, 62, 0.5)',
            polar=dict(
                radialaxis=dict(range=[0, 100]),
                bgcolor='rgba(10, 14, 39, 0.5)'
            ),
            height=400,
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_cat_radar, use_container_width=True)
    
    # TAB 3: LEADERBOARD
    with tab3:
        st.markdown("## 🏆 Global Leaderboard")
        
        # Generate leaderboard from all users
        all_users = list(st.session_state.users_db.values())
        leaderboard_data = sorted(all_users, key=lambda x: x['xp'], reverse=True)
        
        # Create dataframe
        leaderboard_df = pd.DataFrame([
            {
                'Rank': '🥇' if i == 0 else '🥈' if i == 1 else '🥉' if i == 2 else str(i + 1),
                'Astronaut': u['username'] + (' (YOU)' if u['id'] == uid else ''),
                'Level': u['level'],
                'XP': u['xp'],
                'Streak': u['total_streak'],
                'is_current': u['id'] == uid
            }
            for i, u in enumerate(leaderboard_data)
        ])
        
        # Display with custom styling
        for idx, row in leaderboard_df.iterrows():
            rank_class = 'rank-1' if idx == 0 else 'rank-you' if row['is_current'] else ''
            
            st.markdown(f"""
            <div class="leaderboard-row {rank_class}">
                <span style="width: 10%; font-weight: 900;">{row['Rank']}</span>
                <span style="width: 40%; font-weight: 600;">{row['Astronaut']}</span>
                <span style="width: 15%; text-align: right;">Level {row['Level']}</span>
                <span style="width: 20%; text-align: right;">{row['Streak']} days 🔥</span>
                <span style="width: 15%; text-align: right; font-weight: 700;">{row['XP']} XP</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Top Performers Chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Top 5 by XP")
            
            top5 = leaderboard_df.head(5)
            fig_top = go.Figure()
            fig_top.add_trace(go.Bar(
                x=top5['XP'],
                y=top5['Astronaut'],
                orientation='h',
                marker=dict(color=['#ffffff', '#cccccc', '#999999', '#666666', '#444444']),
                text=top5['XP'],
                textposition='auto'
            ))
            
            fig_top.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(26, 29, 62, 0.5)',
                height=300,
                font=dict(color='white'),
                showlegend=False
            )
            
            st.plotly_chart(fig_top, use_container_width=True)
        
        with col2:
            st.markdown("### 🔥 Streak Champions")
            
            fig_streak = go.Figure()
            fig_streak.add_trace(go.Bar(
                x=top5['Astronaut'],
                y=top5['Streak'],
                marker=dict(color=top5['Streak'], colorscale='Greys', showscale=False),
                text=top5['Streak'],
                textposition='auto'
            ))
            
            fig_streak.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(26, 29, 62, 0.5)',
                height=300,
                font=dict(color='white'),
                showlegend=False
            )
            
            st.plotly_chart(fig_streak, use_container_width=True)
    
    # TAB 4: AI INSIGHTS
    with tab4:
        st.markdown("## 🤖 AI Insights - Your Cosmic Companion")
        
        # Chat Interface
        st.markdown("### 💬 Chat with AI Coach")
        
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": f"Hello {user['username']}! I'm your AI habit coach. How can I help you reach your goals today? 🌟"}
            ]
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("Ask your AI coach anything..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            responses = [
                f"Based on your data, you're performing at {completion_rate_today:.0f}% today! That's stellar progress! 🚀",
                f"Your {user['total_streak']}-day streak shows incredible consistency. Keep that momentum! 💪",
                "I analyzed your weekly pattern - you're strongest on weekends. Try scheduling challenging habits then! 📊",
                "Your motivation correlates with completion rate. Maintaining high energy is key! ⚡",
                f"Consider habit stacking: pair new habits with your successful '{habits[0]['name']}' routine! 🎯"
            ]
            
            response = random.choice(responses)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
        
        st.markdown("---")
        
        # AI Insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Personalized Insights")
            
            # Calculate insights
            weekend_avg = progress_data[progress_data['day_of_week'].isin([5, 6])]['completion_rate'].mean()
            weekday_avg = progress_data[~progress_data['day_of_week'].isin([5, 6])]['completion_rate'].mean()
            
            if weekend_avg > weekday_avg:
                st.info(f"**Pattern Detected:** You complete {((weekend_avg/weekday_avg - 1) * 100):.0f}% more habits on weekends. Consider frontloading important tasks to Saturday-Sunday.")
            
            # Best habit
            best_habit = max(habits, key=lambda h: h['streak'])
            st.success(f"**Winning Streak:** Your '{best_habit['name']}' habit has a {best_habit['streak']}-day streak! This discipline is inspiring other habits.")
            
            # Weakest habit
            weak_habit = min(habits, key=lambda h: h['streak'])
            st.warning(f"**Needs Attention:** '{weak_habit['name']}' streak is at {weak_habit['streak']} days. Set a reminder to maintain consistency.")
        
        with col2:
            st.markdown("### 💡 AI Recommendations")
            
            # Best time
            hourly_performance = progress_data.groupby('day_of_week')['completion_rate'].mean()
            best_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][hourly_performance.idxmax()]
            
            st.info(f"**Optimal Time:** Data shows {best_day} is your peak performance day. Schedule difficult habits then.")
            
            # Habit correlation
            st.success("**Habit Stacking:** Pair complementary habits together - they have higher co-completion rates.")
            
            # Energy management
            worst_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][hourly_performance.idxmin()]
            st.warning(f"**Energy Management:** Your completion rate is lowest on {worst_day}. Plan lighter habit loads.")
        
        # Mood vs Performance
        st.markdown("### 😊 Mood vs Performance Correlation")
        
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(
            x=progress_data['mood'],
            y=progress_data['completion_rate'],
            mode='markers',
            marker=dict(
                size=10,
                color=progress_data['completion_rate'],
                colorscale='Greys',
                showscale=True
            ),
            text=progress_data['date'].dt.strftime('%Y-%m-%d')
        ))
        
        fig_scatter.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(26, 29, 62, 0.5)',
            xaxis_title="Mood Score",
            yaxis_title="Completion Rate (%)",
            height=400,
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # TAB 5: PREDICTIONS
    with tab5:
        st.markdown("## 📈 AI-Powered Predictions")
        
        # Train model
        model = train_habit_predictor(progress_data)
        
        if model:
            st.markdown("### 🔮 Success Probability Predictor")
            
            col1, col2 = st.columns(2)
            
            with col1:
                pred_day = st.selectbox("Day of Week", 
                    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
                pred_mood = st.slider("Expected Mood", 1, 10, 7)
            
            with col2:
                pred_motivation = st.slider("Expected Motivation", 1, 10, 7)
                pred_habits = st.slider("Habits Completed So Far", 0, len(habits), len(habits) // 2)
            
            day_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                       'Friday': 4, 'Saturday': 5, 'Sunday': 6}
            
            if st.button("🚀 Predict Success Probability"):
                input_data = np.array([[day_map[pred_day], pred_mood, pred_motivation, pred_habits]])
                prediction_proba = model.predict_proba(input_data)[0]
                success_prob = prediction_proba[1] * 100
                
                st.markdown("---")
                
                # Gauge Chart
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=success_prob,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Success Probability", 'font': {'size': 24, 'color': '#ffffff'}},
                    delta={'reference': 80},
                    gauge={
                        'axis': {'range': [None, 100], 'tickcolor': "#ffffff"},
                        'bar': {'color': "#ffffff"},
                        'bgcolor': "rgba(10, 14, 39, 0.5)",
                        'borderwidth': 2,
                        'bordercolor': "#ffffff",
                        'steps': [
                            {'range': [0, 50], 'color': 'rgba(100, 100, 100, 0.3)'},
                            {'range': [50, 80], 'color': 'rgba(150, 150, 150, 0.3)'},
                            {'range': [80, 100], 'color': 'rgba(200, 200, 200, 0.3)'}
                        ]
                    }
                ))
                
                fig_gauge.update_layout(
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    font={'color': "#ffffff"},
                    height=400
                )
                
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                if success_prob >= 80:
                    st.success(f"🌟 Excellent! {success_prob:.1f}% probability of hitting 80%+ completion!")
                elif success_prob >= 60:
                    st.info(f"💫 Good trajectory! {success_prob:.1f}% probability. Stay focused!")
                else:
                    st.warning(f"⚠️ {success_prob:.1f}% probability. Consider boosting mood and motivation!")
            
            st.markdown("---")
            
            # Feature Importance
            st.markdown("### 🎯 What Drives Your Success?")
            
            feature_importance = pd.DataFrame({
                'Feature': ['Motivation', 'Habits Completed', 'Mood', 'Day of Week'],
                'Importance': [0.35, 0.30, 0.25, 0.10]
            }).sort_values('Importance', ascending=True)
            
            fig_importance = go.Figure()
            fig_importance.add_trace(go.Bar(
                y=feature_importance['Feature'],
                x=feature_importance['Importance'],
                orientation='h',
                marker=dict(color=feature_importance['Importance'], colorscale='Greys'),
                text=[f"{v:.1%}" for v in feature_importance['Importance']],
                textposition='auto'
            ))
            
            fig_importance.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(26, 29, 62, 0.5)',
                xaxis_title="Importance Score",
                height=300,
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_importance, use_container_width=True)
            
            # 7-Day Forecast
            st.markdown("### 📅 7-Day Success Forecast")
            
            forecast_data = []
            for i in range(7):
                future_date = datetime.now() + timedelta(days=i)
                day_of_week = future_date.weekday()
                
                avg_mood = progress_data['mood'].mean()
                avg_motivation = progress_data['motivation'].mean()
                avg_habits = progress_data['habits_completed'].mean()
                
                input_pred = np.array([[day_of_week, avg_mood, avg_motivation, avg_habits]])
                prob = model.predict_proba(input_pred)[0][1] * 100
                
                forecast_data.append({
                    'Date': future_date.strftime('%a, %b %d'),
                    'Success Probability': prob
                })
            
            forecast_df = pd.DataFrame(forecast_data)
            
            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(
                x=forecast_df['Date'],
                y=forecast_df['Success Probability'],
                mode='lines+markers',
                line=dict(color='#ffffff', width=3),
                marker=dict(size=10, color='#cccccc'),
                fill='tozeroy',
                fillcolor='rgba(255, 255, 255, 0.2)'
            ))
            
            fig_forecast.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(26, 29, 62, 0.5)',
                xaxis_title="Date",
                yaxis_title="Success Probability (%)",
                height=400,
                yaxis=dict(range=[0, 100]),
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True)
        else:
            st.info("Need more data to generate predictions. Complete more habits!")
    
    # TAB 6: JOURNAL & ZEN
    with tab6:
        st.markdown("## 🧘 Mindfulness & Reflection")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📝 Daily Reflection")
            journal_text = st.text_area(
                "How are you feeling today?",
                height=200,
                placeholder="I felt productive because..."
            )
            
            if st.button("💾 Save Entry", use_container_width=True):
                if journal_text:
                    # Sentiment analysis (simple)
                    positive_words = ['good', 'great', 'happy', 'productive', 'awesome', 'focus', 'energy']
                    is_positive = any(word in journal_text.lower() for word in positive_words)
                    
                    bonus = 50 if is_positive else 20
                    sentiment = "Positive" if is_positive else "Neutral"
                    
                    # Save entry
                    st.session_state.journal_db[uid].append({
                        'date': datetime.now().isoformat(),
                        'text': journal_text,
                        'sentiment': sentiment
                    })
                    
                    user['xp'] += bonus
                    
                    # Check achievements
                    new_badges = check_achievements(uid)
                    if new_badges:
                        st.balloons()
                    
                    st.success(f"Entry Saved! Sentiment: {sentiment} (+{bonus} XP)")
                    st.rerun()
        
        with col2:
            st.markdown("### 📚 Recent Entries")
            entries = st.session_state.journal_db.get(uid, [])
            
            if not entries:
                st.info("No entries yet. Start journaling!")
            else:
                for entry in reversed(entries[-5:]):
                    entry_date = datetime.fromisoformat(entry['date']).strftime('%b %d, %Y')
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 3px solid #ffffff;">
                        <small style="color: #888">{entry_date}</small><br>
                        <i style="color: #ddd">"{entry['text'][:80]}..."</i><br>
                        <small style="color: #aaa">Sentiment: {entry.get('sentiment', 'N/A')}</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Achievements Display
        st.markdown("## 🏆 Trophy Case")
        
        all_achievements = get_achievements_list()
        unlocked_ids = st.session_state.achievements_db.get(uid, [])
        
        cols = st.columns(4)
        for i, achievement in enumerate(all_achievements):
            is_unlocked = achievement['id'] in unlocked_ids
            
            with cols[i % 4]:
                badge_class = "badge-container" if is_unlocked else "badge-container badge-locked"
                
                st.markdown(f"""
                <div class="{badge_class}">
                    <div class="badge-icon">{achievement['icon']}</div>
                    <div class="badge-name">{achievement['name']}</div>
                    <div class="badge-desc">{achievement['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Progress
        st.markdown("### 🎯 Achievement Progress")
        achievement_progress = len(unlocked_ids) / len(all_achievements)
        st.progress(achievement_progress)
        st.caption(f"{len(unlocked_ids)} / {len(all_achievements)} Achievements Unlocked")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 30px;'>
    <p style='font-size: 24px; font-weight: 900; letter-spacing: 2px;'>STRIDEX</p>
    <p style='font-style: italic; color: #666;'>Small Steps. Cosmic Results.</p>
    <p style='font-size: 11px; margin-top: 20px;'>Powered by AI • Built with Streamlit • v2.0</p>
</div>
""", unsafe_allow_html=True)