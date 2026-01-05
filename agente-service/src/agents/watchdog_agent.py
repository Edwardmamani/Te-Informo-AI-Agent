from crewai import Agent
from src.config.settings import get_llm

llm = get_llm()

def create_watchdog_agent():
    """
    Crea y retorna un agente Watchdog (Investigador) configurado
    
    El Watchdog es responsable de:
    - Analizar información pre-buscada del backend
    - Filtrar información por relevancia
    - Entregar informe preliminar
    - Replanificar análisis si se detectan problemas (backtracking)
    
    Returns:
        Agent: Un agente Watchdog configurado con el LLM
    """
    return Agent(
        role='Investigador (Watchdog)',
        goal='Analizar y filtrar información relevante para la noticia solicitada',
        backstory=(
            'Eres un investigador periodístico experto con gran capacidad de análisis. '
            'Tu función es analizar información proporcionada del backend, filtrarla por relevancia '
            'y presentar un informe preliminar estructurado. Cuando se detectan problemas de calidad, '
            'sesgos o datos falsos, debes replanificar el análisis y solicitar información adicional '
            'hasta alcanzar el umbral de calidad requerido. Tienes una gran capacidad de análisis y '
            'experiencia en evaluación de fuentes periodísticas.'
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
