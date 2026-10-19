import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Read the variables from the .env file into the environment
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise SystemExit("GOOGLE_API_KEY not found. Check your .env file.")

model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# 2. Create the model object
llm = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=api_key,
    temperature=0.3,
)

# 3. Send one question and print the reply
response = llm.invoke("In one sentence, what is MANIT Bhopal known for?")
print(response.content)