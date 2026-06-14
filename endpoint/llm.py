from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from config import AI_API_KEY, PROMPT_TEMPLATE
import os
google_key = os.getenv("AI_API_KEY_2") or AI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",  # other options (gemini-3-flash-preview | gemini-3.1-pro-preview)
    google_api_key=google_key,
)

prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful assistant."), ("user", PROMPT_TEMPLATE)]
)

chain = prompt | llm


def extract_text(content) -> str:
    if isinstance(content, list):
        return "".join(
            block.get("text", "") for block in content if isinstance(block, dict)
        )
    return content
