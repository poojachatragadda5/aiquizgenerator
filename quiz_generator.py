from groq import Groq
import os

# Set your API key (you can later move this to an environment variable or config file for security)
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ["GROQ_API_KEY"])

def generate_quiz(topic: str, model="deepseek-r1-distill-llama-70b") -> str:
    prompt = (
        f"Generate 20 unique multiple-choice quiz questions on '{topic}'. "
        "Each question should have 4 options (A-D) and indicate the correct answer clearly. "
        "Format:\nQ1. Question?\nA. ...\nB. ...\nC. ...\nD. ...\nAnswer: B\n"
    )

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
        temperature=0.8
    )

    return response.choices[0].message.content
