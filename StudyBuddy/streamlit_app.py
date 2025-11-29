import streamlit as st
import google.generativeai as genai
import os
import time

# ============================================================================
# GEMINI API CONFIGURATION
# ============================================================================
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# CRITICAL: Cache the model to prevent re-initialization on every run
@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-2.5-flash')

model = get_model()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="StudyBuddy AI",
    layout="wide",
    page_icon="📚",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%); }
.stButton > button { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important; color: white !important; border: none !important; border-radius: 50px !important; padding: 12px 30px !important; font-weight: 700 !important; }
.response-box { background: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #f093fb; margin: 10px 0; }
.error-box { background: #ffebee; padding: 15px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['show_signup'] = False
    st.session_state['subscription_tier'] = 'free'
    st.session_state['chat_responses'] = []  # Persistent responses
    st.session_state['homework_responses'] = []
    st.session_state['exam_responses'] = []

if 'registered_users' not in st.session_state:
    st.session_state['registered_users'] = {'student': 'study123', 'demo': 'demo123'}

def check_credentials(username, password):
    return st.session_state['registered_users'].get(username) == password

# ============================================================================
# SIGNUP PAGE
# ============================================================================
if st.session_state.get('show_signup', False):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# ✨ Create Account")
        new_username = st.text_input("Username", placeholder="min 3 chars", key="new_user")
        new_password = st.text_input("Password", type="password", placeholder="min 6 chars", key="new_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_pass")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button("🎉 Create Account", use_container_width=True):
                if not new_username or not new_password:
                    st.error("❌ Please fill all fields")
                elif new_password != confirm_password:
                    st.error("❌ Passwords don't match!")
                elif new_username in st.session_state['registered_users']:
                    st.error("❌ Username exists!")
                elif len(new_username) < 3 or len(new_password) < 6:
                    st.error("❌ Username: 3+ chars, Password: 6+ chars")
                else:
                    st.session_state['registered_users'][new_username] = new_password
                    st.success(f"✅ Account created! Welcome {new_username}")
                    st.session_state['show_signup'] = False
                    time.sleep(1)
       
        with col_s2:
            if st.button("◀️ Back", use_container_width=True):
                st.session_state['show_signup'] = False
   

# ============================================================================
# LOGIN PAGE
# ============================================================================
elif not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🔐 StudyBuddy AI")
        st.markdown("Your personal AI study assistant")
        
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            if st.button("🚀 Login", use_container_width=True):
                if not username or not password:
                    st.error("❌ Enter username and password")
                elif check_credentials(username, password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success(f"✅ Welcome {username}!")
                    time.sleep(0.5)
       
                else:
                    st.error("❌ Invalid credentials")
        with col_l2:
            if st.button("👤 Guest", use_container_width=True):
                st.session_state['logged_in'] = True
                st.session_state['username'] = 'guest'
                st.session_state['guest_login_time'] = time.time()
   
        
        st.markdown("---")
        if st.button("✨ Create New Account", use_container_width=True, key="signup_btn"):
            st.session_state['show_signup'] = True
            st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================
else:
    # Check guest timeout
    if st.session_state['username'] == 'guest' and 'guest_login_time' in st.session_state:
        elapsed = time.time() - st.session_state['guest_login_time']
        if elapsed >= 300:
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown(f"# 👋 Welcome, {st.session_state['username']}!")
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Chat", "📚 Homework", "📖 Exam Prep", "💎 Premium"])
    
    # ========================================================================
    # TAB 1: AI CHAT
    # ========================================================================
    with tab1:
        st.markdown("### 🤖 Ask AI Study Assistant")
        
        # Display previous responses
        if st.session_state['chat_responses']:
            st.markdown("#### Previous Responses:")
            for idx, resp in enumerate(st.session_state['chat_responses'][-3:], 1):  # Show last 3
                with st.container():
                    st.markdown(f"**Q{idx}:** {resp['question']}")
                    st.markdown(f"**A{idx}:** {resp['answer']}")
                    st.divider()
        
        user_question = st.text_input("Your question:", key="chat_input", placeholder="Ask anything!")
        
        if st.button("📤 Send", key="send_btn", use_container_width=True):
            if not user_question or user_question.strip() == "":
                st.warning("⚠️ Please enter a question")
            else:
                with st.spinner("🤔 Thinking..."):
                    try:
                        response = model.generate_content(
                            f"You are a helpful study assistant. Give clear, concise answers. Question: {user_question}"
                        )
                        st.session_state['chat_responses'].append({
                            'question': user_question,
                            'answer': response.text
                        })
                        st.success("✅ Got it!")
                        st.markdown("### Answer:")
                        st.markdown(response.text)
                               
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)[:100]}")
    
    # ========================================================================
    # TAB 2: HOMEWORK HELP
    # ========================================================================
    with tab2:
        st.markdown("### 📚 Homework Help")
        
        subject = st.selectbox("Subject:", ["Math", "Physics", "Chemistry", "Biology", "English", "History", "Computer Science"])
        homework_q = st.text_area("Describe problem:", height=120, placeholder="Paste your homework problem here...")
        
        if st.button("💡 Get Help", use_container_width=True, key="hw_btn"):
            if not homework_q or homework_q.strip() == "":
                st.warning("⚠️ Enter your homework problem")
            else:
                with st.spinner("📚 Analyzing..."):
                    try:
                        prompt = f"Help solve this {subject} problem step-by-step:\n{homework_q}"
                        response = model.generate_content(prompt)
                        st.session_state['homework_responses'].append({
                            'subject': subject,
                            'problem': homework_q,
                            'solution': response.text
                        })
                        st.success("✅ Solution:")
                        st.markdown(response.text)
                               
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)[:100]}")
    
    # ========================================================================
    # TAB 3: EXAM PREP
    # ========================================================================
    with tab3:
        st.markdown("### 📖 Exam Preparation")
        
        exam_subject = st.selectbox("Subject:", ["Math", "Physics", "Chemistry", "Biology"], key="exam_subj")
        topic = st.text_input("Topic:", placeholder="e.g., Photosynthesis, Quadratic Equations...")
        difficulty = st.select_slider("Difficulty:", options=["Easy", "Medium", "Hard"])
        
        if st.button("📊 Generate Questions", use_container_width=True, key="exam_btn"):
            if not topic or topic.strip() == "":
                st.warning("⚠️ Enter a topic")
            else:
                with st.spinner("📝 Generating..."):
                    try:
                        prompt = f"Generate 5 {difficulty.lower()} practice questions for {exam_subject} on '{topic}'. Include answers."
                        response = model.generate_content(prompt)
                        st.session_state['exam_responses'].append({
                            'subject': exam_subject,
                            'topic': topic,
                            'difficulty': difficulty,
                            'questions': response.text
                        })
                        st.success("✅ Questions:")
                        st.markdown(response.text)
                               
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)[:100]}")
    
    # ========================================================================
    # TAB 4: PREMIUM
    # ========================================================================
    with tab4:
        st.markdown("### 💎 Premium Features")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Free Plan")
            st.write("✅ Basic AI assistance")
            st.write("✅ 3 questions/day")
            st.write("✅ Chat history")
        with col2:
            st.markdown("#### Premium Plan")
            st.write("✅ Unlimited questions")
            st.write("✅ Advanced analysis")
            st.write("✅ Custom practice tests")
            st.write("🆕 **₹299/month**")
            if st.button("💎 Upgrade Now", use_container_width=True):
                st.session_state['subscription_tier'] = 'premium'
                st.success("🎉 Upgraded to Premium!")
    
    # Logout
    st.markdown("---")
    col_logout = st.columns([1, 5, 1])
    with col_logout[0]:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.rerun()
