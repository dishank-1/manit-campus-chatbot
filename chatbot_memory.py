
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

# 1. Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
)

# 2. Create a prompt that accepts conversation history
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant for students of MANIT Bhopal. "
        "Use the conversation history to understand follow-up questions. "
        "If you do not know an answer, say so instead of guessing."
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

# 3. Build the normal LCEL chain
chain = prompt | llm | StrOutputParser()

# 4. Store histories for different sessions
store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# 5. Wrap the chain with conversation history
chatbot = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# 6. Test a multi-turn conversation
if __name__ == "__main__":
    config = {"configurable": {"session_id": "student_1"}}

    response1 = chatbot.invoke(
        {"question": "My name is Rahul. I study at MANIT Bhopal."},
        config=config,
    )
    print("Bot:", response1)

    response2 = chatbot.invoke(
        {"question": "Where do I study?"},
        config=config,
    )
    print("Bot:", response2)
