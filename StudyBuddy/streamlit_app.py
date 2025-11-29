import streamlit as st
from datetime import date, timedelta
import google.generativeai as genai
import os
import time

# Initialize API Key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# CACHE THE MODEL - THIS IS KEY FOR PERFORMANCE!
@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-2.5-flash')

model = get_model()

st.set_page_config(page_title="StudyBuddy AI", layout="wide", page_icon="📚")
st.markdown("""<style>.stApp { background: #f5f5f5; color: #000000; padding: 20px; border-radius: 50px; }
.stButton > button { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important; color: white !important; border: none !important; border-radius: 50px !important; padding: 12px 30px !important; font-weight: 700 !important; }</style>""", unsafe_allow_html=True)

# Session State Initialization
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['show_signup'] = False
    st.session_state['subscription_tier'] = 'free'

if 'registered_users' not in st.session_state:
    st.session_state['registered_users'] = {'student': 'study123', 'demo': 'demo123'}

def check_credentials(username, password):
    return st.session_state['registered_users'].get(username) == password

# SIGNUP PAGE
if st.session_state.get('show_signup', False):
    st.markdown('📚 Create New Account', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### ✨ Sign Up")
        new_username = st.text_input("Choose Username", placeholder="Enter a username", key="new_user")
        new_password = st.text_input("Choose Password", type="password", placeholder="Enter a password", key="new_pass")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="confirm_pass")
        col_signup, col_back = st.columns(2)
        with col_signup:
            if st.button("🎉 Create Account", use_container_width=True):
                if new_password != confirm_password:
                    st.error("❌ Passwords don't match!")
                elif new_username in st.session_state['registered_users']:
                    st.error("❌ Username already exists!")
                elif len(new_username) < 3 or len(new_password) < 6:
                    st.error("❌ Username must be 3+ chars, password must be 6+ chars!")
                else:
                    st.session_state['registered_users'][new_username] = new_password
                    st.success(f"✅ Account created for {new_username}!")
                    st.session_state['show_signup'] = False
                    st.rerun()
        with col_back:
            if st.button("◀️ Back to Login", use_container_width=True):
                st.session_state['show_signup'] = False
                st.rerun()

# LOGIN PAGE
elif not st.session_state['logged_in']:
    st.markdown('📚 StudyBuddy AI Login', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Login")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 Login", use_container_width=True):
                if check_credentials(username, password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
        with col_btn2:
            if st.button("👤 Guest Login", use_container_width=True):
                st.session_state['logged_in'] = True
                st.session_state['username'] = 'guest'
                st.session_state['guest_login_time'] = time.time()
                st.success("Logged in as guest! Session expires in 5 minutes.")
                st.rerun()
        if st.button("✨ CREATE NEW ACCOUNT", use_container_width=True, key="signup_btn"):
            st.session_state['show_signup'] = True
            st.rerun()

# MAIN APP
else:
    if st.session_state['username'] == 'guest' and 'guest_login_time' in st.session_state:
        elapsed_time = time.time() - st.session_state['guest_login_time']
        if elapsed_time >= 300:
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.rerun()

    st.markdown(f"### 👋 Welcome, {st.session_state['username']}!")
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Chat", "📚 Homework Help", "📖 Exam Prep", "💎 Premium"])
    
    # TAB 1: AI CHAT
    with tab1:
        st.markdown("### 🤖 AI Study Assistant")
        st.write("Ask me anything about your studies!")
        
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
        
        user_question = st.text_input("Ask your question:", key="chat_input")
        
        if st.button("📤 Send", key="send_btn"):
            if user_question:
                with st.spinner("🤔 Thinking..."):
                    try:
                        response = model.generate_content(
                            f"You are a helpful study assistant for high school students. Answer this question: {user_question}"
                        )
                        st.success("🎉 Answer:")
                        st.write(response.text)
                        st.session_state['chat_history'].append({"Q": user_question, "A": response.text})
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # TAB 2: HOMEWORK HELP
    with tab2:
        st.markdown("### 📝 Homework Help")
        subject = st.selectbox("Select Subject:", ["Math", "Physics", "Chemistry", "Biology", "English", "History"])
        homework_question = st.text_area("Describe your homework problem:", height=150)
        
        if st.button("💡 Get Help", key="homework_btn"):
            if homework_question:
                with st.spinner("📚 Finding solution..."):
                    try:
                        prompt = f"Help with {subject} homework problem. Answer step-by-step:\n{homework_question}"
                        response = model.generate_content(prompt)
                        st.success("✅ Solution:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # TAB 3: EXAM PREP
    with tab3:
        st.markdown("### 🎯 Exam Preparation")
        exam_subject = st.selectbox("Select Subject:", ["Math", "Physics", "Chemistry", "Biology"], key="exam_subject")
        topic = st.text_input("Enter topic to study:")
        
        if st.button("📊 Practice Questions"):
            if topic:
                with st.spinner("📝 Generating questions..."):
                    try:
                        prompt = f"Generate 5 practice questions for {exam_subject} on '{topic}'. Format each with question number and difficulty level."
                        response = model.generate_content(prompt)
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # TAB 4: PREMIUM
    with tab4:
        st.markdown("💎 Upgrade to Premium")
        st.write("✅ Unlimited questions")
        st.write("✅ Advanced AI features")
        st.write("✅ No ads")
        st.markdown("**💵 ₹299/month**")
        if st.button("💎 Upgrade", key="upgrade_btn"):
            st.session_state['subscription_tier'] = 'premium'
            st.success("🎉 Upgraded to Premium!")
    
    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
        st.rerun()
