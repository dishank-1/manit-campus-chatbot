
import uuid

import streamlit as st

from chatbot_memory import chatbot, get_session_history

# 1. Configure the web page
st.set_page_config(
    page_title="MANIT Campus Chatbot",
    page_icon="🎓",
    layout="centered",
)

# 2. Display the title
st.title("🎓 MANIT Campus Chatbot")
st.caption("Your AI assistant for campus-related questions.")

# 3. Create a unique conversation session
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

session_id = st.session_state.session_id

config = {
    "configurable": {
        "session_id": session_id
    }
}

# 4. Add a reset button in the sidebar
with st.sidebar:
    st.header("Chat settings")
    st.write("Ask questions about campus life and academics.")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        get_session_history(session_id).clear()
        st.session_state.messages = []
        st.rerun()

# 5. Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Accept a new question
question = st.chat_input("Ask your campus question...")

if question:
    # Display and save the user's message
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate the AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = chatbot.invoke(
                    {"question": question},
                    config=config,
                )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                })

            except Exception:
                st.error(
                    "Sorry, something went wrong. "
                    "Check your API key, model configuration, "
                    "internet connection, and quota."
                )
