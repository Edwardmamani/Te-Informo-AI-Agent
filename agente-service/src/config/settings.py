import os
from langchain_openai import ChatOpenAI
from src.utils.env_loader import get_openai_api_key

# Configurar la API key de OpenAI
os.environ["OPENAI_API_KEY"] = get_openai_api_key()

# Configuración del LLM
LLM_CONFIG = {
    "model": "gpt-4o-mini",
    "temperature": 0.7
}

def get_llm():
    """Crea y retorna una instancia del LLM configurado"""
    return ChatOpenAI(
        model=LLM_CONFIG["model"],
        temperature=LLM_CONFIG["temperature"]
    )

# Configuración del servidor
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": int(os.getenv("PORT", 5000)),
    "debug": True
}

