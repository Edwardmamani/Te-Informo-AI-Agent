from crewai import Crew
from src.tasks.query_tasks import create_query_task, create_suggestions_task
from src.agents.investigador_agent import create_investigador_agent

def create_query_crew(query: str):
    """
    Crea un crew para responder una consulta
    
    Args:
        query: La consulta del usuario
        
    Returns:
        Crew: Un crew configurado con el agente y la tarea
    """
    investigador = create_investigador_agent()
    task = create_query_task(query)
    
    return Crew(
        agents=[investigador],
        tasks=[task],
        verbose=True
    )

def create_suggestions_crew(query: str, context: list = None):
    """
    Crea un crew para generar sugerencias
    
    Args:
        query: El tema principal de interés
        context: Lista de contexto previo de la conversación
        
    Returns:
        Crew: Un crew configurado para generar sugerencias
    """
    investigador = create_investigador_agent()
    task = create_suggestions_task(query, context)
    
    return Crew(
        agents=[investigador],
        tasks=[task],
        verbose=True
    )

