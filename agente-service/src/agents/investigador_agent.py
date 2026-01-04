from crewai import Agent
from src.config.settings import get_llm
from src.tools.news_api_tool import search_news_tool, extract_content_tool

llm = get_llm()

def create_investigador_agent():
    """
    Crea y retorna un agente investigador configurado con acceso a herramientas de noticias
    
    Returns:
        Agent: Un agente investigador configurado con el LLM y herramientas de noticias
    """
    return Agent(
        role='Investigador de Noticias',
        goal='Investigar y analizar información sobre temas solicitados usando múltiples fuentes de noticias',
        backstory=(
            'Eres un experto investigador que puede analizar información, '
            'resumir contenido y proporcionar insights valiosos sobre cualquier tema. '
            'Tienes experiencia en investigación periodística y análisis de datos. '
            'Tienes acceso a herramientas que te permiten buscar noticias en múltiples fuentes '
            'confiables como Google News, BBC, CNN, El País y YouTube, así como extraer el '
            'contenido completo de artículos específicos para análisis profundo.'
        ),
        llm=llm,
        verbose=True,
        tools=[search_news_tool, extract_content_tool],  # Herramientas de noticias del backend
        allow_delegation=False
    )

