import streamlit as st
from openai import OpenAI
from transformers import pipeline

# Initialize OpenAI client
client = OpenAI()

# Load emotion classifier
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

# Generate GPT-based response based on detected emotion
def generate_emotional_response(user_input):
    # Step 1: Detect emotion
    emotion_result = emotion_model(user_input)
    detected_emotion = emotion_result[0]['label'].lower()

    # Step 2: Generate reply using OpenAI
    prompt = f"""
You are a friendly, empathetic, emotionally intelligent person. A friend just said this:

"{user_input}"

You feel they might be experiencing {detected_emotion}. Respond like a real human friend would — thoughtfully, kindly, and naturally.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are an emotionally intelligent, friendly AI who gives comforting, meaningful replies."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

# Streamlit app UI
st.set_page_config(page_title="Emotionally Intelligent Friend", layout="centered")
st.title("🧠 Talk to a Thoughtful Friend")

user_input = st.text_area("What's on your mind?", height=200)

if st.button("Send"):
    if user_input.strip() != "":
        with st.spinner("Thinking like a good friend..."):
            reply = generate_emotional_response(user_input)
            st.markdown("### 🧑‍💬 Reply")
            st.write(reply)
    else:
        st.warning("Please share something so I can respond.")
