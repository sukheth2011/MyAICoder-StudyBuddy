#!/usr/bin/env python
"""
MyAICoder - An AI-powered coding assistant for high school students
"""

import gradio as gr

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

🔍 **Your Code:**
```
{code_snippet[:200]}{' ...' if len(code_snippet) > 200 else ''}
```

Keep coding and learning! 🚀
"""
    return response

def explain_concept(concept):
    """Explain a programming concept"""
    concepts = {
        "variables": "**Variables** store data values. In Python: `x = 5` creates a variable x with value 5.",
        "loops": "**Loops** repeat code. `for i in range(5):` loops 5 times. `while x > 0:` loops while condition is true.",
        "functions": "**Functions** reuse code. Defined with `def my_func():` and called with `my_func()`.",
        "lists": "**Lists** store multiple items: `my_list = [1, 2, 3]`. Access with `my_list[0]`.",
        "dictionaries": "**Dictionaries** store key-value pairs: `my_dict = {'name': 'Ali', 'age': 15}`.",
        "conditionals": "**If-else** makes decisions: `if x > 5:` do something, `else:` do something else.",
        "strings": "**Strings** are text: `my_text = 'Hello'`. Use + to join: `'Hello' + ' World'`.",
    }
    
    if concept.lower() in concepts:
        return concepts[concept.lower()]
    else:
        available = ", ".join(list(concepts.keys())[:5])
        return f"Concept not found. Try: {available}, and more!"

# Create simple Gradio interface
with gr.Blocks(title="MyAICoder", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 MyAICoder - Learn Programming\n\nYour personal AI coding assistant for high school students!")
    
    with gr.Tabs():
        with gr.Tab("Code Analyzer"):
            with gr.Row():
                code_input = gr.Textbox(
                    label="Paste your Python code here",
                    placeholder="Write your code...",
                    lines=8
                )
                analyze_btn = gr.Button("Analyze Code", variant="primary")
                code_output = gr.Markdown()
                analyze_btn.click(analyze_code, inputs=code_input, outputs=code_output)
        
        with gr.Tab("Learn Concepts"):
            with gr.Row():
                concept_select = gr.Textbox(
                    label="Enter a concept to learn",
                    placeholder="e.g., variables, loops, functions, lists...",
                    value="variables"
                )
                explain_btn = gr.Button("Get Explanation", variant="primary")
                concept_output = gr.Markdown()
                explain_btn.click(explain_concept, inputs=concept_select, outputs=concept_output)
        
        with gr.Tab("About"):
            gr.Markdown("""
## About MyAICoder

MyAICoder is designed for 9th-12th grade students learning Python programming.

### Features:
- 📋 **Code Analysis** - Get feedback on your Python code
- 💡 **Concept Learning** - Understand key programming concepts
- 🔐 **Private & Safe** - Your data stays with you
- ⚡ **Fast Feedback** - Instant analysis and explanations

### How to Use:
1. Go to \"Code Analyzer\" tab
2. Paste your Python code
3. Click \"Analyze Code\" to get feedback
4. Go to \"Learn Concepts\" to understand new ideas

Happy coding! 🎉
""")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
