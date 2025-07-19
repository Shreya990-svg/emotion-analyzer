import streamlit as st
from transformers import pipeline
import openai
import os

# Set your OpenAI API key (you can also use Streamlit secrets later)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load emotion classifier
classifier = pipeline("text-classification",
                      model="bhadresh-savani/distilbert-base-uncased-emotion",
                      return_all_scores=True)

# Generate GPT response
def generate_gpt_response(user_input):
    prompt = f"""
You are a caring and emotionally intelligent friend.

Someone just shared with you: "{user_input}"

Respond in a kind, warm, and supportive way. Be empathetic, like a human friend who truly understands their pain or joy.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or gpt-4 if your key has access
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

# Streamlit UI
st.title("💬 Talk to a Real Friend (Emotion-Aware Chat)")
user_input = st.text_area("What’s on your mind today?", height=150)

if st.button("Talk to me"):
    if user_input.strip():
        # Analyze emotion
        emotion_scores = classifier(user_input)[0]
        top_emotions = sorted(emotion_scores, key=lambda x: x['score'], reverse=True)[:3]

        st.subheader("🎭 Detected Emotions")
        for emo in top_emotions:
            st.write(f"**{emo['label'].capitalize()}** – {emo['score']:.2f}")

        # Generate friend-like response
        st.subheader("🤖 Friend's Response")
        st.write(generate_gpt_response(user_input))
    else:
        st.warning("Please share what you're feeling.")
