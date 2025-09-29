import streamlit as st
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyBY0SXoNHy6tbSStt7X4seKNF-SUL3_u_s"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
persona_instructions = """
You are a friendly, encouraging study buddy.
Use a cheerful tone, emojis are allowed.
Always offer helpful tips for learning.
"""

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_gemini_response(prompt, persona_instructions):
    full_prompt = f"{persona_instructions}\n\nUser: {prompt}\nAssistant:"
    response = model.generate_content(full_prompt)
    return response.text

def main():
    st.title("AI Chatbot")
    
    initialize_session_state()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

if prompt := st.chat_input("Chat with Gemini"):
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get Gemini response with persona
    response = get_gemini_response(prompt, persona_instructions)

    # Display assistant response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()


