import streamlit as st
from groq import Groq
import os
import re

# Set API key
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# List of topics
topics = [
    "Python", "Java", "C++", "Data Structures", "Algorithms", "Machine Learning", "Deep Learning",
    "Artificial Intelligence", "Computer Networks", "Operating Systems", "Databases", "SQL", "MongoDB",
    "Cybersecurity", "Cloud Computing", "AWS", "Azure", "Google Cloud", "HTML", "CSS", "JavaScript",
    "React", "Node.js", "Express.js", "Flask", "Django", "Blockchain", "Cryptography", "IoT", "Big Data",
    "DevOps", "Software Testing", "Agile Methodology", "Scrum", "Kanban", "Linux", "Shell Scripting",
    "Data Science", "Mathematics", "Physics", "Chemistry", "Biology", "History", "Geography", "English Grammar"
]

st.set_page_config("AI Quiz Generator", layout="centered")
st.title("🧠 AI Quiz Generator")

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Topic selection
selected_topic = st.selectbox("📚 Choose a Topic or Enter Your Own", topics + ["Other"])
if selected_topic == "Other":
    selected_topic = st.text_input("📝 Enter your custom topic:")

# Generate quiz
if selected_topic and st.button("🎯 Generate Quiz"):
    st.session_state.submitted = False
    prompt = (
        f"Generate 10 unique multiple-choice quiz questions on '{selected_topic}'. "
        "Each question should have 4 options (A-D) and indicate the correct answer clearly. "
        "Format:\nQ1. Question?\nA. ...\nB. ...\nC. ...\nD. ...\nAnswer: B\n"
    )

    with st.spinner("Generating quiz..."):
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="deepseek-r1-distill-llama-70b",
            temperature=0.8
        )

        quiz_text = response.choices[0].message.content
        blocks = re.split(r"\nQ\d+\.", "\n" + quiz_text)
        parsed_questions = []

        for block in blocks[1:]:
            lines = block.strip().split("\n")
            question = lines[0].strip()
            options = [line.strip() for line in lines[1:5] if re.match(r"^[A-D]\.", line)]
            answer_line = next((line for line in lines if line.lower().startswith("answer:")), "")
            answer = answer_line.split(":")[1].strip().upper()
            parsed_questions.append({"question": question, "options": options, "answer": answer})

        st.session_state.questions = parsed_questions
        st.session_state.answers = {}

# Display quiz
if st.session_state.questions and not st.session_state.submitted:
    st.subheader("📝 Take the Quiz")

    for i, q in enumerate(st.session_state.questions):
        user_answer = st.radio(
            f"Q{i+1}. {q['question']}",
            q['options'],
            key=f"q_{i}"
        )
        st.session_state.answers[i] = user_answer

    if st.button("🚀 Submit Quiz"):
        st.session_state.submitted = True

# Show results
if st.session_state.submitted:
    st.subheader("📊 Results")
    score = 0
    for i, q in enumerate(st.session_state.questions):
        user_ans = st.session_state.answers.get(i, "")
        correct_letter = q["answer"]
        correct_option = next((opt for opt in q["options"] if opt.startswith(correct_letter)), "Not Found")

        st.markdown(f"**Q{i+1}. {q['question']}**")
        st.write(f"Your answer: {user_ans}")
        if user_ans.startswith(correct_letter):
            st.success("✅ Correct!")
            score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {correct_option}")

    st.markdown(f"## 🎉 Your Final Score: `{score}/10`")
