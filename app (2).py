import os
import streamlit as st
from groq import Groq

# Set up the Streamlit page layout
st.set_page_config(page_title="AI Learning Roadmap Generator", page_icon="🎓")

# Display Title and Subtitle
st.title("🎓 AI Learning Roadmap Generator")
st.markdown("### Create a personalized learning roadmap with AI")

# --- API KEY SETUP ---
# Streamlit Cloud uses st.secrets, but we also check os.getenv as a fallback
try:
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not set. Add your Groq API key in the Streamlit Cloud Secrets.")
    st.stop() # Stops execution if API key is missing

client = Groq(api_key=api_key)

# --- LOGIC FUNCTION ---
def generate_roadmap(domain, level, duration, hours_per_week):
    if not domain or not domain.strip():
        return "Please enter a learning domain."

    if not duration or not duration.strip():
        return "Please enter a learning duration."

    prompt = f"""
You are an expert learning roadmap designer.

Create a personalized learning roadmap for a student.

STUDENT INFORMATION:
- Learning Domain: {domain}
- Skill Level: {level}
- Learning Duration: {duration}
- Available Time: {hours_per_week} hours per week

Create a realistic and practical roadmap that the student
can actually complete within the given time.

Structure your answer using the following sections:

# 🎯 Learning Objective
Explain what the student should be able to do after completing
the roadmap.

# 📋 Prerequisites
List the knowledge or skills required before starting.

# 🗓️ Learning Roadmap
Divide the roadmap into weeks or months according to
the given learning duration.

For each week/month include:
- Topics to learn
- Important concepts
- Practical exercises
- Mini project

# 🛠️ Practical Projects
Suggest 2-3 projects appropriate for the student's skill level.

# 📚 Recommended Resources
Suggest useful learning resources such as:
- Documentation
- Courses
- YouTube
- Books
- Practice platforms

# ✅ Progress Checkpoints
Give clear checkpoints so the student can measure progress.

# 🏆 Final Capstone Project
Suggest one substantial project that combines the skills learned.

# 🚀 Career Opportunities
Explain what career opportunities or freelance opportunities
the student can explore after completing this roadmap.

IMPORTANT:
- Adjust the difficulty according to the student's skill level.
- Respect the available learning time.
- Do not overload the student.
- Keep the roadmap practical and achievable.
"""

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192", # Switched to a standard Groq model for safety (update if you strictly need your exact model name)
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Unable to generate the roadmap right now. Error: {e}"


# --- USER INTERFACE ---
domain = st.text_input(
    label="📚 Learning Domain",
    placeholder="e.g. Python, AI Automation, Digital Marketing"
)

level = st.selectbox(
    label="📊 Current Skill Level",
    options=["Beginner", "Intermediate", "Advanced"]
)

duration = st.text_input(
    label="⏱️ Learning Duration",
    placeholder="e.g. 2 months, 3 months, 6 months"
)

hours_per_week = st.number_input(
    label="🕐 Available Hours Per Week",
    value=10,
    min_value=1
)

# --- BUTTON ACTION ---
if st.button("🚀 Generate My Roadmap"):
    # Streamlit spinner gives nice visual feedback while the AI generates
    with st.spinner("Generating your personalized roadmap... Please wait."):
        output = generate_roadmap(domain, level, duration, hours_per_week)
        
        st.markdown("---")
        st.markdown("### Your Personalized Roadmap")
        st.markdown(output)