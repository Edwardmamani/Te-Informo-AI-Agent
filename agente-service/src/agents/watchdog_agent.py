from crewai import Agent
from src.config.settings import get_llm

llm = get_llm()

def create_watchdog_agent():
    """
    Crea y retorna un agente Watchdog (Investigador) configurado
    
    El Watchdog es responsable de:
    - Activar sensores (herramientas de búsqueda)
    - Recopilar información cruda
    - Filtrar por relevancia
    - Entregar informe preliminar
    - Replanificar búsqueda si se detectan problemas (backtracking)
    - Buscar fuentes alternativas cuando es necesario
    
    Returns:
        Agent: Un agente Watchdog configurado con el LLM
    """
    return Agent(
        role='Investigador (Watchdog)',
        goal='Investigar, recopilar y filtrar información relevante para la noticia solicitada',
        backstory=(
            'Eres un investigador periodístico experto con acceso a múltiples fuentes y herramientas de búsqueda. '
            'Tu función es activar sensores de búsqueda, recopilar información cruda de diversas fuentes, '
            'filtrarla por relevancia y presentar un informe preliminar. Cuando se detectan problemas de calidad, '
            'sesgos o datos falsos, debes replanificar la búsqueda (backtracking) y buscar fuentes alternativas '
            'hasta alcanzar el umbral de calidad requerido. Tienes una gran capacidad de análisis y una red '
            'extensa de fuentes confiables.'
        ),
        llm=llm,
        verbose=True,
        tools=[]  # Aquí se pueden agregar herramientas de búsqueda específicas
    )
