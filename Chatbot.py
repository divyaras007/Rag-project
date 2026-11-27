import streamlit as st
st.header("hi Chatbot")

import streamlit as st
from groq import Groq

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------------
# GROQ API KEY
# ---------------------------------

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# ---------------------------------
# CUSTOM CSS
# ---------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #101820;
    color: white;
}

h1 {
    color: #00D4FF;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #AAAAAA;
    font-size: 16px;
}

.stChatMessage {
    background-color: #1E293B;
    border-radius: 12px;
}

.stChatInput {
    border: 1px solid #00D4FF;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# TITLE
# ---------------------------------

st.title("🤖 AI Chatbot")

st.markdown(
    '<p class="subtitle">Powered by Streamlit and Groq AI</p>',
    unsafe_allow_html=True
)

st.divider()

# ---------------------------------
# SIDEBAR
# ---------------------------------

with st.sidebar:
    st.title("⚙️ Settings")

    st.write("Welcome to your AI Assistant!")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### About")

    st.write(
        "This chatbot uses Groq AI to answer "
        "your questions instantly."
    )

    st.write("openai/gpt-oss-120b")

# ---------------------------------
# CHAT HISTORY
# ---------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------
# USER INPUT
# ---------------------------------

user_input = st.chat_input("Ask me anything...")

if user_input:

    # Display user message

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response

    with st.chat_message("assistant"):
        try:
            with st.spinner("🤖 Thinking..."):

                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful, friendly AI assistant. "
                                "Give clear and informative answers."
                            )
                        }
                    ] + st.session_state.messages,

                    model="openai/gpt-oss-120b",
                    temperature=0.7,
                    max_completion_tokens=1024
                )

                response = (
                    chat_completion
                    .choices[0]
                    .message.content
                )

                st.markdown(response)

                # Save AI response

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

        except Exception as e:
            st.error(f"Error: {str(e)}")

            st.info(
                "Please check your Groq API key "
                "and internet connection."
            )
