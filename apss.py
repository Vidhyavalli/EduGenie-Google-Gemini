import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="EduGenie - Learning Assistant", page_icon="🧞‍♂️", layout="centered"
)

st.title("🧞‍♂️ EduGenie: Your AI Learning Assistant")
st.write(
    "Ask any question related to your studies, programming, math, or science, and get instant explanations!"
)

# Initialize Gemini Client (Ensure your API key is set in environment variables or hardcoded for testing)
# It's best to use st.secrets for Streamlit Cloud deployment
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except:
    # Fallback or prompt for local testing if secrets aren't set yet
    api_key = st.text_input("Enter your Google Gemini API Key:", type="password")
    if api_key:
        client = genai.Client(api_key=api_key)
    else:
        st.warning(
            "Please enter your Gemini API Key to start chatting with EduGenie."
        )
        client = None

# Chat interface using Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
if prompt := st.chat_input("What do you want to learn today?"):
    if client is None:
        st.error("Please provide a valid Gemini API Key first!")
    else:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response using Gemini
        with st.chat_message("assistant"):
            with st.spinner("EduGenie is thinking..."):
                try:
                    # Using gemini-2.5-flash as a fast and reliable model for text
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=f"You are EduGenie, a helpful AI learning assistant. Explain the following concept clearly to a student: {prompt}",
                    )
                    ai_response = response.text
                    st.markdown(ai_response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": ai_response}
                    )
                except Exception as e:
                    st.error(f"An error occurred: {e}")