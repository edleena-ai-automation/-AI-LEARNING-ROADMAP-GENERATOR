import os
import gradio as gr
from groq import Groq

# Groq API key is read from an environment variable.
# NEVER hard-code the API key in this file.
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is not set. Add your Groq API key as an environment "
        "variable/secret in your deployment platform."
    )

client = Groq(api_key=api_key)


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
            model="openai/gpt-oss-20b",
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


with gr.Blocks() as app:
    gr.Markdown(
        """
        # 🎓 AI Learning Roadmap Generator

        ### Create a personalized learning roadmap with AI
        """
    )

    domain = gr.Textbox(
        label="📚 Learning Domain",
        placeholder="e.g. Python, AI Automation, Digital Marketing"
    )

    level = gr.Dropdown(
        choices=[
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        value="Beginner",
        label="📊 Current Skill Level"
    )

    duration = gr.Textbox(
        label="⏱️ Learning Duration",
        placeholder="e.g. 2 months, 3 months, 6 months"
    )

    hours_per_week = gr.Number(
        label="🕐 Available Hours Per Week",
        value=10,
        minimum=1
    )

    generate_button = gr.Button("🚀 Generate My Roadmap")

    output = gr.Markdown(label="Your Personalized Roadmap")

    generate_button.click(
        fn=generate_roadmap,
        inputs=[domain, level, duration, hours_per_week],
        outputs=output
    )


if __name__ == "__main__":
    app.launch()
