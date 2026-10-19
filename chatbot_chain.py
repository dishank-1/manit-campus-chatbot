import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# 1. The model
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
)

# 2. The prompt template
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant for students of MANIT Bhopal. "
        "Answer campus-related questions clearly and briefly. "
        "If you are not sure about something, say so instead of guessing."
    ),
    ("human", "{question}"),
])

# 3. The chain: prompt -> model -> plain text
chain = prompt | llm | StrOutputParser()

# 4. Try it
if __name__ == "__main__":
    answer = chain.invoke({"question": "What is the best way to prepare for placements?"})
    print(answer)