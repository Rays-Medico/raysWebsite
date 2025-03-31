import os
import streamlit as st

# Streamlit page configuration
st.set_page_config(
    page_title="Ayush",
    page_icon="🤖",
    layout="centered",
)

# Directly define all required values
GROQ_API_KEY='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'

INITIAL_RESPONSE = "Hello! I am Ayush, your virtual health assistant. How can I help you today?"

CHAT_CONTEXT = """You are Ayush, a virtual health assistant designed to provide helpful and accurate information on medical topics. You can offer guidance on symptoms, suggest possible conditions, provide information about medications, recommend when to seek medical attention, and explain medical procedures. 
However, you are not a licensed medical professional, and users should always consult with a healthcare provider for diagnosis and treatment. Maintain a calm, empathetic, and professional tone in all interactions.
"""

INITIAL_MSG = "Hello! I am Ayush, a virtual health assistant designed to provide medical guidance and answer your health-related questions. Please note that I am not a substitute for professional medical advice. How can I assist you today?"

# Save the API key to environment variable (required by Groq client)
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize chat history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": INITIAL_RESPONSE},
    ]

# Page title and caption
st.title("Hey There!")
st.caption("Let's talk developer!...")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar='🤖' if message["role"] == "assistant" else "🗨️"):
        st.markdown(message["content"])

# User input field
user_prompt = st.chat_input("Ask me")

if user_prompt:
    # Display user message
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    try:
        # Import Groq with specific client initialization to handle the issue
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)  # Explicitly pass the API key instead of relying on env var
        
        # Prepare messages for the LLM
        messages = [
            {"role": "system", "content": CHAT_CONTEXT},
            {"role": "assistant", "content": INITIAL_MSG},
            *st.session_state.chat_history[:-1]  # Exclude the most recent user message we just added
        ]

        # Display assistant response (non-streaming for F1 compatibility)
        with st.chat_message("assistant", avatar='🤖'):
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages,
                stream=False  # Disable streaming for Azure F1
            )
            response = completion.choices[0].message.content
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"Error communicating with Groq API: {str(e)}")
        st.info("If you're seeing a 'proxies' error, you may need to update your Groq package. Try running: pip install --upgrade groq")