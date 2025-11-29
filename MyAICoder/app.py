#!/usr/bin/env python
import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# Page configuration
st.set_page_config(page_title="MyAICoder - Code Analysis", layout="wide", page_icon="📝")

def analyze_code(code_snippet):
    """Analyze code and provide suggestions"""
    if not code_snippet or code_snippet.strip() == "":
        return "Please enter some code to analyze."
    
    lines = code_snippet.strip().split("\n")
    char_count = len(code_snippet)
    
    response = f"""
**Code Analysis Results:**
📊 **Metrics:**
- Total Characters: {char_count}
- Total Lines: {len(lines)}
- Average Line Length: {char_count // len(lines) if lines else 0}

💡 **Tips for Better Code:**
1. Use meaningful variable names
2. Add comments to explain logic
3. Follow consistent indentation
4. Test with different inputs
5. Keep functions focused and small

🔍 **Your Code Sample:**
```python
{code_snippet[:200]}{'...' if len(code_snippet) > 200 else ''}
```

Keep coding and learning! 🚀
    """
    return response

# Main UI
st.title("📝 MyAICoder - AI Code Assistant")
st.markdown("### Learn Python Programming with AI Assistance")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Code Analyzer", "Concept Learning", "Quick Tips", "About"])

with tab1:
    st.markdown("## 📝 Code Analysis")
    st.write("Paste your Python code and get AI-powered feedback!")
    
    code_input = st.text_area("Enter your code:", height=200, placeholder="# Paste your Python code here...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Analyze Code", use_container_width=True):
            if code_input:
                analysis = analyze_code(code_input)
                st.success("Analysis Complete!")
                st.markdown(analysis)
            else:
                st.warning("Please enter some code to analyze.")
    
    with col2:
        if st.button("🤖 Get AI Feedback", use_container_width=True):
            if code_input:
                try:
                    prompt = f"As a Python mentor, provide constructive feedback for this code:\n\n{code_input}"
                    ai_response = model.generate_content(prompt)
                    st.info("AI Feedback:")
                    st.write(ai_response.text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter code first.")

with tab2:
    st.markdown("## 📚 Concept Learning")
    
    st.markdown("""
    ### Python Basics
    - **Variables**: Containers for storing data
    - **Data Types**: int, float, str, bool, list, dict
    - **Functions**: Reusable blocks of code
    - **Loops**: Repeat code multiple times
    - **Conditionals**: Make decisions in code
    
    ### Best Practices
    - Write clean, readable code
    - Use proper variable naming
    - Add comments and documentation
    - Test your code thoroughly
    - Follow PEP 8 style guide
    """)
    
    st.markdown("### 🤔 Ask About a Concept")
    concept_question = st.text_input("What concept would you like to learn about?")
    
    if st.button("📚 Learn More", use_container_width=True):
        if concept_question:
            try:
                prompt = f"Explain this Python concept for a high school student: {concept_question}"
                explanation = model.generate_content(prompt)
                st.success("Explanation:")
                st.write(explanation.text)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a concept to learn about.")

with tab3:
    st.markdown("## 🎉 Quick Tips & Tricks")
    
    st.markdown("""
    ### Python Tips
    - **List Comprehension**: `[x for x in range(10)]`
    - **Dictionary Get**: `dict.get('key', default)`
    - **F-Strings**: `f"Hello {name}"`
    - **Lambda Functions**: `lambda x: x * 2`
    - **Enumerate**: `for i, item in enumerate(list)`
    
    ### Code Quality
    - 📝 Write meaningful comments
    - 📚 Follow PEP 8 style guide
    - 🤖 Use descriptive variable names
    - 🧠 Keep functions small and focused
    - ✅ Test your code regularly
    """)

with tab4:
    st.markdown("## 📄 About MyAICoder")
    st.markdown("""
    ### Welcome to MyAICoder!
    
    MyAICoder is designed for 9th-12th grade students learning Python programming.
    
    #### Features:
    - 📝 **Code Analyzer** - Get feedback on your Python code
    - 📚 **Concept Learning** - Understand programming concepts
    - 🎉 **Quick Tips** - Learn best practices and tricks
    - 🤖 **AI-Powered** - Get help from Gemini AI
    
    #### How to Use:
    1. Go to "Code Analyzer" tab
    2. Paste your Python code
    3. Click "Analyze Code" to get metrics
    4. Click "Get AI Feedback" for suggestions
    5. Use "Concept Learning" to understand new topics
    
    **Keep coding and learning!** 🚀
    """)

st.markdown("---")
st.markdown("**Made with ❤️ for student coders** | Powered by Gemini AI")
