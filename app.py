import streamlit as st
import openai
import os
from openai import OpenAIError, RateLimitError

# --- Set OpenAI API Key ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Generate friendly response based on input ---
def generate_emotional_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 
                 "You are a kind and empathetic friend who gives thoughtful, emotionally aware responses. "
                 "You never mention emotions directly. Just respond like a caring human being listening to someone rant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except RateLimitError:
        return "I'm getting a bit overwhelmed with requests. Please try again in a few moments."
    except OpenAIError as e:
        return f"Oops, something went wrong. Please try again later."

# --- Streamlit UI ---
st.set_page_config(page_title="Emotion Buddy", page_icon="😊")
st.title("🧠 Emotional Companion")

user_input = st.text_input("Talk to me...", placeholder="Type your thoughts here...")

if user_input:
    with st.spinner("Thinking..."):
        reply = generate_emotional_response(user_input)
        st.write(reply)
