import os
import logging
from google import genai

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Get API Key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables")

# Configure the client
client = genai.Client(api_key=GEMINI_API_KEY)

# Use a valid, available model
MODEL_NAME = "models/gemini-2.5-flash"

def generate_answer(user_query: str, context: str | None = None) -> str:
    try:
        prompt = _build_prompt(user_query, context)
        logger.info("Generating Gemini response")
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if not response or not response.text:
            logger.warning("Empty response from Gemini")
            return "Sorry, I could not generate an answer at the moment."

        return response.text.strip()

    except Exception as e:
        logger.exception("Gemini generation failed")
        print("GEMINI ERROR >>>", e) 
        return "An internal error occurred while generating the response."

def _build_prompt(user_query: str, context: str | None) -> str:
    """
    Builds a safe, controlled prompt for company KB chatbot
    """
    system_prompt = (
        "You are an AI assistant for a company website. "
        "Answer clearly, professionally, and only using the provided context. "
        "If the answer is not available in the context, say you don't have that information."
    )

    if context:
        return f"""
            {system_prompt}

            Context:
            {context}

            User Question:
            {user_query}
            """
    
    else:
        return f"""
            {system_prompt}

            User Question:
            {user_query}
            """
