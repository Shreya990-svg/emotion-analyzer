import streamlit as st
from openai import OpenAI
from openai import OpenAIError, RateLimitError

# --- Secure OpenAI Key ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Generate emotionally aware reply ---
def generate_emotional_response(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 
                 "You are a kind and empathetic friend who responds to user thoughts without mentioning emotions. "
                 "You sound like a real, caring friend who listens deeply and responds supportively."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except RateLimitError:
        return "I'm receiving too many requests right now. Please try again soon!"
    except OpenAIError:
        return "Oops, something went wrong. Please try again later."

# --- Streamlit UI ---
st.set_page_config(page_title="Emotion Buddy", page_icon="🧠")
st.title("🧠 Emotional Companion")

user_input = st.text_input("Talk to me...", placeholder="Type your thoughts here...")

if user_input:
    with st.spinner("Thinking..."):
        reply = generate_emotional_response(user_input)
        st.write(reply)
