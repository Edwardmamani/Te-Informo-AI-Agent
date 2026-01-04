import os
from dotenv import load_dotenv, find_dotenv

# these expect to find a .env file at the directory above the lesson.
# the format for that file is (without the comment)
# API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService

def load_env():
    """Carga las variables de entorno desde el archivo .env"""
    _ = load_dotenv(find_dotenv())

def get_openai_api_key():
    """Obtiene la API key de OpenAI desde las variables de entorno"""
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key

def get_exa_api_key():
    """Obtiene la API key de Exa desde las variables de entorno"""
    load_env()
    exa_api_key = os.getenv("EXA_API_KEY")
    return exa_api_key

