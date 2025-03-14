import streamlit as st
import google.generativeai as genai
import os

# Configure page
st.set_page_config(page_title="Gemini Chatbot", page_icon="💬", layout="wide")

# Set up your API key
GOOGLE_API_KEY = "AIzaSyA7OQchjmlL2msZZuy5ue3hMH8wx3GdBHw"
genai.configure(api_key=GOOGLE_API_KEY)

# Setup model
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

def get_gemini_response(prompt, chat_history=[]):
    """Get a response from the Gemini model with a system prompt"""
    try:
        system_prompt = """
        You are a helpful, friendly, and knowledgeable AI assistant. 
        You provide clear, concise, and accurate information.
        You're happy to help with a wide range of topics and questions.
        When you don't know something, you admit it rather than making up information.
        Your responses are conversational and engaging while remaining informative.
        """
        
        # Create a chat session
        chat = model.start_chat(history=chat_history)
        
        # Add system prompt if this is a new conversation
        if not chat_history:
            chat.send_message(system_prompt)
            
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error getting response from Gemini: {e}")
        return "I'm having trouble processing your request right now. Please try again."

# Add custom styling
st.markdown("""
<style>
    .chat-container {
        border-radius: 10px;
        margin-bottom: 20px;
        padding: 15px;
        background-color: #f5f5f5;
        max-height: 500px;
        overflow-y: auto;
    }
    .user-message {
        background-color: #2e7d32;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin: 5px 0;
        max-width: 70%;
        margin-left: auto;
    }
    .bot-message {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin: 5px 0;
        max-width: 70%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #4CAF50 0%, #1B5E20 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .input-container {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    .stButton > button {
        background-color: #2e7d32;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #1b5e20;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown("<div class='header'><h1>💬 Gemini Chatbot</h1><p>Ask me anything - powered by Google's Gemini AI</p></div>", unsafe_allow_html=True)

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "👋 Hello! I'm your AI assistant powered by Google's Gemini. How can I help you today?"}
    ]
if 'gemini_history' not in st.session_state:
    st.session_state.gemini_history = []

# Display chat messages
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]
    if role == "user":
        st.markdown(f"<div class='user-message'>{content}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>{content}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Chat input
with st.container():
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input("Type your message:", key="user_input", placeholder="Ask me anything...")
    with col2:
        send_button = st.button("Send", key="send", use_container_width=True)

# Process user input when Send is clicked
if send_button and user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Format history for Gemini
    formatted_history = []
    for msg in st.session_state.gemini_history:
        formatted_history.append(msg)
        
    # Get response from Gemini
    with st.spinner("Thinking..."):
        response = get_gemini_response(user_input, formatted_history)
    
    # Update Gemini history
    st.session_state.gemini_history.append({"role": "user", "parts": [user_input]})
    st.session_state.gemini_history.append({"role": "model", "parts": [response]})
    
    # Add assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Clear input
    st.experimental_rerun()

# Sidebar with options
with st.sidebar:
    st.header("Options")
    
    if st.button("Clear Conversation"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "👋 Hello! I'm your AI assistant powered by Google's Gemini. How can I help you today?"}
        ]
        st.session_state.gemini_history = []
        st.rerun()
    
    st.divider()
    st.markdown("### About")
    st.markdown("""
    This chatbot uses Google's Gemini 1.5 Pro model to provide conversational AI capabilities.
    
    - Ask questions
    - Get information
    - Have a conversations
    """)
    st.divider()
    st.markdown("Powered by Gemini 1.5 Pro")