import streamlit as st
from transformers import pipeline

# Load model
classifier = pipeline("text-classification",
                      model="bhadresh-savani/distilbert-base-uncased-emotion",
                      return_all_scores=True)

# Analyze emotions
def analyze_emotions(text):
    results = classifier(text)[0]
    top_emotions = sorted(results, key=lambda x: x['score'], reverse=True)[:3]
    return top_emotions

# Generate empathetic response
def generate_response(emotions):
    labels = [e['label'] for e in emotions]
    return f"I sense you're feeling {' and '.join(labels)}. It's okay to feel this way — thank you for sharing."

# Streamlit UI
st.title("💬 Mixed Emotion Analyzer")
user_input = st.text_area("What's on your mind?", height=150)

if st.button("Analyze"):
    if user_input.strip() != "":
        emotions = analyze_emotions(user_input)
        st.subheader("🎭 Top Emotions")
        for emo in emotions:
            st.write(f"**{emo['label'].capitalize()}** – {emo['score']:.2f}")
        st.subheader("🤖 Response")
        st.write(generate_response(emotions))
    else:
        st.warning("Please enter something to analyze.")
