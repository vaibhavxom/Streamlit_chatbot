import streamlit as st
import requests

# API details
API_KEY = st.secrets["general"]["API_KEY"]  # Replace with your actual API key
API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}'  # Correct endpoint URL for Gemini

# Function to interact with Gemini API with caching
@st.cache_data
def get_gemini_response(message):
    headers = {
        'Content-Type': 'application/json',
    }

    payload = {
        'contents': [{
            'parts': [{
                'text': message
            }]
        }]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # Check for successful response
    if response.status_code == 200:
        response_data = response.json()
        try:
            bot_response = response_data['candidates'][0]['content']['parts'][0]['text']
            return bot_response
        except KeyError:
            return "Sorry, something went wrong."
    else:
        return f"Error: {response.status_code}, {response.text}"

# Streamlit UI
def chatbot():
    st.title("Chatbot with Gemini AI")

    # Apply custom CSS styles to improve UI appearance
    st.markdown("""
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f4;
                color: #333;
                margin: 0;
                padding: 0;
            }
            .message-box {
                padding: 12px 18px;
                border-radius: 15px;
                margin: 10px 0;
                max-width: 80%;
                word-wrap: break-word;
                color: #333;
                font-size: 16px;
                text-align: justify;
            }
            .user-message {
                background-color: #4CAF50;
                color: white;
                text-align: left;
                margin-left: auto;
            }
            .bot-message {
                background-color: #9E9E9E;
                color: white;
                text-align: justify;
                margin-right: auto;
            }
            .chat-container {
                max-height: 400px;
                overflow-y: auto;
                margin-bottom: 15px;
                padding: 10px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            .stTextInput>div>input {
                border-radius: 20px;
                padding: 12px;
                font-size: 16px;
                border: 1px solid #ddd;
                width: 100%;
                background-color: #fff;
                color: #333;
            }
            .stButton>button {
                background-color: #2196F3;
                color: white;
                border-radius: 30px;
                padding: 12px;
                font-size: 16px;
                width: 100%;
                border: none;
            }
            .stButton>button:hover {
                background-color: #1976D2;
            }
            .stButton>button:focus {
                outline: none;
            }
            @media (max-width: 600px) {
                .message-box {
                    font-size: 14px;
                }
                .stTextInput>div>input {
                    font-size: 14px;
                }
                .stButton>button {
                    font-size: 14px;
                }
            }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state for message history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past messages in the chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg.startswith(":User "):
            st.markdown(f'<div class="message-box user-message">{msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-box bot-message">{msg}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Callback to handle user message input
    def handle_input():
        user_message = st.session_state.user_input
        if user_message:
            # Append the user's message to the session state for immediate display
            st.session_state.messages.append(f":User  {user_message}")

            # Show loading spinner while waiting for the response
            with st.spinner("Bot is thinking..."):
                response = get_gemini_response(user_message)

            # Append bot's response to the session state for immediate display
            st.session_state.messages.append(f"Bot: {response}")

            # Reset user input field to be empty
            st.session_state.user_input = ""  # Clear the input field after submission

    # Input for user message, tied to the session state
    st.text_input("Ask me anything:", key="user_input", on_change=handle_input)

    # Clear chat button (fixed single-click behavior)
    if st.button("Clear Chat"):
        st.session_state.messages.clear()  # Clear the chat history

if __name__ == "__main__":
    chatbot()