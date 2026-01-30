import streamlit as st
from groq import Groq
from groq import GroqError

# --- Secure Groq API Key ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- Generate emotionally aware reply ---
def generate_emotional_response(user_input):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a kind and empathetic friend who responds to user thoughts "
                        "without explicitly naming emotions. You sound like a real, caring "
                        "friend who listens deeply and responds supportively."
                    )
                },
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()

    except GroqError:
        return "Oops, something went wrong. Please try again later."

# --- Streamlit UI ---
st.set_page_config(page_title="Emotion Buddy", page_icon="🧠")
st.title("🧠 Emotional Companion")

user_input = st.text_input(
    "Talk to me...",
    placeholder="Type your thoughts here..."
)

if user_input:
    with st.spinner("Thinking..."):
        reply = generate_emotional_response(user_input)
        st.write(reply)
