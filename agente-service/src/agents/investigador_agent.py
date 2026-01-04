from crewai import Agent
from src.config.settings import get_llm

llm = get_llm()

def create_investigador_agent():
    """
    Crea y retorna un agente investigador configurado
    
    Returns:
        Agent: Un agente investigador configurado con el LLM
    """
    return Agent(
        role='Investigador de Noticias',
        goal='Investigar y analizar información sobre temas solicitados',
        backstory=(
            'Eres un experto investigador que puede analizar información, '
            'resumir contenido y proporcionar insights valiosos sobre cualquier tema. '
            'Tienes experiencia en investigación periodística y análisis de datos.'
        ),
        llm=llm,
        verbose=True
    )

