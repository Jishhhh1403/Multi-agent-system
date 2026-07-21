from langchain.chat_models import init_chat_model

from config.settings import settings


llm = init_chat_model(
    f"google_genai:{settings.MODEL}"
)